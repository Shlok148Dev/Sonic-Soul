"""
Supabase SQL Migrations — Table schema for PSYCHE.

Run these in the Supabase SQL editor to create the required tables.
"""

MIGRATION_001 = """
-- PSYCHE Database Schema v0.1.0
-- Execute in Supabase SQL Editor

-- User Sonic Genomes
CREATE TABLE IF NOT EXISTS sonic_genomes (
    user_id TEXT PRIMARY KEY,
    genome JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Listening Events (the primary user interaction log)
CREATE TABLE IF NOT EXISTS listening_events (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    track_id TEXT NOT NULL,
    event_type TEXT NOT NULL CHECK (event_type IN ('play', 'skip', 'save', 'replay', 'complete')),
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    metadata JSONB DEFAULT '{}',
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES sonic_genomes(user_id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_events_user_time ON listening_events(user_id, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_events_track ON listening_events(track_id);

-- Cold Start Interview Results
CREATE TABLE IF NOT EXISTS cold_start_results (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES sonic_genomes(user_id) ON DELETE CASCADE,
    answers JSONB NOT NULL DEFAULT '[]',
    initial_radar JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_cold_start_user ON cold_start_results(user_id);

-- User Sessions (for temporal taste tracking)
CREATE TABLE IF NOT EXISTS sessions (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES sonic_genomes(user_id) ON DELETE CASCADE,
    started_at TIMESTAMPTZ DEFAULT NOW(),
    ended_at TIMESTAMPTZ,
    listener_state JSONB DEFAULT '{}',
    context JSONB DEFAULT '{}',
    recommendations_served INT DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id, started_at DESC);

-- Enable Row Level Security
ALTER TABLE sonic_genomes ENABLE ROW LEVEL SECURITY;
ALTER TABLE listening_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE cold_start_results ENABLE ROW LEVEL SECURITY;
ALTER TABLE sessions ENABLE ROW LEVEL SECURITY;

-- RLS Policies: users can only access their own data
CREATE POLICY "Users can read own data" ON sonic_genomes
    FOR SELECT USING (auth.uid()::text = user_id);
CREATE POLICY "Users can insert own data" ON sonic_genomes
    FOR INSERT WITH CHECK (auth.uid()::text = user_id);
CREATE POLICY "Users can update own data" ON sonic_genomes
    FOR UPDATE USING (auth.uid()::text = user_id);

-- Repeat for other tables
CREATE POLICY "Users read own events" ON listening_events
    FOR SELECT USING (auth.uid()::text = user_id);
CREATE POLICY "Users insert own events" ON listening_events
    FOR INSERT WITH CHECK (auth.uid()::text = user_id);
""";
