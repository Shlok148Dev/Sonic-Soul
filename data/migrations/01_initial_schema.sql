-- PSYCHE Phase 3 Database Initial Migrations
-- Target: Supabase PostgreSQL
-- Creates baseline schema mappings for tracking user sessions & listener states

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Users Table (Core generic mapping for the genome base)
CREATE TABLE public.psyche_users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    username TEXT UNIQUE NOT NULL,
    sonic_genome JSONB DEFAULT '{}'::jsonb
);

-- 2. Listener States (Tracking ESIE outputs historically)
CREATE TABLE public.listener_states (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    user_id UUID REFERENCES public.psyche_users(id) ON DELETE CASCADE,
    valence FLOAT NOT NULL CHECK (valence >= -1 AND valence <= 1),
    arousal FLOAT NOT NULL CHECK (arousal >= -1 AND arousal <= 1),
    focus FLOAT NOT NULL CHECK (focus >= 0 AND focus <= 1),
    social_mode FLOAT NOT NULL CHECK (social_mode >= 0 AND social_mode <= 1),
    confidence FLOAT NOT NULL CHECK (confidence >= 0 AND confidence <= 1),
    inference_method TEXT NOT NULL,
    raw_signals JSONB DEFAULT '{}'::jsonb
);

-- Row Level Security (RLS) Rules for security checks
ALTER TABLE public.psyche_users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.listener_states ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can only read their own data" ON public.psyche_users
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Listener states are self-accessible" ON public.listener_states
    FOR ALL USING (auth.uid() = user_id);

-- Setup Index for faster user_id trajectory lookups
CREATE INDEX idx_listener_states_user ON public.listener_states(user_id, created_at DESC);
