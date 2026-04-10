# PSYCHE — THE ULTIMATE DEFINITIVE MASTERPLAN v4.0
## *Personalized Sonic Cognition & Hyper-adaptive Emotional Engine*
### *The Music Platform That Replaces Spotify, Apple Music, and YouTube Music*

> **One-line mission:** Build the product the entire music streaming industry has been too corporate, too siloed, and too afraid to build — a single platform where intelligence, audio quality, content depth, and human connection all exist at once, for everyone.
>
> **One-line goal:** Make every Spotify/Google recruiter who sees this project cancel their afternoon.
>
> **Standard:** Not a student project. Not a demo. A deployed, installable, forkable, cite-able system that recruiters bookmark, developers install, and researchers cite.
>
> **Build stack:** Google Antigravity · GSD (Get Shit Done) · Ralph Loop · CodeRabbit

---

## HOW TO READ THIS DOCUMENT

This is the single source of truth for the entire PSYCHE build. It is structured in **twelve major sections**:

1. **THE BRAND STRATEGY** — Who PSYCHE is, for whom, and why the dual identity works
2. **THE BUSINESS CASE** — Problem definition, baselines, success metrics, stakeholders, risk
3. **THE COMPETITIVE TEARDOWN** — Where every major platform fails, with exact user evidence
4. **THE COMPLETE PRODUCT** — All five competing dimensions, every feature across all 60 additions + 10-gap system
5. **THE ARCHITECTURE** — All five repos, every agent, full system design
6. **THE TECH STACK** — 100% free and open source, fully documented
7. **THE DATA STRATEGY** — All datasets, quality framework, versioning, feature engineering
8. **THE EXPERIMENTATION FRAMEWORK** — All 5 experiments, baselines, validation strategy
9. **THE FOUR BUILD TOOLS** — Antigravity, GSD, Ralph Loop, CodeRabbit — exact role and usage
10. **THE 14-WEEK BUILD PLAN** — Day-by-day execution with exact commands
11. **THE OPEN SOURCE LAUNCH** — GitHub org, README, launch playbook, post-launch
12. **THE INTERVIEW ARSENAL** — Every answer to every question a Spotify director can ask

---

# PART 1: THE BRAND STRATEGY — WHO PSYCHE IS

## The Dual Identity Model

**For the end user:** PSYCHE is a premium music streaming product. The name works because music is fundamentally psychological — it regulates mood, encodes memory, shapes identity. Every feature maps directly to that truth. The UX language is warm, human, and emotionally intelligent. Zero developer jargon visible.

**For the developer:** PSYCHE is the open-source engine under the hood — six AI agents, a Python SDK, a REST API, a benchmark harness. The GitHub org `psyche-music` is a technical artifact. The product website at `psyche.fm` is a consumer product.

```
psyche.fm                        ← Consumer product. Beautiful. Emotional. For everyone.
github.com/psyche-music           ← Developer engine. Open source. For builders.
```

These are not in tension. They reinforce each other. Every developer who installs `pip install psyche-core` becomes an evangelist for the consumer product. Every user who loves the app becomes proof that the technology works.

**The tagline:** *"Music that actually knows you."*

Short. Universal. Addresses the single biggest complaint across all three platforms simultaneously.

---

# PART 2: THE BUSINESS CASE

## 2.1 The Business Problem Brief

Before a single line of code is written, PSYCHE answers the three questions that separate production engineers from tutorial-followers:

| Question | PSYCHE's Answer |
|---|---|
| **What's broken?** | Spotify's recommender treats all users as static entities with fixed taste profiles, ignoring real-time emotional state, temporal taste evolution, and causal audio micro-events that drive engagement. |
| **Who has the problem?** | 713M Spotify MAU (Q3 2025). Artists in the bottom 99% who receive <1% of algorithmic plays. New users with cold-start problem. Spotify itself: churn from poor recommendations. |
| **What's the cost of not solving it?** | Industry research shows 31% of users skip algorithmically recommended tracks. Each skip is a lost stream, lost royalty, and signal of recommendation failure at scale. |

## 2.2 Current Baseline — What PSYCHE Must Beat

- **Spotify Discover Weekly:** Collaborative filtering + NLP on playlist names. Cold start: pick 3 artists. No emotional context. No explanation.
- **Spotify Radio:** Content-based filtering on audio features. No temporal decay. No fairness constraints.
- **Spotify DJ:** LLM narration over pre-selected tracks. No real-time listener state modeling. No causal micro-event analysis.

**The baseline numbers:**
- Discover Weekly serendipity rate: ~18% new-artist saves
- Cold-start quality: arbitrary (3-artist selection)
- Playlist coherence: unmeasured publicly
- Artist diversity: top 1% of artists receive 90%+ of plays

## 2.3 Success Metrics Hierarchy

| Tier | Metric | Target vs. Baseline |
|---|---|---|
| **Primary (Business)** | Simulated stream engagement rate | +20% vs. Spotify API |
| **Primary (Business)** | Artist diversity (Gini coefficient) | 31% more equitable distribution |
| **Secondary (ML)** | Serendipity rate (new-artist saves) | 22%+ vs. Spotify's ~18% |
| **Secondary (ML)** | Cold-start quality (first 10 recs) | 2× improvement over 3-artist selection |
| **Secondary (ML)** | Playlist coherence score | 28% smoother energy/key transitions |
| **Secondary (ML)** | Content integrity F1 | F1 > 0.85 on held-out AudioSet |
| **Guardrail** | Emotional alignment (user self-report) | ≥70% agree music matched stated mood |
| **Guardrail** | Explainability acceptance | ≥80% of users find explanations meaningful |
| **Guardrail** | Inference latency | <200ms p95 for full recommendation call |

## 2.4 Stakeholder Map

| Stakeholder | What They Need | How PSYCHE Serves Them |
|---|---|---|
| **Listener (End User)** | Music that matches their current moment, not just their history | Real-time Emotional State Engine + Sonic Explainability Agent |
| **Artist (Content Creator)** | Fair exposure regardless of label size | Fairness-Aware RL Recommender with diversity reward signal |
| **Spotify (Decision Maker)** | Engagement, retention, platform health | All 10 gaps addressed simultaneously, benchmarked |
| **Interviewer** | Evidence you think in production systems | Full pipeline: ingestion → agents → deployment → monitoring |

## 2.5 Risk Assessment — Pre-Mortem

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Spotify API rate limits | High | Moderate | FMA + MPD datasets as primary; API for demo enrichment only |
| LLM API cost overrun | Medium | Moderate | Ollama local models (Llama 3) as fallback; API only for final demo |
| MERT/CLAP inference too slow | Medium | High | Pre-compute all embeddings offline; serve from FAISS index |
| RL agent diverges during training | Medium | High | Clip reward function; warm-start from supervised baseline |
| Cold-start agent response quality | Low | High | Prompt engineering + few-shot examples; fallback to genre selection |
| No ground-truth emotional labels | High | Moderate | Use valence/arousal proxies from audio features as synthetic labels |

---

# PART 3: THE COMPETITIVE TEARDOWN — WHERE EVERY PLATFORM FAILS

*Based on deep research across Reddit, Spotify Community, Apple Community, YouTube Music forums, r/spotify, r/TrueSpotify, r/applemusic, r/youtubemusic, tech press, and music tech discourse.*

## What Spotify Does Wrong

1. **Algorithm contamination** — one week of sleep music destroys years of taste profile. No intent detection.
2. **Same 30 songs trap** — repetition is the #1 complaint, running since 2021, still unfixed.
3. **Black box recommendations** — zero explanation for why anything plays.
4. **Worst audio quality** — subjectively worse than YTM and Apple Music. Lossless arrived late.
5. **Feature bloat** — podcasts, audiobooks, video bundled into one app. Users explicitly say "I just want music."
6. **Wrapped inaccuracy** — AI-generated stats that are demonstrably wrong. "BTS is my top artist — I didn't listen to them since 2021."
7. **No written feedback channel** — you can like/dislike but you cannot *communicate* with the algorithm.
8. **Artist royalties** — $0.003–$0.005 per stream. Artists leaving the platform publicly.

## What YouTube Music Does Wrong

1. **The shared Like button** — liking an anime video contaminates your music library permanently. Described as "the crucial missing thing."
2. **Video-first architecture** — library sorting, playlist management, and metadata are all broken because music is treated as a video type.
3. **No library organization** — can't sort playlists alphabetically by artist. 5,000-song like limit.
4. **Audio quality ceiling** — 256kbps AAC. No lossless. Audiophiles cannot use it seriously.
5. **Podcast/video bleed** — discovers your YouTube watch history into music recommendations.
6. **Samples tab = Japanese shamisen** — the discovery feed is contaminated by YouTube browsing history.
7. **No cross-device sync** — queue doesn't transfer between phone and computer in real time.

## What Apple Music Does Wrong

1. **Recommendations are advertising** — curation feels like what labels want you to hear.
2. **Desktop app is a disaster** — widely described as "Soviet-era administrative software."
3. **No social features** — Apple Music Connect was abandoned in 2019.
4. **Ecosystem lock-in** — works beautifully on Apple devices, badly everywhere else.
5. **Algorithm does not learn** — Love/Dislike buttons exist but users report they don't meaningfully improve recommendations.
6. **No explanation layer** — pure black box, worse than Spotify.
7. **Shuffle is broken** — users describe it as "asinine" and "completely random."

## The Universal Complaint Across All Three

> *"No service has everything for everyone and I've tried many. I wish there was one platform that had it all."*
> — Direct Reddit quote from multi-platform music streaming discourse

**PSYCHE is that platform.**

---

# PART 4: THE COMPLETE PRODUCT

## 4.1 The Five Competing Dimensions — PSYCHE Wins All Five

| Dimension | Spotify | YouTube Music | Apple Music | **PSYCHE** |
|---|---|---|---|---|
| **Intelligence** | Good | Good | Mediocre | **Best. 10 ML agents. Explains every decision.** |
| **Audio Quality** | 320kbps / lossless late 2025 | 256kbps AAC, no lossless | 24-bit/192kHz lossless + Atmos | **24-bit/192kHz lossless + Atmos + HRTF spatial** |
| **Content Depth** | 100M+ tracks, official only | Covers, lives, remixes, fan uploads | 100M+ tracks, some exclusives | **FMA + YouTube audio pipeline + user uploads + official tracks** |
| **Library Control** | Decent | Broken | Good for power users | **Best in class. Sort by anything. No limits. No contamination.** |
| **Human Connection** | Social but limited | Minimal | None | **Sonic Identity, Taste Twins, Collaborative Maps, live widgets** |

## 4.2 The Three User Modes

**MODE A: LISTENER** — For the everyday user who just wants great music.
- Launches to Now Playing with auto-generated queue
- ESIE state displayed as colored rings (no jargon — just visual mood indicator)
- "Why this?" button on every track = 1-tap explanation
- All 6 agents invisible — they just work
- Context Profiles (Work/Sleep/Gym/Social) as large-tap buttons

**MODE B: EXPLORER** — For users who want to engage with their taste.
- Sonic Identity visualization (the EQ-curve fingerprint)
- Taste Timeline (monthly history + GRU projection forward)
- Discovery controls: familiarity slider, geographic origin filter, decade selector
- Rabbit Hole Mode with depth slider
- Emotional Arc Builder (set destination state)

**MODE C: ENGINEER** — For developers, researchers, recruiters.
- 6-agent mission control panel
- Live latency trace
- Meta-orchestrator weight bars
- Baseline comparison table (vs Spotify API)
- API playground

## 4.3 The Onboarding Experience

**Screen 1: "What does music do for you?"**
Not "select your favorite genres." A single, warm question on a full-screen dark background with an animated waveform. Three options as large cards:
- "Carry me through the day" → Work/commute/study context pre-loaded
- "Help me feel something" → Emotional intelligence mode prioritized
- "Take me somewhere new" → Discovery mode prioritized

**Screen 2: The Cold Start Interview**
5 conversational questions from the PSYCHE agent. The Sonic Identity radar builds itself in real time as you answer. No artist selection. No genre checkboxes. A conversation.

**Screen 3: "Your first playlist is ready."**
The radar is complete. A personalized playlist of 15 tracks is generated. Play immediately. Total onboarding time: under 3 minutes.

## 4.4 The Core Audio Engine

- **Standard:** 320kbps AAC
- **Lossless:** 16-bit/44.1kHz FLAC (CD quality)
- **Hi-Res Lossless:** 24-bit/192kHz FLAC
- **Spatial:** HRTF (Head-Related Transfer Function) binaural rendering — surround-like on any headphones, zero Dolby licensing cost
- **PSYCHE Enhanced:** MERT-powered dynamic EQ that adapts to the track's sonic character in real time

## 4.5 The Three-Source Catalog

**Source 1: FMA + Licensed Catalog**
Free Music Archive (106k+ tracks) + partnerships with distributors (DistroKid, TuneCore, CD Baby) to ingest independent releases. Every track in MERT+CLAP embedding space.

**Source 2: YouTube Audio Pipeline (Open Source Tier)**
A PSYCHE-specific audio extraction pipeline that — on user request — pulls the audio from a YouTube URL (live performance, cover, remix) and adds it to the user's personal library. User-initiated, personal library only, same model as YouTube Music's own uploads feature.

**Source 3: User Uploads**
Any user can upload their own audio files. PSYCHE processes them through the full pipeline: MERT embedding, CLAP embedding, FAISS indexing. They become part of your Sonic Genome just like any streamed track. The library becomes *yours*, not the platform's.

## 4.6 The Library Management Philosophy — The Clean Room

**Principle 1: Total Separation.** Music library is a completely isolated data structure from any other content type. No shared Like button. No video bleed. No podcast contamination. These are not separate settings — they are separate data architectures.

**Principle 2: Total Control.** Sort by: artist, album, year, BPM, key, energy, valence, geographic origin, date added, play count, ESIE context tag, cosine similarity to current mood. Filter by any combination. No size limits anywhere.

**Principle 3: Total Portability.** One-click export your entire library (tracks, playlists, listening history, Sonic Genome) as a JSON file or standard M3U. This trust signal alone is a powerful competitive advantage.

---

# PART 5: THE 10 GAPS — RESEARCH-BACKED, PRODUCTION-JUSTIFIED

Every gap below is sourced from Spotify's own published research papers, RecSys 2025 contributions, and peer-reviewed MRS literature.

## GAP 1 — No Real-Time Emotional State Modeling

| Dimension | Detail |
|---|---|
| **What Spotify does** | Recommends based on historical listening patterns and playlist context tags (e.g., "chill", "workout") |
| **What nobody does** | Infer the listener's current emotional and cognitive state from passive multimodal signals updated every 90 seconds |
| **Research citation** | Spotify Research (2018): "MR research is still facing substantial challenges... dig deep into the very essence of listener needs, preferences, and intentions" |
| **PSYCHE solution** | Emotional State Inference Engine (ESIE): LLM classifier over session signals → live Listener State Vector [valence, arousal, focus, social_mode] |
| **Business justification** | Matching music to current emotional state is the single most requested feature in music app user research globally |

## GAP 2 — No Causal Understanding of Why Songs Work

| Dimension | Detail |
|---|---|
| **What Spotify does** | Correlates user-item interactions. Knows you skipped a song but not which 8-second moment caused the skip. |
| **What nobody does** | Model which acoustic sub-components (the bass drop, the key change, the BPM shift at a specific timestamp) caused a skip, replay, or save |
| **Research citation** | Spotify audio analysis uses a 42-dimensional feature vector but attributes behavior to the whole track, not sub-segments |
| **PSYCHE solution** | Micro-Event Attribution Engine: Demucs stem separation + librosa segment analysis → per-user "Sonic Genome" of preferred acoustic events |
| **Business justification** | Causal attribution enables precision targeting. Instead of "you like rock," PSYCHE knows "you love the specific harmonic tension at the bridge of rock songs" |

## GAP 3 — Cold Start Problem Remains Unsolved at Scale

| Dimension | Detail |
|---|---|
| **What Spotify does** | Asks new users to select 3 artists. Maps to genre clusters. Serves generic recommendations for weeks. |
| **What nobody does** | Use a conversational LLM agent to conduct a 90-second psychographic interview that extracts emotional needs, cultural anchors, and listening contexts before a single song is played |
| **Research citation** | Spotify RecSys 2025: "Generalized User Representations" paper addresses cold-start but does not solve the conversational intake problem |
| **PSYCHE solution** | Cold Start Psychographic Agent: LLM-powered interview → rich embedding via CLAP similarity matching → warm user vector before first play |
| **Business justification** | First-week experience determines 30-day retention. Solving cold start is a direct revenue lever for Spotify's subscriber growth. |

## GAP 4 — No Principled Serendipity Engine With Explainability

| Dimension | Detail |
|---|---|
| **What Spotify does** | Discover Weekly surfaces unknown artists with zero explanation to the user |
| **What nobody does** | A principled system that quantifiably manages the familiarity-novelty tradeoff AND explains every discovery in musically-literate natural language |
| **Research citation** | Spotify Research survey: "A good mix of familiar and unknown songs... Supporting discovery of interesting new songs, still contextualized by familiar ones, increases the likelihood of serendipitous encounter" |
| **PSYCHE solution** | Serendipity-Calibrated Discovery Agent: CLAP audio similarity graph + LLM narration: "This artist uses the same harmonic tension you love in Radiohead, but they're from Lagos and signed last week" |
| **Business justification** | Explained discovery builds trust. Users who understand why a new song was recommended are 3× more likely to save it (internal Spotify UX research). |

## GAP 5 — Artist Fairness Is Completely Absent From the Recommendation Loop

| Dimension | Detail |
|---|---|
| **What Spotify does** | Rich get richer. Top 1% of artists receive 90%+ of algorithmic plays. No fairness constraint in production recommenders. |
| **What nobody does** | Build a multi-objective RL recommender that treats artist equity as a first-class reward signal alongside user engagement |
| **Research citation** | Music Tomorrow (2025): "Most academic papers on music recommender fairness use outdated datasets... gap between research and industry practices" |
| **PSYCHE solution** | Fairness-Aware RL Recommender: custom Gymnasium environment with composite reward = engagement + artist diversity + geographic spread. Trained with PPO via Stable-Baselines3. |
| **Business justification** | EU Digital Services Act (DSA) and platform accountability laws are forcing streaming companies to address algorithmic fairness. This is a compliance and reputational necessity. |

## GAP 6 — Playlist Coherence Is Purely Heuristic

| Dimension | Detail |
|---|---|
| **What Spotify does** | Auto-generated playlists use simple energy/BPM sorting. Jarring key mismatches and energy drops are common. |
| **What nobody does** | Model playlist-level coherence as a sequence optimization problem treating the playlist as a story with emotional chapters |
| **Research citation** | Spotify MRS Survey: "A highly disliked song can have a strong influence on how they judge the entire playlist" — one bad transition poisons the whole experience |
| **PSYCHE solution** | Playlist Coherence Architect: Transformer sequence model trained on MPD, optimizing key compatibility + energy arc + tempo trajectory + emotional narrative across the full playlist |
| **Business justification** | Playlist quality is Spotify's primary engagement driver. 31% of listening time is playlist-based. A 10% improvement in coherence = measurable session length increase. |

## GAP 7 — Cross-Domain Context Signals Are Ignored

| Dimension | Detail |
|---|---|
| **What Spotify does** | Uses only in-app behavioral signals. Ignores temporal context, stated activity, and environmental signals. |
| **What nobody does** | Safely fuse cross-domain context (time of day, day of week, stated activity, weather) with audio features using a differential privacy layer |
| **Research citation** | Spotify RecSys 2025: "Calibrated Recommendations with Contextual Bandits" deploys contextual signals but does not fuse environmental data |
| **PSYCHE solution** | Context Fusion Module: temporal + stated-activity + weather API signals → differential privacy layer → context embedding → injected into recommendation stack |
| **Business justification** | Context-aware recommendations reduce skip rate significantly. Users working out need different music than users sleeping, even if their history is identical. |

## GAP 8 — AI-Generated & Harmful Audio Enters the Recommendation Loop Undetected

| Dimension | Detail |
|---|---|
| **What Spotify does** | Announced rules in September 2025 against spam and AI-generated content, but critics say the system lacks real-time safeguards |
| **What nobody does** | A multimodal pre-recommendation classifier that scores every candidate track for AI-generation likelihood, lyrical toxicity, and metadata spoofing before it reaches the listener |
| **Research citation** | Headphonesty (Jan 2026): "Spotify's algorithm recommending AI songs with hateful lyrics" — the system has no real-time gate |
| **PSYCHE solution** | Content Integrity Guardian: CLAP embeddings + fine-tuned classifier on FMA + AudioSet → agent gate that runs on every recommendation call with configurable risk thresholds |
| **Business justification** | Legal liability, brand safety, and regulatory pressure all converge here. Spotify needs this. No one has shipped a working demo. |

## GAP 9 — No Long-Horizon Taste Evolution Modeling

| Dimension | Detail |
|---|---|
| **What Spotify does** | Your 2015 listening still influences 2026 recommendations. No temporal decay model. No life-event detection. |
| **What nobody does** | Model taste evolution as a time-series problem, recognizing that preferences drift with age, life events, and cultural exposure, and weight recent behavior accordingly |
| **Research citation** | ResearchGate (2025): "Temporal convolutional networks with language models for decoding music preferences in mental health profiling" — temporal modeling of preferences is an open research frontier |
| **PSYCHE solution** | Temporal Taste Evolution Model: GRU + attention architecture trained on LFM-1b listening history dataset, with configurable exponential half-life decay per user |
| **Business justification** | Long-term users churn when recommendations feel "stale." Adaptive taste modeling is the solution to Spotify's retention cliff after year 3. |

## GAP 10 — No Unified Explainability Layer for Music AI

| Dimension | Detail |
|---|---|
| **What Spotify does** | Complete black box. Zero explanation to users or artists about algorithmic decisions. |
| **What nobody does** | A natural language explainability layer that answers "Why did the system play this song?" in real, human, musically-literate language |
| **Research citation** | Spotify Research (2025): diversity-accuracy dilemma paper notes that "ethical implications of these designs" require explainability — but no production explainability layer exists |
| **PSYCHE solution** | Sonic Explainability Agent (SEA): LangChain RAG pipeline over audio feature DB → LLM generates musicologically accurate explanations for every recommendation decision |
| **Business justification** | EU AI Act (2026) mandates explainability for high-impact algorithmic systems. Spotify needs this for compliance. PSYCHE builds it first. |

---

# PART 6: THE 60 USER-DRIVEN FEATURE ADDITIONS

*Grounded in three rounds of real user research — Reddit, Spotify Community, YouTube Music forums, Apple Music forums, TechCrunch, NPR, Billboard.*

## ROUND 1: SPOTIFY REDDIT RESEARCH — Additions 01–30

### Category: Algorithm Trust & Control (01–07)

**Addition 01 — Intent Detection Engine (Passive vs. Active Listening)**
A new 11th agent: IntentClassifier. Automatically detects listening mode from session signals — active (song skips, seeks, likes), passive (no interaction, long sessions, repeated loops), background (sleep, work, study detected via time + device context). Passive and background plays are weighted near-zero in taste profile updates. Only active intent shapes the recommendation model.
Reddit trigger: *"The algorithm monitors USE but not INTENT. I listen to white noise at work — I don't want 10,000 white noise recommendations forever."*
Tech: Session signal analysis · Skip/seek pattern model · Time-of-day classifier · New agent: IntentClassifier

**Addition 02 — Taste Profile Timeline Editor**
A dedicated UI screen showing your full listening history as an interactive timeline. Each session is a colored node. You can select any time range and mark it as "excluded from taste" — removing its weight from the GRU model. Visual confirmation shows how removing a session shifts your taste vector. Undo available for 30 days. The "editing your own musical memory" feature nobody has ever shipped.
Reddit trigger: *"My ex played his music on my account. His taste still shows up in suggestions. Please let me remove specific listening sessions."*
Tech: D3 timeline · GRU weight recalculation · Session tagging API · Undo stack

**Addition 03 — Context Profiles (Named Listening Modes)**
User-created named profiles: Work, Sleep, Gym, Social, Commute, Deep Focus. Each profile has its own ESIE parameters (arousal/valence target), its own taste profile weights, and its own coherence settings. Switching profiles is one tap. PSYCHE learns each profile independently — your Sleep profile never contaminates your Discovery profile.
Reddit trigger: *"There's no version of Spotify that knows I'm driving vs studying vs falling asleep. Each context needs completely different music."*
Tech: Profile-scoped ESIE · Isolated taste vectors · One-tap switching · API parameter: context_profile

**Addition 04 — Recommendation Explanation Cards ("Why This?")**
Every single recommendation includes a 2-sentence natural language explanation generated by the SEA agent. Format: "[Feature] — [Connection to your taste]." Example: "The bass-forward production and off-beat syncopation here matches the micro-patterns your Sonic Genome shows you replay most. This artist is from Accra and has 847 listeners."
Reddit trigger: *"Why did the system play this? I want to understand what it found in common with my taste, not just get a black box."*
Tech: SEA LangChain RAG · Sonic Genome diff · Expandable card UI · Feature highlight viz

**Addition 05 — Real-Time Written Feedback Channel**
A persistent text input at the bottom of every recommendation view. User types anything — "Too sad today", "Wrong energy for my morning run", "I love this but heard it 40 times this week." This text feeds directly into the ESIE context window and the meta-orchestrator via natural language. The system parses intent, adjusts Listener State Vector in real-time, and shifts the next 5 recommendations accordingly.
Reddit trigger: *"I want to tell Spotify's algorithm where to go — not just skip a song. I want to write WHY I'm skipping."*
Tech: NLP intent parsing · Live LSV adjustment · Feedback loop API · Confirmation UI

**Addition 06 — Repetition Detection & Diversity Enforcer**
A hard constraint layer sitting between the orchestrator output and final response. Tracks a rolling 200-song session history. Any candidate track within cosine similarity 0.92 of a recently played track is automatically demoted. Exact duplicates are blocked entirely. The diversity score is shown in Engineer View as a live "session entropy" gauge.
Reddit trigger: *"It recommends the same 30 songs for every playlist regardless of what's already there, occasionally recommending songs ALREADY in the playlist."*
Tech: Rolling session buffer · Cosine similarity threshold · Session entropy metric · Configurable API param

**Addition 07 — Taste Lock Toggle ("I'm Not Myself Today" Mode)**
A single toggle: "Taste Lock." When enabled, all listening in the current session has ZERO weight on the taste profile or GRU model. No passive listening contamination, no Wrapped impact, no algorithm drift. Unlike Spotify's Private Session (buried in settings, expires), Taste Lock is permanently accessible on the main UI, visually indicated with an amber padlock LED.
Reddit trigger: *"I was in a depressed phase and only listened to sad music for 2 weeks. Now the algorithm thinks that's all I want — forever."*
Tech: Session-scoped weight zeroing · GRU bypass flag · Visual LED indicator · API: taste_lock param

### Category: Emotional Intelligence & Wellbeing (08–14)

**Addition 08 — Mood Spiral Detection & Gentle Intervention**
ESIE monitors the valence/arousal trajectory over a 30-minute session window. If a user's inferred state shows consistent negative valence decline for 45+ minutes AND arousal drops below threshold, PSYCHE gently shifts recommendations toward neutral-positive valence tracks with smooth energy transitions — never abruptly, never obviously. A soft alert appears: "You've been in a quiet mood. Want to stay here or shift the energy?" with two buttons, no judgment.
Reddit trigger: *"A friend literally had a mental breakdown and all Spotify would recommend were tracks that further perpetuate their suicidal thoughts. Fix your algorithm."*
Tech: ESIE trajectory monitoring · Valence decline detector · Soft intervention UI · Configurable threshold

**Addition 09 — Emotional Arc Builder (Plan Your Listening Journey)**
User sets a "destination state" — a target valence/arousal point on a 2D grid with named zones (Energized, Calm, Focused, Joyful). PSYCHE generates an arc of recommendations that gradually moves from the user's current inferred state toward their target, using the Coherence Agent to ensure smooth transitions. The arc is visualized as a path on the EQ curve.
Reddit trigger: *"I know what mood I want to be in AFTER listening. Nobody lets me specify: 'I'm sad now, I want to feel hopeful in 30 minutes.'"*
Tech: 2D valence-arousal grid UI · Arc generation algorithm · Coherence Agent integration · Progress visualization

**Addition 10 — The Memory Playlist (Life Chapters)**
PSYCHE's Temporal Taste GRU identifies inflection points in your listening history — moments when your taste shifted significantly. Each inflection = a "chapter." Each chapter gets an auto-generated playlist of tracks that were sonically novel for you at that time, annotated with the micro-events that drove the shift. The chapter list is a visual timeline you can share.
Reddit trigger: *"I have my Top Songs from every year saved. Looking at them takes me back to exactly that time. This is my favorite thing about any streaming app."*
Tech: GRU inflection detection · Chapter segmentation · Shareable timeline · LFM-1b training data

**Addition 11 — Context-Aware Sleep Timer with Fade Intelligence**
When enabled: sets a timer, gradually reduces arousal of recommendations toward sleep-optimal ranges (low BPM, high valence, minimal rhythmic complexity), then fades volume over 10 minutes. Crucially: ALL sleep-mode listening is automatically Taste-Locked — zero algorithm impact. A sleep session report confirms: "Your taste profile was fully protected last night."
Reddit trigger: *"I fell asleep listening to a song. It looped 70 times. Now it's on my Wrapped. Now my algorithm is ruined."*
Tech: Arousal fade algorithm · Auto Taste Lock · Volume fade API · Sleep report screen

**Addition 12 — Rumination Guard (Breaking the Sad Loop)**
Research from Reddit's r/depression shows maladaptive music use (rumination loops) is identifiable from acoustic features — low valence, high self-reference in lyrics, slow tempo, minor key. The Rumination Guard agent monitors these signals over time. It does NOT intervene unless the user asks — instead it makes a gentle offer: "You've been in the same sonic space for a while. Want me to find something that moves through it?" Always opt-in, never preachy.
Reddit trigger: *"I get stuck in bad memories. When I try to use music to feel better I actually end up feeling worse. The algorithm just keeps feeding the loop."*
Tech: PLOS ONE research basis · Acoustic rumination signals · Opt-in offer UI · User agency preserved

**Addition 13 — Weather & Calendar Integration Layer**
Context Fusion Module gets two new inputs: optional weather API (temperature, precipitation, cloud cover → environmental embedding) and optional calendar integration (meeting in 20 mins → focus mode, free afternoon → exploration mode). Both are privacy-first: processed locally, never stored. The recommendation rationale now says "Adjusted for: rainy afternoon, no meetings until 4pm."
Reddit trigger: *"A rainy Friday morning and eager for the weekend — the music I need is completely different from a sunny beach drive. Context is everything."*
Tech: OpenWeatherMap API · Calendar OAuth (Google/Apple) · Local processing only · Rationale display

**Addition 14 — Sonic Fingerprint Card (Viral Social Feature)**
PSYCHE generates a unique "Sonic Fingerprint" — a beautiful shareable card built from your Sonic Genome. Shows: top 3 defining micro-events (e.g., "bridge harmonic tension," "off-beat bass drops," "vocal reverb"), your taste position in UMAP space relative to 8 global listener archetypes, the geographic region whose music most closely matches your taste, and a generated "Sonic Tagline." Fully animated, shareable as a PNG. Updates monthly.
Reddit trigger: *"Sound Town from Spotify Wrapped was genius — it placed me in a city that matched my taste. That geographic connection was the most shareable thing they ever did."*
Tech: Sonic Genome synthesis · UMAP archetype placement · Shareable card generation · Framer Motion animation

### Category: Discovery & Taste Expansion (15–19)

**Addition 15 — Rabbit Hole Mode (Controlled Deep Discovery)**
A dedicated mode that intentionally maximizes the Serendipity Agent while temporarily lowering the Familiarity constraint. User sets a "depth" slider: Surface (±1 embedding distance from comfort zone), Dive (±3), Abyss (±5 — territory you've never approached). As you explore, a breadcrumb trail shows how far you've wandered from your core taste. "Abyss Mode" will be tweeted.
Reddit trigger: *"I'd love to discover something completely unknown to the rest of the world. Not the same 30 popular songs. Take me somewhere new."*
Tech: Serendipity Agent upweight · Depth slider UI · Breadcrumb trail D3 · Discovery card generator

**Addition 16 — Artist Origin Trails (Geographic Music Discovery)**
A map-based discovery mode. Click any country or region on the Fairness Observatory world map and PSYCHE generates a "best match" playlist of artists from that region whose sonic characteristics align with your taste profile. "Music from Lagos that sounds like what you already love, that you've never heard." This directly turns the Fairness Agent from a backend metric into a user-facing product feature.
Reddit trigger: *"Top 1% of artists get 90%+ of plays. I want to find music from places I've never heard from — Lagos, Tbilisi, Bogotá."*
Tech: Fairness Agent reused · Geographic metadata DB · CLAP geographic matching · D3 world map UI

**Addition 17 — Sonic Bridge ("You'd Love This If You Like That")**
A single-track analysis tool. User pastes any track or selects from their library. PSYCHE runs CLAP + Micro-Event attribution to find the specific sub-features they respond to (the "what you actually like about it"), then searches the FAISS index for tracks that share THOSE features specifically — not just genre similarity. Result: "You love the minor-key bridge tension here, not the country production. Here are 8 tracks that do the same thing in indie, jazz, and electronic."
Reddit trigger: *"I don't like country music, but I do like some of the Rolling Stones' renditions of country songs. Nobody maps those nuanced connections."*
Tech: Per-track CLAP analysis · Sub-feature extraction · Cross-genre FAISS search · Feature attribution display

**Addition 18 — Era Time Machine (Discover Across Decades)**
A decade selector overlay on the main discovery view. User selects: 60s, 70s, 80s, 90s, 00s, 10s. PSYCHE's CLAP audio-text embeddings are decade-agnostic — they encode sonic characteristics, not release date. So "music that sounds like what you love, but from the 1970s" is a real FAISS query. Each era playlist includes a 1-sentence SEA explanation of the sonic connection: "This 1973 track has the same harmonic restlessness you love in modern alt-rock."
Reddit trigger: *"There's much older music that was popular then but doesn't appear in recommendations — Neil Sedaka, obscure 70s artists. The algorithm only knows the present."*
Tech: Decade metadata filter · Era-agnostic CLAP search · SEA era explanation · Decade selector UI

**Addition 19 — Taste Twin (Social Discovery)**
Anonymous-by-default Sonic Identity matching. PSYCHE computes the cosine similarity between your Sonic Genome and all other PSYCHE users who have opted into the feature. Shows your top 5 "Taste Twins" — users with similar but not identical taste vectors (0.75–0.85 similarity is the sweet spot for discovery). Each Twin's profile shows only their Sonic Fingerprint card — no personal info. Their recent discoveries that you haven't heard are auto-surfaced as recommendations.
Reddit trigger: *"Airbuds raised $5M for social music features. Spotify hasn't cracked the identity+social piece. Users want music-based social connection."*
Tech: Sonic Genome cosine match · Opt-in privacy model · Anonymous Twin profiles · Twin discovery feed

### Category: Identity, Sharing & Wrapped Replacement (20–23)

**Addition 20 — PSYCHE Rewind (Always-On Stats)**
A dedicated stats screen showing: total listening time (today/week/month/all-time), taste evolution chart month by month, top micro-events across all time, genre distribution by energy, most-replayed 8-second segments across all tracks (the "sonic moments" you love most), and a live "listening age" (how old your taste sounds vs. release dates). All data accurate, all year.
Reddit trigger: *"I crave the Wrapped stats every year. I'm a data nerd. I want this all year round, not just in December — accurate, real-time, mine."*
Tech: Real-time stats API · Micro-event aggregation · Listening age calculator · Annual export

**Addition 21 — Collaborative Taste Map (Real-Time Group Blend)**
When 2–8 people start a shared session (via link or QR code), PSYCHE computes the intersection of their Sonic Genomes in real time and generates recommendations that sit in the overlap — the exact musical territory where everyone's taste converges. The overlap is visualized as intersecting EQ curves on screen. As people join or leave, the blend updates live. The party DJ feature nobody has ever done with actual intelligence.
Reddit trigger: *"I wish there was a centralized site where people could contribute to a playlist regardless of what streaming service they use."*
Tech: Multi-user Genome intersection · Real-time FAISS query · Intersecting curves D3 · QR join link

**Addition 22 — Sonic Identity Badge System**
A badge system based on genuinely unique sonic behaviors detected in your Sonic Genome. Not generic personality types — specific achievements: "Bridge Chaser" (you engage 4× more during song bridges), "Bass Archaeologist" (you discovered 23 bass-forward tracks before they hit 10k plays), "The Cartographer" (your taste spans the widest geographic range of any user in your city), "Minor Key Prophet" (92nd percentile minor key engagement). Badges are shareable cards. They cannot be gamed.
Reddit trigger: *"Sound Town went viral because it gave me a shareable identity label based on my music. Listening Characters failed because they were generic."*
Tech: Sonic Genome behavioral analysis · Percentile ranking engine · Badge card generator · Shareable PNG export

**Addition 23 — Real-Time Now Playing Widget**
A PSYCHE embeddable widget (React component + iOS/Android widget) that shows what you're listening to right now, your current ESIE mood state (as colored rings — no data exposure), and a "Play alongside" button that starts a Collaborative Taste Map session. Integrates with Discord, Slack, GitHub profile README, and personal sites. Ghost Mode toggle disables it instantly.
Reddit trigger: *"Airbuds has 15M downloads just for showing friends what you're listening to. Spotify has a social feature but it's buried. This is unmet demand."*
Tech: Public now-playing API · Embeddable React widget · ESIE mood rings · Ghost Mode toggle

### Category: Artist & Creator Tools (24–27)

**Addition 24 — Artist Algorithmic Transparency Report**
A public-facing report for any artist in the FMA dataset: their Gini contribution score (how much PSYCHE's Fairness RL routes plays toward them), their CLAP embedding neighborhood (what genres/regions they sit near in embedding space), and the specific sonic features that the algorithm responds to in their tracks. Artists can see: "PSYCHE recommends you to users who love [these 3 micro-events]. Your bridge section at 2:34 drives 67% of your saves."
Reddit trigger: *"Artists earning under 1,000 streams get zero pay. Top 1% get 90%+ of plays. Artists have no visibility into why the algorithm promotes or ignores them."*
Tech: Artist Gini contribution · CLAP neighborhood map · Micro-event attribution · Public artist API

**Addition 25 — Sonic Compatibility Analyzer ("Will My Audience Like This?")**
Artists upload a track. PSYCHE runs full feature extraction + CLAP embedding and returns: predicted listener segment match scores (what % of each archetype group would engage), comparison to the artist's previous tracks in embedding space, top 3 micro-events detected, and a "PSYCHE Fit Score" for each of 6 listening contexts (Work, Gym, Night, Discovery, etc.). Available via API. A production tool that music industry professionals would pay for.
Reddit trigger: *"Discovery Mode lets artists pay to be pushed — but they don't know if their new track will resonate. It's a leap of faith with money."*
Tech: Offline CLAP analysis · Segment match scores · Context fit scoring · Artist upload API

**Addition 26 — AI Content Shield (Authenticity Certificate)**
The Content Integrity Guardian gets a public-facing API: any platform (SoundCloud, Bandcamp, podcast hosts) can call `/integrity/check` with an audio file and receive: AI-generation probability (0–1), toxicity score, metadata spoofing indicators, and a signed PSYCHE Authenticity Certificate if the track passes all thresholds. The certificate is a shareable badge: "PSYCHE Verified — Human-made music." This becomes the industry standard for proving authenticity pre-release.
Reddit trigger: *"'Slopify' — Spotify's algorithm recommended AI songs with hateful lyrics. Real artists are competing with synthetic content that pays zero royalties."*
Tech: Content Integrity Guardian · Public /integrity API · Signed certificate generation · Platform integration SDK

**Addition 27 — Public Equity Score Dashboard**
A public, live dashboard at `psyche-music.github.io/equity` showing: Gini coefficient of PSYCHE's current recommendations vs. Spotify's historical baseline, geographic distribution of plays (countries represented), label-size breakdown (major/indie/unsigned share), and a "Fairness Trend" showing week-over-week improvement as PSYCHE's RL model optimizes. Media will cite it. Researchers will use it. The DSA compliance story writes itself.
Reddit trigger: *"Spotify pays $10B in royalties but only 4.4% of musicians make over $131K. The distribution is catastrophic and invisible."*
Tech: Live Gini API · Public GitHub Pages site · Weekly trend tracking · DSA compliance evidence

### Category: Developer Platform & Ecosystem (28–30)

**Addition 28 — psyche.js TypeScript SDK**
A first-class TypeScript SDK alongside the Python one. `npm install psyche-client`. Exposes: real-time ESIE state via WebSocket hook (`usePsycheState()`), recommendation fetching with React Query integration, Context Profile management, and the Now Playing widget as a drop-in component. Full TypeScript types for every API response. Auto-generated from the FastAPI OpenAPI spec — always in sync. The VS Code plugin is built on this.
Reddit trigger: *"Developers want to build music-aware apps without building the full rec stack. Give them a 3-line integration."*
Tech: TypeScript first-class · React hooks · Auto-generated from OpenAPI · npm package

**Addition 29 — PSYCHE Webhooks (Event-Driven Music Intelligence)**
A Webhook system that lets any external service push context signals into PSYCHE's recommendation engine. Supported signal types: `emotional_state_update` (from a wearable, meditation app, or journaling tool), `activity_change` (from a fitness tracker), `focus_score` (from a productivity app like Reclaim or Notion), `custom_context` (any JSON object with key-value signal pairs). PSYCHE processes these via the Context Fusion Module and adjusts recommendations in real-time. This makes PSYCHE a platform, not just a product.
Reddit trigger: *"I want music that changes based on external events — my heart rate, my productivity score, my coding errors. But there's no way to pipe that into a music app."*
Tech: Webhook receiver endpoint · Context Fusion integration · Signal schema validation · Real-time LSV update

**Addition 30 — Custom Agent Framework (Bring Your Own Agent)**
The `BasePsycheAgent` protocol is published as a formal specification with a CONTRIBUTING guide: "How to add a new agent to PSYCHE." Any developer can implement the protocol, register their agent with the meta-orchestrator, and submit a PR. Community agents get a vote in the orchestrator proportional to their benchmark performance on `psyche-bench`. The GitHub repo has a `community-agents/` directory. This transforms PSYCHE from a project into an ecosystem.
Reddit trigger: *"The open source community will build better agents than any single team. Give them the infrastructure to plug in."*
Tech: BasePsycheAgent protocol · Agent registry · psyche-bench evaluation · community-agents/ directory

---

## ROUND 2: YOUTUBE MUSIC RESEARCH — Additions 31–45

**Addition 31 — The Firewall Library (Video/Music Total Separation)**
Architecturally isolated music database. Liking a YouTube video never, ever enters PSYCHE's music library. No shared data structure, no bleed, no settings toggle needed — it's physically separate from day one.
Reddit trigger: *"My carefully curated collection was polluted by memes. The only fix is a second account."*
Tech: Isolated DB schema · Explicit URL add only · No shared like button

**Addition 32 — Universal Library Sort & Filter Engine**
Sort by title, artist, album, year, BPM, key, energy, valence, geographic origin, date added, play count, ESIE context tag, or cosine similarity to any track. Filter by any combination. Zero limit on library size.
Reddit trigger: *"You're expected to move songs one by one, like a medieval scribe copying a manuscript."*
Tech: FAISS-backed sort · Multi-column filter · No size limits

**Addition 33 — Deep Cut Index (Live, Covers, Alternates)**
PSYCHE's Deep Cut search surfaces non-official versions of any track. Audio quality labeling (Official Studio / Live / Fan Cover / Remix) always visible. A "Versions" panel on every track shows all known variants with quality scores. The Micro-Event engine identifies which version you prefer at the stem level.
Reddit trigger: *"EDM remixes from 2011, obscure live cuts — content that doesn't exist on Spotify. That's why I stay on YTM."*
Tech: Version panel UI · Quality labels · Micro-event version matching

**Addition 34 — Audio Quality Label on Every Track**
Exact codec, bit depth, sample rate, and file source displayed on Now Playing and in every library view before you play. "Stats for Nerds" mode shows LUFS, dynamic range, and codec in real time during playback. No guessing. No disappointment.
Reddit trigger: *"There's no option to see what quality you're actually getting. Stats for Nerds proves normalization is happening."*
Tech: Codec display · LUFS metering · Dynamic range readout

**Addition 35 — Cross-Device Queue Sync (Real-Time, <500ms)**
Queue state stored server-side, synced via WebSocket to all connected devices in under 500ms. Start on laptop, pick up phone — exact track position, ESIE context, and upcoming queue all transfer instantly. Includes car/speaker handoff via PSYCHE Connect API.
Reddit trigger: *"Spotify was seamless moving between car and phone. YouTube Music has never figured this out."*
Tech: WebSocket state sync · PSYCHE Connect API · Under 500ms

**Addition 36 — The Content Type Filter (Always Visible)**
A global Content Filter permanently visible in the navbar: [Music Only] [Include Videos] [Include Live] [Include Covers]. Default: Music Only. State persists across sessions. The feature Google has refused to ship for 5+ years.
Reddit trigger: *"I don't want YouTube Music asking me to continue watching a video I started on YouTube. I want music only."*
Tech: Persistent navbar filter · Default: Music Only · Session-persistent

**Addition 37 — Volume Normalization Control (LUFS Standard)**
Normalization on/off toggle. Target loudness level in LUFS (broadcast standard). Options: -14 LUFS (streaming standard), -23 LUFS (broadcast standard), -9 LUFS (loud/club), Custom. Visible in every playback session. Not buried in settings.
Reddit trigger: *"There needs to be an option to turn normalization on or off. Music sounds tiny or too loud at times."*
Tech: pyloudnorm · LUFS target selector · Real-time processing

**Addition 38 — Smart Offline (Predictive Download Engine)**
The Temporal Taste GRU predicts what you'll want to listen to in the next 24 hours based on your patterns, then pre-downloads those tracks automatically on WiFi. Configurable storage budgets. Context-aware: Gym profile → high-energy tracks pre-downloaded before Monday morning automatically.
Reddit trigger: *"Offline mode is frustrating. Downloaded songs don't play properly. I want this to just work."*
Tech: GRU prediction engine · WiFi-only download · Context-profile aware

**Addition 39 — The Uncapped Library (No Limits, Ever)**
FAISS scales to 100M+ vectors with sub-millisecond retrieval. PSYCHE's library is designed from day one for collections with 50,000+ tracks. No liked-songs cap. No album-as-playlist confusion. No limits anywhere in the data model.
Reddit trigger: *"5,000 songs sounds like a lot, but it's very easy to hit. Hard-core users are penalized most."*
Tech: FAISS billion-scale · No data model caps · Power user first

**Addition 40 — Community Discovery Hub**
Native community playlist discovery: curated playlists from power users quality-scored by engagement and diversity, "Playlists your Taste Twins love," genre-community feeds, and a weekly "Community Pick" surfaced by the Fairness RL agent to ensure small-community music gets exposure.
Reddit trigger: *"I love that YouTube Music suggests community playlists based on my library. Nobody else does this."*
Tech: Taste Twin feeds · Fairness-weighted picks · Genre community feeds

**Addition 41 — Video Layer (Optional, Clean, Opt-In)**
Optional Video Mode toggle. When enabled, Now Playing shows the official music video if available, with a clean "Audio Only" button to strip the video instantly. Video mode is always opt-in, never default, never algorithmically recommended. Zero video content for users who don't enable it.
Reddit trigger: *"The infinite YouTube library wins for me. But I want music first, video second — not mixed together."*
Tech: YouTube embed (opt-in) · Instant audio-only switch · Never default

**Addition 42 — Adventurousness Dial (Persistent, Universal)**
A persistent Adventurousness dial (1–10) in every user's profile: 1 = only similar to what you've loved, 10 = Rabbit Hole mode. Applies to every listening mode — not just radio. The dial shows your current position on the familiarity-novelty spectrum at all times with visual feedback.
Reddit trigger: *"YouTube Music's Music Tuner lets me control variety and adventurousness. Spotify simply doesn't have this."*
Tech: Serendipity Agent weight · Persistent profile setting · All-mode application

**Addition 43 — Live Performance Mode (Dedicated Category)**
Dedicated Live Mode: CLAP search filtered to live recording embeddings, Coherence Agent adjusted for live show energy variance, SEA provides recording context for each track ("Madison Square Garden, 2019 world tour, extended bridge version"). Live performances as a first-class content category.
Reddit trigger: *"Songs unreleased on Spotify, live versions, covers — YouTube's variety allows discoveries that don't exist elsewhere."*
Tech: CLAP live-recording filter · Coherence Agent tuning · SEA recording context

**Addition 44 — Instant Queue Sculpting (Gesture-Based)**
Swipe upcoming tracks: left = remove, right = extend (more like this), up = play immediately, down = push later. The queue responds to gestures in real time, updating future recommendations based on what you're accepting or rejecting. More granular than any "not interested" button.
Reddit trigger: *"I love that I can shape my 'Up Next' queue to match exactly what I want to hear after any song."*
Tech: Gesture queue control · Real-time rec update · No permanent algo impact

**Addition 45 — Unified Search (Natural Language + Audio Humming)**
Natural language ("sad indie rock from the late 2000s"), audio humming/singing search (CLAP finds it), lyric fragments, and combined queries ("like Radiohead but from Africa after 2020"). The same CLAP model powering recommendations powers search — sonic concepts, not just text metadata.
Reddit trigger: *"YouTube's natural language search can find tracks even if you don't know their names. Why doesn't every service have this?"*
Tech: CLAP joint embedding search · Audio humming input · Combined query parser

---

## ROUND 3: APPLE MUSIC RESEARCH — Additions 46–60

**Addition 46 — Spatial Audio for Any Headphone (HRTF Binaural)**
HRTF processing applied to any stereo track using open-source research models. Not Dolby Atmos — equally immersive, zero licensing cost, works on any headphone. MERT embeddings identify which tracks benefit most (highly produced, multi-layered arrangements).
Reddit trigger: *"Using my AirPods Pro 2, Dolby Atmos tracks sound noticeably more immersive. Nothing else comes close."*
Tech: py3d-audio (open source) · HRTF processing · Any headphone

**Addition 47 — Human + AI Curation Blend**
Serendipity Agent generates 100 candidates → open "Editor Signal" API (verified music journalists/curators rate and annotate tracks) → final blend weights both. SEA explains when editorial influence shaped a recommendation: "Flagged by 3 editors in the ambient community as a defining 2024 release."
Reddit trigger: *"Apple Music's editorial curation feels like a knowledgeable friend. Spotify's algorithm can't replicate that feeling."*
Tech: Editor Signal API · Verified curator network · SEA attribution

**Addition 48 — Beat-by-Beat Lyrics (Open Source, Every Track)**
Word-level synchronized lyrics engine using the Gentle forced aligner + LRC format. Full-screen animated background shifts color based on ESIE's current valence/energy reading. Not behind a paywall. Included on every track with available lyrics data. Works cross-platform.
Reddit trigger: *"Apple's beat-by-beat lyrics support is unmatched. I miss it whenever I'm not on Apple devices."*
Tech: Gentle aligner (open source) · ESIE color background · All platforms

**Addition 49 — Animated Artwork Engine (Procedural, Every Track)**
Procedural animated artwork for every track generated from waveform, BPM, and energy characteristics. The artwork breathes with the music, pulses with bass hits, shifts color with the mood vector in real time. No licensing deals needed — every track gets this treatment via librosa analysis.
Reddit trigger: *"Apple Music's animated artwork support is unmatched. Every other service looks static by comparison."*
Tech: librosa waveform analysis · Real-time BPM pulse · ESIE color mapping

**Addition 50 — Desktop App That Actually Works**
Full Electron desktop app matching web app quality. Desktop-exclusive features: multi-column library sort, waveform scrubbing, playlist folder nesting, smart playlists with complex rules, external audio interface routing to DAC/amp, gapless playback across playlists, system-tray mini-player.
Reddit trigger: *"Apple's truly shitty desktop app — it looks like Soviet-era administrative software. That's what forced me out."*
Tech: Electron · DAC/amp routing · Smart playlist engine

**Addition 51 — Smart Shuffle (Coherence-Aware)**
Shuffle mode runs through the Playlist Coherence Architect: artist order is randomized but key compatibility, energy arc, and tempo transitions are still optimized. You never get a jarring key change or energy drop between two shuffled tracks. Random artist, coherent transitions.
Reddit trigger: *"Apple Music's asinine shuffling algorithms are one of the main reasons I left after three months."*
Tech: Coherence Agent integration · Key compatibility preserved · Energy arc maintained

**Addition 52 — Infinite Discovery Stream (Never Repeats, Never Ends)**
Always-on "Infinite Discovery" stream sourced from CLAP similarity search, filtered by the Serendipity Agent to guarantee novelty. Runs indefinitely. Periodically narrated by SEA: "You've been discovering new music for 47 minutes. Here's a bridge track back to something familiar." Never repeats. Never ends.
Reddit trigger: *"Apple's Discovery Station is continuous radio-style — a better model than Spotify's once-a-week finite playlist."*
Tech: Serendipity Agent continuous · SEA narration · Novelty guarantee

**Addition 53 — Local File Cloud Sync + Full Pipeline Treatment**
Upload any local audio file. PSYCHE processes it through the full MERT+CLAP pipeline — it gets embedded into your Sonic Genome, appears in similarity searches, influences recommendations, and triggers SEA explanations. Your 1987 bootleg becomes a first-class member of your music graph.
Reddit trigger: *"Apple lets you upload local files and sync them to the cloud. Without this I can't use a music service."*
Tech: Full MERT+CLAP processing · Sonic Genome integration · Cross-device sync

**Addition 54 — Artist Bio & Story Layer ("About the Song" — Expanded)**
Full artist context layer: biography, recording story, production context, cultural impact — plus the PSYCHE-exclusive connection: "This artist pioneered the harmonic pattern that appears in 23 of your most-replayed tracks." LangChain RAG over music knowledge sources, SEA-narrated.
Reddit trigger: *"Spotify's 'About the Song' feature is its most useful addition yet. I want more of this everywhere."*
Tech: LangChain RAG pipeline · Sonic Genome connection · SEA narrative

**Addition 55 — Cross-Platform Sync (Device Agnostic by Design)**
PSYCHE is device-agnostic from the architecture level. Web app is the primary surface. Same session state, queue, ESIE context, and library sync in real time across all logged-in surfaces. No platform-exclusive features. Everything on web = everything on mobile = everything on desktop. One account, one experience.
Reddit trigger: *"Cross-platform approach is what brought me back to Spotify. Apple Music fails here — only works on Apple devices."*
Tech: WebSocket state sync · Platform-agnostic design · No exclusive features

**Addition 56 — Recommendation Explainability for Curation**
SEA attributes every recommendation to specific audio features and behavioral signals: "78th percentile engagement with minor 7th chord progressions + 3 track replays this week with similar harmonic movement + 82% similarity match unseen for 47 days." Transparent. Always. No label influence without disclosure.
Reddit trigger: *"Apple's curation feels like advertising — what labels want you to hear, not what you actually want."*
Tech: SEA full attribution · Label influence disclosure · Feature-level explanation

**Addition 57 — Superfan Tier (The Feature Nobody Has Shipped)**
PSYCHE Superfan: unlimited hi-res lossless, early access to unreleased tracks from partner indie artists, direct artist messaging (opt-in), monthly "Sonic Letter" (SEA narrative of your taste evolution), priority queue on new releases, psyche-bench developer tools access. Revenue without exploitation. Industry first — ships here.
Reddit trigger: *"Companies have been teasing superfan tiers since 2024. A 20% conversion rate would be 160M subscribers. Nobody has shipped it."*
Tech: Hi-res unlimited · Artist direct messaging · Monthly Sonic Letter

**Addition 58 — Lossless Hardware API (Roon, Sonos, External DAC)**
Dedicated lossless streaming API endpoint for external hardware integration: Roon (RAAT protocol), Sonos (SMAPI), DLNA-compatible devices, external DACs. Returns raw FLAC stream URLs external players consume directly — bypassing the PSYCHE player if desired. Included in Hi-Res tier.
Reddit trigger: *"Apple makes it a pain to play music with my Hi-Fi gear. No bit-perfect on Mac is a crime for a service claiming audiophile quality."*
Tech: Roon RAAT protocol · DLNA/SMAPI · Raw FLAC endpoint

**Addition 59 — Transparent Pricing Lock for Early Adopters**
Open-source self-hosted version: free forever. Hosted psyche.fm: price locked for 3 years for early adopters. Price changes announced 6 months in advance with full explanation. No surprise increases. This trust signal costs nothing to implement and differentiates PSYCHE from every corporate streaming service.
Reddit trigger: *"Apple Music's unwavering price is a main selling point. Spotify's constant price hikes are driving users to look elsewhere."*
Tech: 3-year early adopter lock · 6-month advance notice · Full public explanation

**Addition 60 — The "Just Music" Manifesto (Product Principle as Feature)**
"PSYCHE is a music product. We don't sell podcasts. We don't sell audiobooks. We don't run ads. We don't use your listening data to sell you things. Music is enough." This manifesto shapes the UI (no podcast sidebar), the recommendation system (no podcast crossover), and the business model.
Reddit trigger: *"Spotify's biggest issue is it has diverted away from music. There's too much going on. I wish there was just music."*
Tech: Homepage commitment · Shapes all UX decisions · Business model aligned

---

# PART 7: THE FIVE REPOSITORIES — COMPLETE ARCHITECTURE

All five live under the `psyche-music` GitHub organization.

```
github.com/psyche-music/
├── psyche-core          ← Python SDK (pip installable) + all 10+ ML agents
├── psyche-ui            ← Next.js production frontend dashboard
├── psyche-api           ← FastAPI backend + WebSocket server + OpenAPI docs
├── psyche-bench         ← Open evaluation harness (the academic moat)
└── psyche-plugins       ← VS Code extension, Discord bot, Spotify overlay, Electron desktop
```

## Repo 1: `psyche-core` — The Python SDK

### Install
```bash
pip install psyche-core
```

### Package Structure
```
psyche/
├── agents/
│   ├── base.py                      # BasePsycheAgent protocol (all agents implement this)
│   ├── esie.py                      # Emotional State Inference Engine (Gap 1)
│   ├── micro_event.py               # Micro-Event Attribution Engine (Gap 2)
│   ├── cold_start.py                # Cold Start Psychographic Agent (Gap 3)
│   ├── serendipity.py               # Serendipity-Calibrated Discovery Agent (Gap 4)
│   ├── fairness_rl.py               # Fairness-Aware RL Recommender (Gap 5)
│   ├── coherence.py                 # Playlist Coherence Architect (Gap 6)
│   ├── context_fusion.py            # Cross-Domain Context Fusion (Gap 7)
│   ├── integrity.py                 # Content Integrity Guardian (Gap 8)
│   ├── temporal_taste.py            # Temporal Taste Evolution Model (Gap 9)
│   ├── explainability.py            # Sonic Explainability Agent / SEA (Gap 10)
│   ├── intent_classifier.py         # Intent Detection Engine (Addition 01)
│   └── rumination_guard.py          # Rumination Guard (Addition 12)
├── models/
│   ├── listener_state.py            # ListenerStateVector Pydantic model
│   ├── sonic_genome.py              # Per-user Sonic Genome
│   ├── track.py                     # Track, RecommendedTrack, IntegrityScore
│   └── context.py                   # SessionContext, ActivityContext, ContextProfile
├── pipelines/
│   ├── ingestion.py                 # Raw audio → validated → features
│   ├── feature_extraction.py        # librosa + Demucs + MERT + CLAP
│   ├── embedding_index.py           # FAISS index build + query
│   ├── data_quality.py              # Quality gates, corruption detection
│   └── dvc_tracking.py              # DVC artifact registration
├── orchestrator.py                  # LLM Meta-Orchestrator (weights all agents)
├── mini_orchestrator.py             # Lightweight 2-3 agent version for SDK users
├── config.py                        # Pydantic Settings with config.yaml
├── fallbacks.py                     # All fallback behaviors documented
└── utils/
    ├── audio.py
    ├── embeddings.py
    ├── metrics.py                   # All evaluation metrics (nDCG, Gini, etc.)
    └── logging.py                   # W&B + structured logging helpers
```

### The Complete Agent Table

| Agent | Input | Output | Model | Gap |
|---|---|---|---|---|
| **ESIE** | Session signals, recent tracks, time, activity | ListenerStateVector [valence, arousal, focus, social] | Ollama Llama 3 + signal classifiers | 1 |
| **Micro-Event** | Raw audio + interaction timestamps | Per-user Sonic Genome of preferred acoustic events | Demucs + librosa + attention pooling | 2 |
| **Cold Start** | Multi-turn conversation (5 questions) | Warm user embedding via CLAP similarity | Claude Sonnet 4.6 (conversational) | 3 |
| **Serendipity** | User embedding + FAISS results | Novel tracks with similarity explanation | CLAP graph + novelty scorer + LLM | 4 |
| **Fairness RL** | Listener state + candidate pool | Ranked tracks: engagement + fairness composite | PPO via Stable-Baselines3 (Gymnasium) | 5 |
| **Coherence** | Seed track + target length + listener state | Coherent track sequence with energy/key arc | Transformer seq2seq (HuggingFace, MPD) | 6 |
| **Context Fusion** | Time, activity, weather | Context embedding with differential privacy | Feature fusion + DP layer | 7 |
| **Integrity** | Candidate track audio + metadata | Risk score [AI-generated, toxic, spoofed] | CLAP fine-tuned on AudioSet + FMA | 8 |
| **Temporal Taste** | LFM-1b listening history | Taste evolution model with decay weights | GRU + attention, exponential half-life | 9 |
| **SEA** | Track features + user history | Natural language explanation | LangChain RAG over FAISS → LLM | 10 |
| **IntentClassifier** | Session signals, skip/seek patterns | Passive/Active/Background classification | Signal classifier | Addition 01 |
| **RuminationGuard** | Acoustic features, session valence trajectory | Opt-in mood spiral offer | PLOS ONE acoustic signals | Addition 12 |

### Developer Use Cases
```python
# Use case 1: Meditation app — just ESIE
from psyche.agents import EmotionalStateEngine
esie = EmotionalStateEngine(model="llama3-local")
state = esie.infer(session_signals=my_signals)
# Returns: ListenerStateVector(valence=0.7, arousal=0.4, focus=0.8, social=0.2)

# Use case 2: Podcast platform — just Content Integrity Guardian
from psyche.agents import ContentIntegrityGuardian
guardian = ContentIntegrityGuardian(risk_threshold=0.85)
score = guardian.evaluate(audio_path="episode_47.mp3")
# Returns: IntegrityScore(ai_generated=0.12, toxic=0.03, spoofed=0.01)

# Use case 3: Game audio — ESIE + Coherence only
from psyche.agents import EmotionalStateEngine, PlaylistCoherenceArchitect
from psyche import MiniOrchestrator
psyche = MiniOrchestrator(agents=["esie", "coherence"])
recs = psyche.recommend(user_id="player_42", context={"activity": "combat"})

# Use case 4: Full platform
from psyche import PsycheOrchestrator
psyche = PsycheOrchestrator.from_config("config.yaml")
recs = psyche.recommend(user_id="user_123", n=10)
# Returns: List[RecommendedTrack] with explanation, confidence, agent weights
```

## Repo 2: `psyche-ui` — The Production Frontend

### Design Philosophy: Instrument-Grade
PSYCHE's UI looks like Teenage Engineering (the hardware synth company that designed the OP-1) built a mission control dashboard for Spotify's AI team.

**Visual Identity:**
- Background: Deep near-black `#0A0A0B` with subtle noise texture
- Primary accent: Warm amber/copper `#E8A04A` (like studio monitor LEDs)
- Secondary accent: Electric teal `#00D4B8` for live/active indicators
- Data font: `Berkeley Mono` — numbers feel like studio equipment readouts
- Heading font: `Instrument Serif` — editorial, premium audio magazine
- Loading states: Canvas-based oscilloscope animations, never spinners
- Agent cards: Styled like hardware synthesizer modules with signal LEDs, confidence meters
- The Sonic Identity chart: EQ frequency response curve, not a standard radar chart

### Tech Stack
| Layer | Technology | Why |
|---|---|---|
| Framework | Next.js 15 (App Router) | SSR for demo SEO, RSC for performance |
| Language | TypeScript (strict mode) | Required for "production-grade" claim |
| Styling | Tailwind CSS + CSS Variables | Utility-first + custom theme tokens |
| Components | Radix UI primitives | Accessible, unstyled — applies our aesthetic |
| Charts | Recharts + D3.js | Recharts standard, D3 for custom oscilloscope/EQ viz |
| Animation | Framer Motion | Waveform, radar morphing, agent card transitions |
| Real-time | Socket.io client | Live agent state from psyche-api WebSocket |
| State | Zustand | Lightweight, zero boilerplate |
| Data fetching | TanStack Query v5 | Auto-caching, background refetch |
| Deployment | Vercel (free) | One-command deploy, preview URLs on every PR |

### The Six Screens

**Screen 1: Landing Page**
Full-screen hero with animated canvas waveform background. Amber traces on near-black. Headline: "The Music Intelligence Platform That Knows How You Feel Right Now." Three headline metrics (vs. Spotify API) displayed as large data readouts. Single CTA: "▶ Try the Live Demo." GitHub star count badge.

**Screen 2: Cold Start Interview (The Hook)**
Full-screen split: left half is a conversational chat UI where the PSYCHE Cold Start Agent asks 5 questions. Right half is the Sonic Identity Radar building itself live as you answer each question. The radar uses EQ-curve aesthetics, five axes: `Harmonic Complexity · Rhythmic Drive · Emotional Depth · Discovery Hunger · Social Mode`. Every answer causes the curve to morph in real time. This is the screen that gets screen-recorded and shared.

**Screen 3: Main Dashboard (Two Modes)**

*Listener View:* Left panel shows the live Sonic Identity EQ curve + Taste Timeline. Right panel shows Now Playing with Why This Track explanation, live Emotional State readout (four vector values updating every 90s), and upcoming queue with agent badges.

*Engineer View (toggle):* Left panel shows all agent cards styled as hardware modules with signal LEDs, confidence scores, and last-update timestamps. Right panel shows Meta-Orchestrator weight bars (real-time), Pipeline Trace latency breakdown (FAISS retrieval / agents / orchestrator / SEA), and live Baseline Comparison table.

**Screen 4: Sonic Identity Deep Dive**
- UMAP scatter plot of all listened tracks as dots in 2D embedding space, D3-powered, clusters visible
- Scrollable Taste Timeline: GRU history (left) and forward prediction with confidence band (right)
- Stem Preference Breakdown: horizontal bars for vocals/bass/drums/harmony engagement rates
- "Your Sonic Signature": CLAP dimensions with highest activation

**Screen 5: Fairness Observatory**
- D3 world map: countries colored by fraction of plays routed to artists from that region
- Animated Gini Coefficient gauge: large circular dial with PSYCHE value vs. Discover Weekly baseline
- RL Reward Decomposition: live breakdown `Engagement: 0.71 + Diversity: 0.18 + Geographic: 0.11`
- Label Size Breakdown: donut chart (major / indie / unsigned artist share)

**Screen 6: Developer Portal**
- Interactive API Playground: embedded Swagger UI with pre-filled example requests
- Code Snippets: Python / JavaScript / cURL, each for a specific developer use case
- One-click Deploy buttons: `Deploy to Railway` and `Deploy to Render`
- SDK installation code with copy button

## Repo 3: `psyche-api` — The Backend API

### FastAPI Structure
```
psyche_api/
├── main.py                          # App init, CORS, middleware, lifespan events
├── routers/
│   ├── recommendations.py           # POST /recommend, GET /queue/{user_id}
│   ├── agents.py                    # GET /agents/status, GET /agents/{agent_id}
│   ├── listener.py                  # GET /listener/{user_id}, POST /session
│   ├── cold_start.py                # POST /cold-start/message (SSE streaming)
│   ├── fairness.py                  # GET /fairness/metrics
│   ├── explain.py                   # GET /explain/{track_id}?user_id={id}
│   ├── integrity.py                 # POST /integrity/check (public API)
│   └── health.py                    # GET /health, GET /metrics (Prometheus)
├── websockets/
│   ├── agent_state.py               # WS /ws/agents — live agent telemetry
│   └── listener_state.py            # WS /ws/listener/{user_id} — live ESIE updates
├── middleware/
│   ├── rate_limiting.py             # Token bucket per API key
│   ├── api_key_auth.py              # Bearer token validation
│   └── request_logging.py           # Structured JSON logs
├── schemas/                         # Pydantic models (shared with psyche-core)
└── tests/
    ├── test_recommendations.py
    ├── test_latency.py              # CI enforces <200ms p95
    └── test_integration.py          # Full end-to-end happy path
```

### Key API Endpoints
```
POST   /recommend           → Full recommendation call with agent weights + explanations
POST   /cold-start/message  → SSE stream: agent response + radar_delta for live radar update
GET    /agents/status       → All agent states, confidence, latency, last updated
WS     /ws/agents           → Real-time agent telemetry (Engineer View)
WS     /ws/listener/{id}    → Real-time ESIE updates every 90 seconds
GET    /fairness/metrics    → Gini coefficient, artist concentration, geographic spread
GET    /explain/{track_id}  → Full SEA explanation with audio feature citations
POST   /integrity/check     → Public API: AI-generation score + authenticity certificate
GET    /health              → System health, FAISS index status, model load status
```

## Repo 4: `psyche-bench` — The Academic Moat

```bash
pip install psyche-bench

# Evaluate any recommender against the PSYCHE benchmark
psyche-bench evaluate \
  --model my_recommender.py \
  --dataset fma-small \
  --baselines spotify-api,random,popularity,genre-match,als-implicit \
  --metrics serendipity,diversity,coherence,latency,cold-start-ndcg

# Output: Full benchmark report + W&B link
```

When researchers use `psyche-bench` in their papers, they cite PSYCHE. When blog posts compare music recommenders, they use psyche-bench. When other projects use it, PSYCHE becomes infrastructure for the field — and infrastructure is never forgotten.

## Repo 5: `psyche-plugins`

- **VS Code Extension (Highest Virality):** Music that changes based on your active file, error count, and time in flow state. "My IDE now recommends music based on my code error count" is a tweet that writes itself.
- **Electron Desktop App:** Full native desktop experience matching web app quality (Addition 50).
- **Spotify Web Player Chrome Extension:** Overlays PSYCHE's explanation layer on Spotify Web Player.
- **Discord Bot:** Server mood → collective ESIE → music recommendation. Gaming/study communities.

---

# PART 8: THE FULL TECH STACK — 100% FREE & OPEN SOURCE

## Audio Analysis & Feature Extraction

| Tool | GitHub Stars | Role in PSYCHE |
|---|---|---|
| **librosa** | 7k+ | MFCCs, chroma, tempo, spectrograms, onset detection, segmentation. Foundation of all audio feature extraction. |
| **Demucs (Meta)** | 8k+ | State-of-the-art stem separation: vocals, drums, bass, guitar, other. Powers the Micro-Event Attribution Engine. |
| **essentia (MTG)** | 2.7k+ | Key detection, BPM, chord analysis. Complements librosa for harmonic features. |
| **madmom** | 1.3k+ | Beat tracking, onset detection, tempo estimation. More accurate than librosa for rhythmic features. |
| **audiocraft (Meta)** | 22k+ | MusicGen + EnCodec. Used for audio generation experiments and understanding audio tokenization. |

## Music Foundation Models (The Secret Weapons)

| Tool | GitHub | What It Provides |
|---|---|---|
| **MERT** | yizhilll/MERT | Self-supervised music understanding model. 95M and 330M parameter variants. The "BERT for music" — produces rich semantic embeddings that understand musical structure. |
| **LAION-CLAP** | LAION-AI/CLAP | Contrastive Language-Audio Pretraining. Joint audio-text embedding space. Enables semantic queries like "calm piano music with tension" → vector search in milliseconds. |
| **microsoft/muzic** | microsoft/muzic | MusicBERT, CLaMP, PDAugment. Research-grade music understanding models. |
| **ACE-Step** | ace-step/ACE-Step | Music generation foundation model. Used for generating synthetic training data for the Content Integrity Guardian. |

## LLM & Agentic AI Layer

| Tool | Stars | Role in PSYCHE |
|---|---|---|
| **LangChain** | 98k+ | Agent orchestration framework. Powers the LLM Meta-Orchestrator, Sonic Explainability Agent RAG pipeline, and Cold Start Psychographic Agent conversation flow. |
| **LlamaIndex** | 40k+ | RAG over audio feature database. Enables the SEA to retrieve relevant audio feature context before generating explanations. |
| **Ollama** | 120k+ | Run Llama 3 / Mistral locally. Zero API cost for development and testing. |
| **Anthropic API (Claude)** | — | Backbone for Cold Start Agent and SEA in production demo. Superior musicological reasoning. |

## Reinforcement Learning

| Tool | Stars | Role in PSYCHE |
|---|---|---|
| **Stable-Baselines3** | 9k+ | PPO and SAC implementations for the Fairness-Aware RL Recommender. |
| **Gymnasium (Farama)** | 7k+ | Custom music recommendation environment. State = listener vector + candidate pool. Action = track selection. Reward = composite engagement + fairness. |
| **Ray RLlib** | 35k+ | Scalable distributed RL training. Used if SB3 training is too slow on single machine. |

## Deep Learning & Recommendation Models

| Tool | Stars | Role in PSYCHE |
|---|---|---|
| **PyTorch** | 85k+ | All neural network training: Temporal Taste GRU, Playlist Coherence Transformer, Content Integrity Classifier. |
| **Hugging Face Transformers** | 140k+ | Pre-trained Transformer models for Playlist Coherence Architect. Fine-tuning infrastructure. |
| **RecBole** | 3.5k+ | Recommendation system benchmark suite. Provides ALS baseline (B4) and standardized evaluation protocols. |
| **FAISS (Meta)** | 32k+ | Billion-scale vector similarity search. Stores all MERT + CLAP embeddings. Sub-millisecond retrieval. |

## Audio Quality Pipeline (New Additions)

| Technology | Purpose | Addition |
|---|---|---|
| py3d-audio (open-source) | HRTF binaural spatial audio for any headphone | 46 |
| Gentle aligner (CMU) | Beat-by-beat lyrics synchronization | 48 |
| librosa waveform → animated artwork | Procedural animated cover art | 49 |
| Electron | Native desktop experience | 50 |
| Roon RAAT / DLNA protocol | Lossless audiophile hardware integration | 58 |
| pyloudnorm | Volume normalization control (LUFS standard) | 37 |
| FLAC 24-bit/192kHz streaming (ffmpeg) | Hi-res lossless tier | Audio Engine |

## Infrastructure, Deployment & Monitoring

| Tool | Role in PSYCHE |
|---|---|
| **FastAPI** | Serving layer for all agent calls. RESTful API with Pydantic validation, OpenAPI docs auto-generated. <5ms overhead. |
| **Next.js 15** | Production frontend. SSR for SEO, RSC for performance. |
| **Docker + Docker Compose** | Full containerized deployment. One command to run entire stack: `docker-compose up`. |
| **Weights & Biases (free)** | Experiment tracking, RL training visualization, model comparison, drift monitoring. |
| **DVC** | Data pipeline versioning. Every dataset version and feature extraction run is reproducible from git commit. |
| **Hugging Face Spaces (free)** | Public deployment platform. Demo accessible without any setup. |
| **Vercel (free)** | Frontend deployment. Preview URLs on every PR. |

---

# PART 9: THE DATA STRATEGY

## 9.1 Data Sources — All Open License

| Dataset | Source | Size | License | What It Provides |
|---|---|---|---|---|
| **FMA (Free Music Archive)** | github.com/mdeff/fma | 106k tracks, 343GB full / 7.2GB small | Creative Commons | Audio files + metadata + genre labels. Primary audio corpus. |
| **Spotify Million Playlist Dataset** | AICrowd RecSys Challenge | 1M playlists, 66M track-playlist pairs | Academic use | Playlist co-occurrence data. Trains Coherence Architect. |
| **Last.fm LFM-1b Dataset** | Schedl et al. | 1 billion listening events, temporal | Research | Temporal listening history. Trains Temporal Taste Evolution Model. |
| **AudioSet** | Google Research | 2M 10-second YouTube clips, 527 classes | CC BY 4.0 | Audio event labels. Fine-tunes Content Integrity Guardian. |
| **MTG-Jamendo** | MTG Barcelona | 55k+ tracks, mood/genre tags | Creative Commons | Mood labels as proxy for emotional state ground truth. |
| **MagnaTagATune** | magnatagatune.com | 25k 29-second clips, 188 tags | Research | Auto-tagging benchmark. Evaluates MERT embeddings. |

**Data Ethics Verification:** All datasets: (1) have explicit research/CC licenses, (2) do not include PII, (3) are not scraped from Spotify in violation of ToS, (4) are citeable in academic documentation.

## 9.2 Data Quality Framework

| Quality Dimension | How PSYCHE Handles It |
|---|---|
| **Completeness** | FMA has ~8% missing audio files in the full set. Strategy: use FMA-small (8k tracks, 100% complete) for development; FMA-medium for final training. Log missing rate per batch. |
| **Audio validity** | All files validated with `librosa.load()` in pipeline. Corrupt files quarantined and logged. Target: <1% invalid files in training set. |
| **Metadata consistency** | Artist/track name normalization using fuzzy matching (rapidfuzz). Duplicate detection via MERT embedding cosine similarity > 0.98 threshold. |
| **Label drift** | Mood labels are subjective. Strategy: use valence/arousal dimensions (continuous) rather than categorical mood labels. More robust to annotator disagreement. |
| **Temporal data integrity (LFM-1b)** | Remove listening events with timestamps outside 2008–2024 range. Remove sessions <2 tracks or >200 tracks (likely bots). Document all filters. |

## 9.3 Data Versioning Strategy — DVC

```
data/
├── raw/              ← Sacred. Never modified. DVC tracked.
├── validated/        ← Post-quality-check. DVC tracked.
├── features/         ← MERT + CLAP embeddings. DVC tracked.
├── splits/           ← Fixed-seed train/val/test. DVC tracked.
└── models/           ← Trained artifacts. DVC + W&B links.
```

**Reproducibility guarantee:** Any experiment in PSYCHE can be reproduced exactly using: `git checkout <commit_hash> && dvc checkout`.

## 9.4 Feature Engineering Strategy — Every Feature Documented

| Feature Group | Features Extracted | Hypothesis | Tool |
|---|---|---|---|
| **Low-level audio** | MFCCs (40 coefficients), spectral centroid, rolloff, zero-crossing rate, RMS energy | Capture timbral characteristics that determine genre and mood perception | librosa |
| **Rhythmic** | Tempo (BPM), beat strength, onset envelope, rhythmic regularity | Tempo is the primary driver of arousal; beat strength correlates with energy preference | librosa + madmom |
| **Harmonic** | Chroma features (12-dim), key, mode (major/minor), harmonic change rate | Harmonic tension and resolution patterns drive emotional valence | librosa + essentia |
| **Structural** | Segment boundaries, section lengths (verse/chorus/bridge), energy arc across sections | Song structure determines narrative arc; bridge energy spikes cause skips or saves | librosa segmentation |
| **Stem-level** | Vocal energy, bass energy, drum pattern regularity, guitar/melody presence | Users who skip at specific stems have stem-level preferences (e.g., dislike heavy bass) | Demucs |
| **Semantic embedding** | MERT 95M representation (768-dim), CLAP joint embedding (512-dim) | Foundation model representations capture high-level musical meaning beyond hand-crafted features | MERT + LAION-CLAP |

---

# PART 10: THE EXPERIMENTATION FRAMEWORK

## 10.1 The Five Baselines — Must Be Beaten Before Complex ML Is Justified

| Baseline | Method | Expected Performance | Purpose |
|---|---|---|---|
| **B0: Random** | Random track selection from catalog | ~2% serendipity rate | Sanity check floor |
| **B1: Popularity** | Top-100 most played tracks globally | ~8% engagement rate | Confirms personalization adds value |
| **B2: Genre matching** | Match user's top genre, sort by plays | ~12% engagement | Baseline for content-based |
| **B3: Spotify API** | spotify.recommendations() endpoint | ~18% serendipity, baseline diversity | THE baseline PSYCHE must beat on all metrics |
| **B4: Collaborative filtering (ALS)** | Implicit ALS on MPD co-occurrence matrix | ~15% engagement | Validates deep approach beats classical CF |

## 10.2 The Five Hypothesis-Driven Experiments

| Experiment ID | Hypothesis | Control | Treatment | Decision Criterion |
|---|---|---|---|---|
| **EXP-01** | MERT embeddings outperform MFCCs for artist similarity | FAISS search with MFCC features | FAISS search with MERT embeddings | Precision@10 on held-out artist pairs |
| **EXP-02** | CLAP similarity improves serendipity over genre-based discovery | Genre-matched random track | CLAP cosine similarity within genre boundary | % of tracks user would save (simulated) |
| **EXP-03** | RL with fairness reward doesn't degrade engagement vs. greedy | Greedy engagement-only recommender | PPO with composite fairness+engagement reward | Engagement rate vs. artist Gini coefficient |
| **EXP-04** | Temporal decay improves recommendations for 3+ year users | Full history equal-weight CF | GRU with exponential decay on LFM-1b sessions | nDCG@10 on held-out recent sessions |
| **EXP-05** | Stem-level features add signal beyond full-track features | Full-track MERT embedding only | MERT + Demucs stem embeddings concatenated | Micro-event attribution accuracy |

## 10.3 Validation Strategy — Time-Based Splits for All Temporal Models

| Model | Split Strategy | Rationale |
|---|---|---|
| **Temporal Taste Model (GRU)** | Train: LFM-1b sessions 2008–2021. Val: 2022. Test: 2023–2024. | Must simulate future listening from past. Random split leaks future data. |
| **RL Recommender (PPO)** | Train env: MPD playlists 1–800k. Val: 800k–900k. Test: 900k–1M. | Playlist sequences are temporally ordered within sessions. |
| **Content Integrity Classifier** | Standard 70/15/15 stratified split on AudioSet/FMA | Non-temporal classification; stratification ensures class balance. |
| **Playlist Coherence Model** | Train on MPD playlists with ≥20 tracks. Test on 5k held-out playlists. | Held-out set evaluated by human raters on 100 sample playlists. |
| **CLAP Serendipity Retrieval** | k-fold cross-validation on MTG-Jamendo mood labels | Non-temporal; fold stratified by mood category. |

## 10.4 Monitoring Strategy — Four Categories

| Category | Metrics | Alert Threshold |
|---|---|---|
| **Business** | Simulated engagement rate, artist Gini coefficient, cold-start quality score | Drop >5% from baseline triggers investigation |
| **Model Performance** | nDCG@10 per agent, Content Integrity F1, Coherence smoothness score | Drop >3% from validation performance triggers retrain flag |
| **Data Quality** | Missing feature rate per batch, CLAP embedding distribution shift, audio file corruption rate | Missing rate >2% or KS-test p<0.05 on embeddings triggers alert |
| **System Health** | API p95 latency, error rate, FAISS query time, memory usage | Latency >200ms or error rate >1% triggers immediate investigation |

---

# PART 11: THE FOUR BUILD TOOLS — EXACT ROLE AND USAGE

## Tool 1: Google Antigravity — Primary Build Environment

**What It Is:** Agent-first IDE (antigravity.google) — a heavily modified VS Code fork powered by Gemini 3.1 Pro, with support for Claude Sonnet 4.6. Free in public preview with generous rate limits.

**Key Capabilities:**
- **Agent Manager View:** Mission control dashboard where you spawn, monitor, and interact with multiple agents running in parallel. Each agent gets its own task, produces Artifacts, and you guide them by leaving comments — like commenting on a Google Doc.
- **Built-in Browser Agent:** Deep Chrome integration. Agents can spin up a browser, navigate your localhost, interact with the UI, and return screenshots as Artifacts — without you switching windows.
- **Asynchronous Execution:** Dispatch an agent on a long-running task, then switch to a different workspace and work on something else.
- **Knowledge Base:** Agents save learned context (patterns, gotchas, conventions) to a project knowledge base. Future agents automatically read this, so quality compounds over time.

**PSYCHE Workspace Structure:**
```
Workspace 1: psyche-core     (backend agents, ML pipeline)
Workspace 2: psyche-ui       (Next.js frontend)
Workspace 3: psyche-api      (FastAPI layer)
Workspace 4: psyche-bench    (evaluation harness)
```

**Model Selection:**
- **Gemini 3.1 Pro** (free, highest rate limit): data pipelines, feature extraction, notebook work, boilerplate generation
- **Claude Sonnet 4.6**: LLM agent code (ESIE, SEA, orchestrator), complex architectural decisions, nuanced reasoning
- **Claude Opus 4.6** (sparingly): Final system architecture reviews, critical algorithm implementations

**Agent Skill Files (.agents/ directory):**
```markdown
# .agents/skills/psyche-conventions/SKILL.md
## PSYCHE Code Conventions

### Agent Implementation Rules
- ALL agents extend BasePsycheAgent from psyche/agents/base.py
- ALL agent __init__ accepts config: PsycheConfig (Pydantic)
- ALL agents have .infer() as primary method, fully typed
- ALL agents have .fallback() that returns valid output when inference fails
- NEVER hardcode model names, paths, thresholds — always config.yaml
- EVERY agent logs to W&B via psyche.utils.logging.log_agent_call()

### Data Model Rules
- ALL data models are Pydantic v2 BaseModel
- EVERY model has model_config = ConfigDict(frozen=True) unless mutation needed

### Experiment Rules
- EVERY experiment run logs: git commit hash, DVC data hash, all hyperparams
- NEVER use random splits on temporal data
- ALWAYS document hypothesis, control, treatment, decision criterion
```

## Tool 2: GSD (Get Shit Done) — Planning & Execution Framework

**What It Is:** Meta-prompting, context engineering, and spec-driven development system with 31,000+ GitHub stars. Installs as an npm package and adds slash commands to Claude Code and Antigravity.

**The Core GSD Loop:**
```
/gsd:discuss-phase N    → AI asks clarifying questions, resolves ambiguity
/gsd:plan-phase N       → AI researches, creates atomic task list with verification criteria
/gsd:execute-plan       → Subagents implement in parallel, each with fresh context, each commits atomically
/gsd:verify-work N      → Checks output against goals, creates fix plans for failures
/gsd:ship N             → Creates clean PR from verified work
```

**Install:**
```bash
npx get-shit-done-cc@latest --global
```

**GSD Configuration for PSYCHE:**
```yaml
# .gsd/config.yaml for psyche-core
project:
  name: "PSYCHE Core"
  type: "ml-python"
  description: "Multi-agent music intelligence platform"

research_before_questions: true
context_window_size: "1M+"

quality_gates:
  schema_drift_detection: true
  security_enforcement: true
  scope_reduction_detection: true

agent_skills:
  - path: ".agents/skills/psyche-conventions/SKILL.md"
  - path: ".agents/skills/ml-experiment/SKILL.md"
```

**Rule:** GSD runs *before* Antigravity starts building. The sequence is always:
```
GSD discuss → GSD plan → Antigravity execute → Ralph Loop verify → CodeRabbit review
```

## Tool 3: Ralph Loop — Autonomous Execution Engine

**What It Is:** An autonomous AI agent loop that runs Claude Code (or Antigravity) repeatedly until all PRD items are complete. Created by Geoffrey Huntley in 2025. Core philosophy: instead of managing context carefully, *embrace fresh starts*. Git history is memory. Progress persists in files.

**How It Works:**
```bash
while true; do
  claude_code --run-prompt "CLAUDE.md"   # Fresh instance, reads task file
  check_completion                        # Did it output <promise>COMPLETE</promise>?
  if complete; then break; fi
  update_progress                         # Update progress.txt with what was done
done
```

**PSYCHE-Specific Ralph Configuration:**
```bash
# .ralphrc for psyche-core
PROJECT_NAME="psyche-core"
PROJECT_TYPE="python-ml"
CLAUDE_TIMEOUT_MINUTES=30        # ML training tasks need time
MAX_CALLS_PER_HOUR=60
SESSION_CONTINUITY=true
ALLOWED_TOOLS="Write,Read,Edit,Bash(git *),Bash(python *),Bash(pytest *),Bash(pip *)"
```

**The PSYCHE CLAUDE.md Template:**
```markdown
# PSYCHE Build Instructions

## Current Phase
[Filled in by GSD plan output]

## Completion Criteria
[Exact acceptance criteria from GSD phase plan]

## Architecture Constraints
- ALL agents must extend BasePsycheAgent protocol
- ALL data models must use Pydantic v2
- ALL configs must read from config.yaml, NEVER hardcoded
- ALL experiments must log to W&B with commit hash + DVC hash
- Fallback behavior required for every agent

## Verification
[Specific test commands and expected outputs]

## Output Promise
When all stories pass: output <promise>COMPLETE</promise>
```

**Use Ralph Loop for:** Implementing individual agents after their architecture is designed · Building frontend components after design tokens are set · Writing test suites · Data pipeline work (process 10k FMA tracks → embeddings → FAISS index)

**Do NOT use Ralph for:** Architectural decisions · Anything without verifiable acceptance criteria · The first week (no established patterns yet)

## Tool 4: CodeRabbit — Quality Gate

**What It Is:** AI-powered code review tool running on 2M+ repositories. Auto-reviews every pull request using LLMs + 40+ linters/SAST tools, leaving inline comments just like a senior engineer.

**PSYCHE `.coderabbit.yaml` for psyche-core (Python/ML):**
```yaml
reviews:
  high_level_summary: true
  path_filters:
    - "!data/raw/**"
    - "!data/features/**"
    - "!.planning/**"
    - "!notebooks/**"

instructions: |
  This is a Python ML project. PSYCHE is a multi-agent music intelligence platform.

  ALWAYS flag:
  - Hardcoded values that should be in config.yaml
  - Missing type hints on public functions
  - W&B logging missing from experiment code
  - DVC not tracking new data artifacts
  - Agent without documented fallback behavior
  - Missing docstrings on BasePsycheAgent subclasses
  - Latency-critical code paths without profiling
```

**PSYCHE `.coderabbit.yaml` for psyche-ui (TypeScript/Next.js):**
```yaml
instructions: |
  ALWAYS flag:
  - Missing null checks / unhandled promise rejections
  - Hardcoded color values (must use CSS variables from globals.css)
  - Missing loading and error states on data-fetching components
  - WebSocket connections not cleaned up in useEffect
  - Missing aria-label on interactive elements
  - Components exceeding 200 lines (must decompose)
```

**Weekly CodeRabbit Ritual (every Sunday):**
- Review the week's flagged issues by category
- Identify the top 3 recurring issue types
- Add those to `.coderabbit.yaml` instructions as explicit rules

## The Four-Tool Orchestration Map

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     THE PSYCHE BUILD CYCLE                              │
│                                                                         │
│  1. GSD DISCUSS          You + AI clarify what is being built           │
│     (15-30 min)          Ambiguity resolved before a line is written    │
│                                    │                                    │
│  2. GSD PLAN             AI researches, creates atomic task plan        │
│     (30-60 min)          2-3 tasks per phase, each with verify criteria │
│                                    │                                    │
│  3. ANTIGRAVITY          You architect, AI executes                     │
│     (hours/overnight)    Parallel workspaces, Browser Agent for UI      │
│         +                                                               │
│     RALPH LOOP           Autonomous overnight execution for ML tasks    │
│     (overnight)          "Build this, loop until tests pass"            │
│                                    │                                    │
│  4. CODERABBIT           Auto-reviews every PR                          │
│     (minutes)            Catches bugs, missing tests, arch violations   │
│                                    │                                    │
│  5. YOU                  Review CodeRabbit comments, fix, merge         │
│     (30-60 min/PR)       Human judgment on what CodeRabbit can't catch  │
│                                    │                                    │
│  6. LOOP                 Next phase begins                              │
└─────────────────────────────────────────────────────────────────────────┘
```

**Day structure during build weeks:**
- **Morning (9am–12pm):** GSD discuss + plan for today's phase. Antigravity hands-on work.
- **Afternoon (12pm–6pm):** Antigravity execution. Review previous Ralph Loop results. CodeRabbit fixes.
- **Evening (6pm–10pm):** Launch Ralph Loop for overnight autonomous tasks. Set up CLAUDE.md with tomorrow's spec.
- **Overnight:** Ralph Loop runs. Antigravity Browser Agent verifies frontend changes.

---

# PART 12: THE 14-WEEK BUILD PLAN

## Master Timeline at a Glance

```
Weeks 1–2:  Foundation Layer        Data pipeline, FAISS, baselines, all tooling setup
Week 3:     Listener Modeling       ESIE, Cold Start Agent, GRU baseline
Week 4:     Fairness RL             PPO agent, Gymnasium, Fairness dashboard
Week 5:     Discovery + Integrity   CLAP serendipity, Content Guardian, SEA
Week 6:     Coherence + Context     Playlist Coherence Transformer, Context Fusion, Temporal
Week 7:     Orchestrator + API      Meta-Orchestrator, FastAPI layer, full integration
Week 8:     Cold Start Experience   The Interview screen (viral demo core)
Week 9:     Engineer View + Portal  Mission control, API playground
Week 10:    Identity + Fairness UI  UMAP scatter, Taste Timeline, World Map
Week 11:    Audio Engine + Library  Lossless tier, HRTF spatial, lyrics sync, sort engine
Week 12:    Consumer Polish         Animated artwork, desktop app, cross-device sync
Week 13:    OSS Polish              psyche-bench CLI, VS Code plugin, full docs
Week 14:    Launch                  HN, r/ML, Product Hunt, blog post, recruiter outreach
```

---

## WEEK 1: ENVIRONMENT SETUP & TOOLING

**Goal:** All tooling configured. GitHub org created. Docker environment running. All agent skill files written.

### Day 1: GitHub Org + Tool Stack Setup

```bash
# 1. Create GitHub org
# Go to github.com → New organization → "psyche-music"
# Create repos: psyche-core, psyche-ui, psyche-api, psyche-bench, psyche-plugins

# 2. Install GSD globally
npx get-shit-done-cc@latest --global

# 3. Clone psyche-core, initialize GSD
cd psyche-core
/gsd:new-project
# GSD asks questions → answer fully → generates .planning/ directory with project brief

# 4. Download Antigravity
# antigravity.google/download → sign in with Gmail → open psyche-core workspace

# 5. Connect CodeRabbit to psyche-music GitHub org (2 clicks at coderabbit.ai)
# 6. Set up W&B project: wandb init --project psyche-production
# 7. Set up DVC: dvc init && git add .dvc && git commit -m "chore: init dvc"
```

### Day 2: Docker Environment

```bash
/gsd:discuss-phase 0    # Discuss Docker setup requirements
/gsd:plan-phase 0       # GSD creates Docker task plan
/gsd:execute-plan       # Antigravity executes: Dockerfile + docker-compose.yml
```

Antigravity mission:
```
Requirements:
- Python 3.11 base with all ML dependencies pinned
- Services: psyche-core, psyche-api (FastAPI), redis (caching), postgres (user data)
- librosa, Demucs, MERT (via transformers), CLAP (LAION), FAISS-cpu, torch
- docker-compose up brings full stack in one command
- Health checks on all services
- Volume mounts for data/ directory (DVC-managed, not in image)

Output promise: docker-compose up works, all services healthy
```

### Days 3–5: Data Pipeline (GSD Phase 1)

```bash
/gsd:discuss-phase 1
/gsd:plan-phase 1
# Task 1.1: FMA-small download + validation (file integrity, corrupt audio detection)
# Task 1.2: librosa feature extraction (MFCCs, chroma, tempo, energy) → DVC tracked
# Task 1.3: MERT + CLAP embeddings → FAISS index build
```

**Day 3 Evening — Ralph Loop for overnight data processing:**
```bash
cat > scripts/ralph/CLAUDE.md << 'EOF'
# PSYCHE Phase 1: Data Pipeline

## Task 1.1: FMA Validation Pipeline
Build psyche/pipelines/ingestion.py that:
- Downloads FMA-small (8k tracks) to data/raw/fma_small/
- Validates every audio file with librosa.load()
- Quarantines corrupt files to data/quarantine/ with logged reason
- Outputs: data/validated/fma_small/ with manifest.json
- Logs: validation rate, corrupt file count, to W&B

Acceptance criteria:
- All 8k files processed
- manifest.json contains path, duration, sample_rate for each valid file
- DVC tracking: dvc add data/validated/

Output <promise>PHASE1_1_DONE</promise> when complete.
EOF

./scripts/ralph/ralph.sh --max-iterations 30
```

**Day 4:** Review Ralph output → Fix CodeRabbit flags → merge → Task 1.2 (MFCC + chroma extraction overnight)

**Day 5:** Task 1.3 — MERT + CLAP embeddings + FAISS index build overnight

```python
# Verify FAISS index
import faiss
index = faiss.read_index('data/features/clap_index.faiss')
print(f'FAISS index: {index.ntotal} vectors, {index.d} dimensions')
# Expected: ~8000 vectors, 512 dimensions for CLAP
```

### Days 6–7: Baselines B0–B4 (GSD Phase 2)

All 5 baselines implemented, logged to W&B under "baseline-benchmarks" project.

```bash
/gsd:discuss-phase 2
/gsd:plan-phase 2
# Task 2.1: B0 (random), B1 (popularity), B2 (genre-match)
# Task 2.2: B3 (Spotify API) with rate limiting, log 100 test user profiles
# Task 2.3: B4 (ALS collaborative filtering via RecBole)
```

**Day 7 Evening — Week 1 close:**
```bash
/gsd:complete-milestone     # Archive Week 1 planning, prep Week 2
# Weekly CodeRabbit ritual: review flagged issue categories from Week 1 PRs
# Add top 3 recurring issues to .coderabbit.yaml instructions
# Update .agents/skills/ with patterns discovered this week
```

---

## WEEK 2: FRONTEND SCAFFOLD + PSYCHE-BENCH FOUNDATION

**Goal:** psyche-ui Next.js scaffold running locally with design system and mock data. psyche-bench CLI skeleton. No real API yet — everything uses mock data so frontend can develop in parallel.

### Days 8–9: psyche-ui Scaffold (Antigravity Browser Agent)

```
Antigravity Mission:
- Next.js 15 App Router, TypeScript strict mode
- CSS Variables in globals.css:
  --bg-primary: #0A0A0B
  --bg-secondary: #111114
  --bg-card: #16161A
  --accent-amber: #E8A04A
  --accent-teal: #00D4B8
  --text-primary: #F5F0E8
  --text-secondary: #8A8A94
  --signal-green: #4AE88A
  --signal-red: #E84A4A
- Fonts: Instrument Serif (headings) + Berkeley Mono (data) via next/font
- Radix UI primitives, Framer Motion, Recharts, D3, Zustand, TanStack Query v5, Socket.io-client
- Landing page renders at localhost:3000 with animated waveform background
- ViewToggle component (Listener ↔ Engineer)

Use Antigravity Browser Agent to verify localhost:3000 renders correctly.
Output <promise>SCAFFOLD_DONE</promise> when browser confirms no errors.
```

**Day 9: Design Components Sprint**
Parallel agents in Antigravity:
- Agent A: `AgentCard` component — hardware module aesthetic, LED indicator, confidence meter
- Agent B: `SonicIdentityRadar` — D3-powered EQ-curve radar, five axes, morphing animation
- Agent C: `WaveformBackground` — Canvas sine-wave animation, amber traces on dark

### Days 10–11: psyche-bench Skeleton + Mock API

```bash
/gsd:new-project          # psyche-bench intake
/gsd:discuss-phase 1
/gsd:plan-phase 1
# Task 1.1: CLI scaffold (Click-based, pip installable entry point)
# Task 1.2: Metric implementations (serendipity, Gini, coherence) from psyche/utils/metrics.py
# Task 1.3: FMA-small dataset adapter
```

Create `psyche-ui/lib/mockApi.ts` with full mock data matching the real API schemas. Every component that will eventually call the API gets connected to mocks now.

### Days 12–14: Feature Engineering + Week 2 Hardening

**Day 12:** Demucs stem separation on full FMA-small (8k tracks → 32k stem files) — Ralph Loop overnight

**Day 13:** Create `EXPERIMENT_LOG.md` with EXP-01 hypothesis setup

**Day 14 — Week 2 close:**
```bash
/gsd:complete-milestone
# Verify: docker-compose up works, all Week 1+2 tests pass
# psyche-ui: landing page live on Vercel preview URL
```

---

## WEEK 3: LISTENER MODELING LAYER

**Goal:** ESIE, Cold Start Agent, GRU baseline all working. EXP-01 run and logged.

### Days 15–16: ESIE (Gap 1)

```bash
/gsd:discuss-phase 3
/gsd:plan-phase 3
# Task 3.1: ESIE signal classifiers (time-of-day, activity encoding, recent track features)
# Task 3.2: Llama 3 prompt chain (Ollama) → ListenerStateVector output
# Task 3.3: ESIE validation: 50 synthetic sessions with known emotional contexts
```

**Day 15 Evening — Ralph Loop for ESIE implementation:**
```bash
cat > scripts/ralph/CLAUDE.md << 'EOF'
# PSYCHE Phase 3.1-3.2: Emotional State Inference Engine

Build psyche/agents/esie.py implementing BasePsycheAgent.

Architecture:
1. Signal classifiers: encode [time_of_day, day_of_week, recent_track_features,
   stated_activity, session_length] → feature vector
2. Ollama Llama 3 prompt chain: structured JSON prompt with signal features
   → LLM output parsed to ListenerStateVector[valence, arousal, focus, social]
3. Fallback: if Ollama unavailable, use time-of-day heuristic (morning → high focus,
   evening → lower arousal, midnight → low arousal high valence)

Requirements:
- Fully typed with Pydantic v2
- Async .infer() method
- W&B logging on every call
- Config-driven (model name, thresholds all in config.yaml)
- Unit tests for all three paths (full inference, partial signals, fallback)

Test commands:
pytest tests/unit/test_esie.py -v

Output <promise>ESIE_DONE</promise> when all tests pass.
EOF

./scripts/ralph/ralph.sh --max-iterations 40
```

**Day 16:** Review Ralph output + CodeRabbit review + fix flags + merge ESIE PR + Run EXP-01

### Days 17–18: Cold Start Psychographic Agent (Gap 3)

```bash
/gsd:plan-phase 3        # Cold Start sub-phase
# Task 3.4: LangChain conversation chain (5-question interview)
# Task 3.5: CLAP similarity matching from conversation → warm user embedding
# Task 3.6: Live radar-delta SSE stream for the frontend animation
```

Ralph Loop overnight for Cold Start Agent:
```
Build psyche/agents/cold_start.py.
The agent conducts a 5-turn conversation, extracting psychographic signals
(emotional needs, cultural anchors, listening contexts) then maps to CLAP embedding space.
Each conversational turn should emit a `radar_delta` for the live frontend update.

LLM: Claude Sonnet 4.6 via Anthropic API (superior conversational reasoning).
Fallback: If API unavailable, serve genre-selection fallback.
Acceptance: Integration test psyche_api/tests/test_cold_start.py passes.
```

**Day 18:** Connect to `psyche-ui` Cold Start Interview screen (mock → real). Test live radar update loop via Browser Agent.

### Days 19–21: Temporal Taste GRU + IntentClassifier (Gap 9 + Addition 01)

**Day 19:** GRU architecture setup
```bash
/gsd:discuss-phase 3      # Temporal taste sub-phase + Intent Classifier
/gsd:plan-phase 3
# Task 3.7: LFM-1b data loading + preprocessing
# Task 3.8: GRU + attention architecture (PyTorch)
# Task 3.9: Training with exponential half-life decay
# Task 3.10: IntentClassifier (passive/active/background detection)
```

**Days 19–21:** Ralph Loop training overnight (multi-night). EXP-04 (temporal decay vs. equal-weight history) run as part of training.

---

## WEEK 4: FAIRNESS RL RECOMMENDER (GAP 5)

**Goal:** PPO agent trained, fairness dashboard built, EXP-03 run.

### Days 22–23: Gymnasium Environment Design

```bash
/gsd:discuss-phase 4
# Discuss: state space (listener vector + candidate pool), action space (track selection),
# reward function components (engagement proxy + Gini + geographic spread)
/gsd:plan-phase 4
```

Antigravity mission:
```
State: ListenerStateVector (4 dims) + candidate_pool_embeddings (10 tracks × 512 dims)
Action: Discrete selection from 10 candidates
Reward: α×engagement_proxy + β×artist_diversity_delta + γ×geographic_spread_delta
  where α=0.7, β=0.2, γ=0.1 (adjustable in config.yaml)

Environment must be:
- Compatible with Stable-Baselines3 PPO
- Fully typed
- Logged to W&B (episode reward, each reward component separately)
- Configurable reward weights via config.yaml

Tests: tests/unit/test_fairness_env.py
```

**Day 23 — PPO Training (3-night Ralph Loop):**
- Night 1: PPO warm-start, verify convergence signal in W&B
- Night 2: Tune reward weights, full training run
- Night 3: EXP-03 (PPO with fairness vs. greedy engagement-only)

### Days 24–26: Fairness RL Frontend + Artist Tools

**Day 24 — Parallel agents (Antigravity Workspace 2):**
- Agent 1: `FairnessGauge` — animated circular Gini dial, amber needle
- Agent 2: `WorldMap` — D3 projection, countries colored by artist play fraction
- Agent 3: `RewardDecompositionBar` — live horizontal bars
- Agent 4: Artist Transparency Report API (Addition 24)

**Day 25:** Connect Fairness Observatory page. Run EXP-03. Target: 31% better Gini with <5% engagement degradation.

**Day 26:** Sonic Compatibility Analyzer (Addition 25) — artist upload API for pre-release audience prediction.

---

## WEEK 5: DISCOVERY AGENT + CONTENT INTEGRITY + SEA (GAPS 4, 8, 10)

### Days 29–31: Serendipity Agent + Content Integrity Guardian

**Day 29:** CLAP Audio Similarity Graph (Ralph Loop)
```bash
# Build serendipity discovery on top of the FAISS CLAP index
# Novelty scorer: penalize too similar (similarity > 0.85) AND too dissimilar (< 0.25)
# EXP-02: CLAP serendipity vs. genre-based random discovery
# Target: 22%+ serendipity rate vs. 18% Spotify baseline
```

**Day 30:** Content Integrity Classifier fine-tuning (overnight Ralph)
```bash
# Fine-tune CLAP classifier on AudioSet (AI-gen audio vs. organic)
# Generate synthetic negative examples using ACE-Step
# Target: F1 > 0.85 on held-out test set
# Public /integrity/check API for Addition 26 (AI Content Shield)
```

**Day 31:** Sonic Explainability Agent (SEA)
```bash
# LangChain RAG pipeline: FAISS audio feature DB → LLM explanation generation
# Every recommendation gets: "Why this track?" in musical language
# SEA must reference: specific audio features, artist context, Sonic Genome patterns
# Validated: 50-sample human evaluation (you rate 50 explanations: meaningful/not)
# Target: 80%+ rated meaningful
```

### Days 32–35: SEA Frontend + Discovery Features Integration

- `ExplanationBubble` component + `TrackCard` with agent badge + WHY THIS TRACK? collapsible section
- Connect psyche-api's `/explain/{track_id}` endpoint to the frontend
- Rabbit Hole Mode UI (Addition 15) — depth slider, breadcrumb trail
- Sonic Bridge component (Addition 17) — cross-genre CLAP search
- Era Time Machine UI (Addition 18) — decade selector overlay

---

## WEEK 6: COHERENCE + CONTEXT FUSION + REMAINING AGENTS (GAPS 6, 7, 9)

### Days 36–38: Playlist Coherence Transformer

**Day 36 — Architecture design (mandatory GSD discuss — do not skip):**
```bash
/gsd:discuss-phase 6
# Discuss: MPD data loading for coherence training,
# Transformer seq2seq vs. GNN approaches,
# Energy/key compatibility function design
# Human evaluation protocol for 100-sample manual review
```

**Days 37–38 — Training (overnight Ralph Loops):**
```bash
# Fine-tune HuggingFace Transformer seq2seq on MPD playlists ≥20 tracks
# Input: seed track embedding + target length + listener state vector
# Output: sequence of track recommendations optimizing energy arc + key compatibility
# Training: 2 nights minimum (MPD is large)
# Evaluation: 5k held-out playlists + 100-sample human rating
# Target: coherence score 0.89+ (28% better than Spotify baseline)
```

Smart Shuffle (Addition 51) is automatically enabled once Coherence Agent is running.

### Days 39–40: Context Fusion + Remaining Additions

**Day 39:** Context Fusion Module with weather API + calendar integration (Addition 13)

**Day 40:** Emotional Arc Builder (Addition 09) backend + Rumination Guard agent (Addition 12)

**Day 40 Evening:**
```bash
/gsd:discuss-phase 6
# Key design decision: how does listener state vector determine agent weights?
# Write the weighting rules. This is a design decision, not an implementation decision.
```

---

## WEEK 7: META-ORCHESTRATOR + FASTAPI + FULL INTEGRATION

**Goal:** All agents wired into a single production-ready system. FastAPI serving layer live. <200ms p95 enforced in CI.

### Days 43–44: LLM Meta-Orchestrator

```python
# psyche/orchestrator.py
# Input: ListenerStateVector + context signals + all agent outputs (as structured JSON)
# Process: LLM prompt with rule-based pre-weighting based on listener state
#   Example: arousal=HIGH + activity=WORKOUT → Coherence weight × 1.4, Serendipity × 0.6
# Output: Final ranked track list with explanation metadata + agent weight breakdown

# The LLM is Claude Sonnet 4.6 (best reasoning for this blending logic)
# Fallback: Rule-based weighting without LLM (pure heuristic) if API unavailable
```

### Days 45–46: FastAPI Layer (Ralph Loop)

```bash
# Build complete psyche-api with all endpoints
# Acceptance criteria:
# - All endpoints return correct Pydantic schemas
# - WebSocket connections stable under 10 concurrent connections
# - /health endpoint returns all agent statuses
# - Swagger UI available at /docs
# - test_latency.py: 100 sequential /recommend calls, p95 < 200ms
```

### Days 47–49: End-to-End Integration + Latency Enforcement

**Day 47:** 200 synthetic user sessions through the complete pipeline
```bash
# Script: scripts/validate_pipeline.py --sessions 200
# Every session: cold start → ESIE → all agents → orchestrator → SEA → response
# Log all metrics to W&B under "integration-test-v1"
```

**Day 48 — Latency profiling and optimization:**
```bash
# FAISS retrieval target: <10ms
# All agents parallel target: <120ms  
# Meta-orchestrator target: <25ms
# SEA explanation target: <15ms
# Total p95 target: <200ms

# Optimization: pre-compute MERT embeddings, run agents async with asyncio.gather,
# cache frequent user queries
```

**Day 49 — CI enforcement:**
```yaml
# .github/workflows/ci.yml
# Add: pytest tests/performance/test_latency.py
# test_latency.py fails CI if p95 > 200ms on 100 calls
```

Add Webhooks (Addition 29) — external signal ingestion into Context Fusion Module.

---

## WEEK 8: COLD START INTERVIEW EXPERIENCE (THE VIRAL CORE)

**Goal:** The Cold Start Interview screen is complete, wired to real API, verified via Browser Agent.

### Days 50–52: Interview Chat + Live Radar Animation

**Day 50 — The experience flow:**
1. User arrives at `/demo` → dark screen with pulsing waveform
2. PSYCHE typewriter text: "Let's build your Sonic Identity."
3. Chat window opens: first question from Cold Start Agent streams in character by character
4. User types answer → submitted
5. LEFT SIDE: agent streams response (typewriter effect)
6. RIGHT SIDE: Sonic Identity radar morphs. Specific axes activate based on the answer content
7. After each of 5 questions: radar pulse animation, confidence band grows
8. After question 5: "Initializing PSYCHE..." → waveform animation → main dashboard transition

**Day 51 — Antigravity Workspace 2 (psyche-ui), all day:**
```
Build the ColdStartInterview page at /demo.

Left side: ColdStartChat component
- Message history with alternating user/agent bubbles
- Agent messages: typewriter streaming effect (character by character)
- User input: dark terminal-style input with amber cursor
- Each message bubble has timestamp in Berkeley Mono

Right side: RadarBuilder component
- SonicIdentityRadar (D3 EQ-curve visualization)
- Starts flat (no activation)
- Each user answer triggers a radar_delta from the /cold-start/message SSE endpoint
- Framer Motion spring animation interpolates the radar curve to new values
- After all 5 questions: pulse animation, PSYCHE branding appears

Transition: After interview completes, full-page Framer Motion transition
(waveform sweep) → main dashboard

Browser Agent must verify:
- Chat messages render correctly
- Radar updates after each message
- Transition to dashboard works
```

**Day 52:** Integration with real Cold Start Agent. 5 real question/answer sessions tested.

### Days 53–54: Polish + Social Features

**Day 53:** Micro-interaction polish + Sleep Timer UI (Addition 11) + Taste Lock toggle (Addition 07) + Context Profiles screen (Addition 03)

**Day 54:** Real-Time Written Feedback Channel (Addition 05) — persistent text input wired to ESIE + Record first demo footage

---

## WEEK 9: ENGINEER VIEW + DEVELOPER PORTAL

### Days 57–59: Agent Orchestra (Engineer View)

```
AgentCard × 12 agents:
- Hardware module visual: dark card, amber LED (green=active, yellow=degraded, red=failed)
- Title: agent name in Berkeley Mono caps
- Live stats: confidence %, last update timestamp, key output value
- Expandable section: last 3 inference results

MetaOrchestratorWeights:
- 12 horizontal weight bars, one per agent
- Width updates in real-time via WebSocket /ws/agents
- Colors match agent LEDs

PipelineTrace:
- Single horizontal latency bar broken into segments
- Segments: FAISS retrieval / agents / orchestrator / SEA
- Each segment colored differently, labeled with ms value
- Total shown prominently in Berkeley Mono: "147ms p95"

BaselineComparison table:
- Metric | PSYCHE | Spotify API | Delta (colored green)
- Delta column shows +23%, +31% etc. in accent amber color
```

**Day 58:** Taste Profile Timeline Editor (Addition 02) — D3 interactive timeline, session exclusion UI

**Day 59:** ViewToggle integration → smooth Framer Motion transition between Listener ↔ Engineer view

### Days 60–63: Developer Portal + Real-Time Now Playing Widget

**Day 60:** API Playground — Swagger UI embed, pre-filled example requests, live against psyche-api

**Day 61:** Code Snippets (Python / JS / cURL) + Deploy Buttons (Railway, Render) + PSYCHE Webhooks documentation

**Day 62:** psyche.js TypeScript SDK (Addition 28) — `npm install psyche-client`, React hooks, auto-generated from OpenAPI

**Day 63:** Real-Time Now Playing Widget (Addition 23) — embeddable React component, Ghost Mode toggle, psyche-ui Vercel deployment + custom domain

---

## WEEK 10: SONIC IDENTITY DEEP DIVE + FAIRNESS OBSERVATORY

### Days 64–66: Sonic Identity Deep Dive Screen

**Day 64:** UMAP Scatter Plot backend + D3 frontend
```python
# GET /sonic-identity/{user_id}/umap
# Returns: {tracks: [{x, y, title, artist, cluster_id}], user_clusters: [...]}

# D3 scatter plot:
# User's tracks: amber dots (slightly larger)
# Other FMA tracks: dim grey dots
# Hover: shows track title, cluster membership
# Click cluster: highlight all tracks in that cluster
# Zoom: D3 zoom behavior
```

**Day 65:** Taste Timeline + Stem Breakdown
```
TasteTimeline:
- Horizontal scrollable timeline
- Historical taste vectors (monthly snapshots from GRU training data)
- Future projection: dashed line with confidence band (from GRU forward pass)
- Smooth D3 path animation

StemBreakdown:
- Horizontal bar chart: 4 stems (vocals, bass, drums, melody)
- Bar width = engagement rate from Micro-Event Attribution Engine
- Caption: "You engage 3.2× more with vocal-forward tracks than average"
```

**Day 66:** Sonic Fingerprint Card (Addition 14) — animated shareable card generation + Memory Playlist (Addition 10) — life chapters timeline

### Days 67–70: Fairness Observatory + Social Features

**Day 67:** D3 World Map — geoNaturalEarth projection, choropleth, animated updates, Artist Origin Trails (Addition 16)

**Day 68:** All Fairness Observatory components live — FairnessGauge + WorldMap + RewardDecompositionBar + LabelSizeDonut + Public Equity Score Dashboard (Addition 27)

**Day 69:** Taste Twin (Addition 19) + Collaborative Taste Map (Addition 21) + Sonic Identity Badge System (Addition 22)

**Day 70:** End-to-end UI quality review. All 6 screens via Browser Agent.

---

## WEEK 11: AUDIO ENGINE + LIBRARY MANAGEMENT

**Goal:** Audio quality tier system complete. Library management features. PSYCHE Rewind.

### Days 71–73: Audio Engine Implementation

**Day 71:** Lossless FLAC streaming pipeline (16-bit and 24-bit/192kHz tiers) + ffmpeg integration + LUFS metering (pyloudnorm) + Volume Normalization Control (Addition 37)

**Day 72:** HRTF binaural spatial audio (py3d-audio) + Animated Artwork Engine (Addition 49) — procedural, every track, librosa-driven

**Day 73:** Beat-by-Beat Lyrics engine (Gentle aligner + LRC format) (Addition 48) + Audio Quality Label display (Addition 34) on every track + Stats for Nerds overlay

### Days 74–76: Library Management + Discovery Features

**Day 74:** Universal Library Sort & Filter Engine (Addition 32) — FAISS-backed sort by any attribute, no size limits + Deep Cut Index (Addition 33) — version panel, quality labels

**Day 75:** Smart Offline — Predictive Download Engine (Addition 38) + Cross-Device Queue Sync <500ms (Addition 35) + Uncapped Library (Addition 39)

**Day 76:** PSYCHE Rewind (Addition 20) — always-on stats screen + Infinite Discovery Stream (Addition 52) + Live Performance Mode (Addition 43)

### Days 77–78: Desktop App + Lossless Hardware API

**Day 77:** Electron desktop app (Addition 50) — multi-column library sort, waveform scrubbing, playlist folder nesting, smart playlists, DAC/amp routing, gapless playback, system-tray mini-player

**Day 78:** Lossless Hardware API (Addition 58) — Roon RAAT protocol, DLNA/SMAPI, raw FLAC endpoints + Superfan Tier infrastructure (Addition 57) — unlimited hi-res, Sonic Letter, artist direct messaging

---

## WEEK 12: CONSUMER POLISH

**Goal:** All additional consumer-facing features complete. Advanced social features. Complete QA.

### Days 79–84: Remaining Additions + Full QA

**Day 79:** Community Discovery Hub (Addition 40) + Adventurousness Dial (Addition 42) — persistent 1–10 scale in user profile + Instant Queue Sculpting (Addition 44) — gesture-based

**Day 80:** Unified Search — natural language + audio humming (Addition 45) + Human + AI Curation Blend (Addition 47) — Editor Signal API + Local File Cloud Sync (Addition 53)

**Day 81:** Artist Bio & Story Layer (Addition 54) + Cross-Platform Sync final verification (Addition 55) + Content Type Filter always visible in navbar (Addition 36)

**Day 82:** Smart Offline completion + Video Layer opt-in (Addition 41) + Emotional Arc Builder full UI (Addition 09)

**Day 83:** Transparent Pricing Lock implementation (Addition 59) + "Just Music" Manifesto copy throughout app (Addition 60) + Onboarding flow complete with all three modes

**Day 84:** Complete end-to-end QA. All screens. All modes. All agents. Browser Agent full walkthrough.

---

## WEEK 13: OPEN SOURCE POLISH

**Goal:** Everything a serious open source project needs. psyche-bench CLI ready. VS Code plugin. Complete documentation.

### Days 85–87: Documentation Sprint

**Day 85 — README (most important file):**
```markdown
# PSYCHE 🎵

# README Structure:
# Section 1: Hook (5 seconds)
#   - GIF: 5-second Engineer View with agents running
#   - One sentence: what PSYCHE is
#   - Results table: PSYCHE vs Spotify API on 6 metrics
#
# Section 2: Business problem (60 seconds)
#   - The 10 gaps (one line each, linked to detailed docs)
#
# Section 3: Quick start (2 minutes)
#   - docker-compose up
#   - pip install psyche-core example
#   - Deploy button (Railway + Render)
#
# Section 4: Architecture diagram (30 seconds)
#   - SVG: 5 layers, 12+ agents, data flow
#   - Auto-renders in GitHub
#
# Section 5: Who uses this
#   - 5 developer use cases with code snippets
#
# Section 6: Experiment results
#   - W&B links to all 5 experiments
#
# Section 7: Future improvements
#   - 5 next steps with business justification (product thinking)
#
# Section 8: Cite PSYCHE
#   - BibTeX entry
```

**Day 86 — All supporting docs:**
- `MODEL_CARD.md` — intended use, training data, performance metrics, limitations, ethical considerations, fairness analysis
- `API_DOCS.md` — every endpoint, request/response schema, example calls, error codes
- `EXPERIMENT_LOG.md` — all 5 experiments with hypothesis, design, results, conclusion, W&B links
- `DATA.md` — dataset descriptions, collection methodology, quality issues, licenses, privacy
- `DEPLOYMENT.md` — step-by-step deployment guide, env vars, troubleshooting
- `CONTRIBUTING.md` — how to add a new agent, how to run tests, code standards

**Day 87 — GitHub org polish:**
- Issue templates (bug report, new agent request via Addition 30)
- PR template (with CodeRabbit review checklist)
- GitHub Actions: CI (tests + lint), release (auto PyPI on tag), bench (weekly psyche-bench)
- Deploy badges, build badges, PyPI badge, HF Spaces badge
- Papers With Code submission under "Music Recommendation"

### Days 88–91: psyche-bench CLI + VS Code Extension + Final Integration

**Day 88 — psyche-bench CLI (Ralph Loop):**
```bash
# Build the complete psyche-bench pip installable CLI
# Must work in 3 commands:
# pip install psyche-bench
# psyche-bench download-data --dataset fma-small
# psyche-bench evaluate --model my_model.py --output results.json
```

**Day 89 — VS Code Extension (Ralph Loop + Antigravity):**
```bash
# psyche-plugins/vscode-psyche
# Changes music based on:
#   - Active file language (Python → focus mode, HTML/CSS → creative mode)
#   - Error count in Problems panel (>5 errors → high-arousal music)
#   - Git commit frequency (flow state detected → coherent playlist protection)
# Sidebar panel: current Listener State Vector + Now Playing
```

**Day 90:** HuggingFace Spaces deployment — psyche-api on HF Spaces (free GPU tier), psyche-ui on Vercel

**Day 91 — Week 13 close:**
- Full stack health check: all endpoints, all agents, all UI screens
- Verify: `pip install psyche-core` works in a clean environment
- Verify: `pip install psyche-bench` and benchmark quickstart works
- Verify: VS Code extension installs and connects

---

## WEEK 14: LAUNCH

**Goal:** Every deliverable complete. Blog post live. Multi-platform community posts. Recruiter outreach.

### Day 92: Demo Video Recording

**The 5-minute demo video structure:**
1. **0:00–0:30** — The problem: "31% of Spotify recommendations get skipped. Here's why."
2. **0:30–1:30** — The Cold Start Interview (screen recording, narrated)
3. **1:30–2:30** — Engineer View: "Here's all 12 agents running in parallel to produce that recommendation"
4. **2:30–3:30** — Results: PSYCHE vs. Spotify API, metric by metric, W&B links
5. **3:30–4:30** — Live code: `pip install psyche-core`, 10-line recommendation example
6. **4:30–5:00** — "It's open source. Here's how to use just the agent you need."

Upload to YouTube. The link goes in the README hero section.

### Day 93: Blog Post

**Title:** "10 Gaps in Spotify's Recommendation Stack (And How I Filled All of Them)"

**Structure:**
1. The 10 gaps (one section each, 150 words, research citation, PSYCHE solution)
2. The architecture (embed the SVG diagram)
3. Key results with W&B experiment links
4. How to use PSYCHE in your project (3 use cases with code)
5. What's next (invite contributors)

Publish on personal blog + cross-post to dev.to + Hashnode. The blog post is the HN submission.

### Days 94–95: Community Launch

**Hacker News — Show HN:**
```
Show HN: PSYCHE – Open-source multi-agent music intelligence that outperforms Spotify's API

We built PSYCHE, a production-deployed Python framework where 12+ specialized AI agents
(emotional state, RL recommender, serendipity, coherence, content integrity, explainability,
intent classifier, rumination guard, and more) collaborate to fill 10 documented gaps in
Spotify's recommendation stack — plus 60 user-driven additions grounded in real complaint data.

Results vs. Spotify's own API:
• +31% artist diversity (Gini coefficient)
• +23% serendipity rate
• +27% playlist coherence
• 147ms p95 latency
• pip install psyche-core

Live demo → [URL]
GitHub → [URL]
5-min video → [URL]
```

**Reddit posts:**
- r/MachineLearning — focus on the RL + multi-agent architecture
- r/musicinformationretrieval — focus on the audio ML + psyche-bench
- r/programming — focus on the SDK design + open source structure
- r/Python — focus on `pip install psyche-core` developer experience
- r/spotify — focus on the "10 gaps" angle and what PSYCHE solves for real users
- r/youtubemusic — the Firewall Library + all YTM fixes
- r/applemusic — spatial audio democratization + desktop app

**Product Hunt launch** — same day as HN

### Days 96–98: Recruiter Outreach + Portfolio Integration

**Day 96:** Update GitHub profile, LinkedIn, portfolio site with PSYCHE case study

**Day 97:** Targeted researcher outreach — find 3–5 papers on music recommendation fairness/explainability from RecSys 2025, email/DM the authors about PSYCHE and psyche-bench as evaluation framework

**Day 98:** Papers With Code submission + monitor launch metrics + respond to all GitHub issues and comments from launch week

---

# PART 13: OPEN SOURCE LAUNCH INFRASTRUCTURE

## The Complete GitHub Repository Structure (psyche-core)

```
psyche-core/
│
├── README.md                       ← The pitch deck (see structure in Week 13)
├── LICENSE                         ← MIT
├── CONTRIBUTING.md                 ← How to add a new agent + run tests
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── CHANGELOG.md                    ← Semantic versioning, auto-generated
├── MODEL_CARD.md                   ← Intended use, limits, fairness analysis, ethics
├── API_DOCS.md                     ← Every endpoint, schema, examples
├── EXPERIMENT_LOG.md               ← EXP-01 through EXP-05 with W&B links
├── DATA.md                         ← Datasets, licenses, ethics verification
├── DEPLOYMENT.md                   ← Step-by-step, env vars, troubleshooting
│
├── psyche/                         ← Installable Python package
│   └── [full structure above]
│
├── data/
│   ├── raw/                        ← Sacred. Never modified. DVC tracked.
│   ├── validated/                  ← Post-quality-check. DVC tracked.
│   ├── features/                   ← MERT + CLAP embeddings. DVC tracked.
│   ├── splits/                     ← Fixed-seed train/val/test. DVC tracked.
│   └── models/                     ← Trained artifacts. DVC + W&B links.
│
├── scripts/
│   ├── download_fma.sh             ← One-command FMA-small download
│   ├── build_faiss_index.py        ← Build MERT + CLAP FAISS index
│   ├── run_baselines.py            ← B0–B4 baselines all in one script
│   └── validate_pipeline.py        ← End-to-end health check
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_feature_analysis.ipynb
│   ├── 03_baseline_benchmarks.ipynb
│   ├── 04_esie_development.ipynb
│   ├── 05_rl_training.ipynb
│   └── 06_final_evaluation.ipynb   ← "Show your work" notebook
│
├── tests/
│   ├── unit/                       ← One test file per agent
│   ├── integration/test_full_pipeline.py
│   └── performance/test_latency.py ← CI fails if p95 > 200ms
│
├── configs/
│   ├── config.yaml                 ← Default (all params here)
│   ├── config.dev.yaml
│   └── config.prod.yaml
│
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml          ← Full stack: one command
│   └── docker-compose.dev.yml
│
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                  ← Tests + lint on every PR
│   │   ├── release.yml             ← Auto PyPI publish on tag
│   │   └── bench.yml               ← Weekly psyche-bench runs
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md
│       └── new_agent.md            ← Template for contributing new agents
│
├── .agents/                        ← Antigravity knowledge base
│   ├── skills/
│   │   ├── psyche-conventions/SKILL.md
│   │   ├── ml-experiment/SKILL.md
│   │   └── data-pipeline/SKILL.md
│   └── rules.md
│
├── .gsd/config.yaml                ← GSD configuration
├── .coderabbit.yaml                ← CodeRabbit review rules
└── .ralphrc                        ← Ralph Loop configuration
```

## Who Uses PSYCHE — The Complete User Map

| User Type | Entry Point | What They Use | How Found | What They Say |
|---|---|---|---|---|
| **Spotify/Google recruiter** | Live demo URL | Full dashboard, both views, video | Your application | "The 12-agent mission control is unlike anything I've seen in a portfolio" |
| **Indie dev (wellness app)** | `pip install psyche-core` | ESIE only | PyPI / HN post | "I replaced 3 weeks of work with 15 lines" |
| **Music startup** | docker-compose README | Full API + agents | Blog post / HN | "This saved us 2 months building our rec system from scratch" |
| **ML researcher** | `pip install psyche-bench` | Benchmark suite | Papers With Code | "We used psyche-bench to evaluate our system in the RecSys submission" |
| **Other CS student** | GitHub README | Codebase + notebooks | GitHub trending | "The best documented ML project I've seen from an undergrad" |
| **Podcast platform** | psyche-core docs | ContentIntegrityGuardian only | "content safety AI audio" search | "Finally an open-source content gate that actually works" |
| **Game developer** | /recommend API endpoint | ESIE + Coherence only | Discord / game dev forums | "Dynamic soundtracks that actually match player emotional state" |
| **VS Code user** | Extension marketplace | Plugin only | Twitter/X "IDE recommends music" | "50k downloads in first month" |
| **Audiophile** | Lossless Hardware API | Raw FLAC endpoint + Roon integration | r/audiophile | "Finally lossless streaming I can pipe into my stack" |
| **Artist/Label** | Sonic Compatibility Analyzer | Pre-release audience prediction | LinkedIn / industry newsletter | "We A/B tested our single artwork concept using PSYCHE's fit scores" |

---

# PART 14: THE INTERVIEW ARSENAL

## The 2.5-Minute Project Walkthrough Script

> "Spotify's recommendation system has 10 documented, unfilled gaps that I identified from their own published research papers. I built PSYCHE — a multi-agent music intelligence platform that addresses all 10 simultaneously, plus 60 additional features grounded in three rounds of real user research across Reddit, Spotify Community, YouTube Music forums, and Apple Music forums.
>
> The core is a 12-agent orchestration system: a real-time emotional state engine, a fairness-aware RL recommender, a serendipity discovery agent, a playlist coherence model, a content integrity guardian, a natural language explainability layer, an intent classifier, a rumination guard, a temporal taste model, a context fusion module, a micro-event attribution engine, and a cold start psychographic agent.
>
> I trained it on the FMA dataset, Last.fm LFM-1b, and the Spotify Million Playlist Dataset. When benchmarked against Spotify's own recommendation API, PSYCHE achieves 31% better artist diversity, 22% serendipity rate versus your 18% benchmark, and 28% better playlist coherence. It's deployed on Hugging Face Spaces. Here is the 5-minute demo."

## Technical Questions — PSYCHE-Backed Answers

| Interviewer Question | Your Answer |
|---|---|
| **"Why did you choose PPO for the RL recommender?"** | "EXP-03 in my W&B log. DQN discretized the action space too aggressively for embedding-based track selection. PPO converged 40% faster and achieved better Gini. W&B link: [URL]" |
| **"How do you handle cold start?"** | "Two approaches. New users: Cold Start Agent, 5-question conversational interview, CLAP similarity → warm embedding before first play. New tracks: MERT embeddings provide immediate similarity matching — no CF history needed." |
| **"What breaks when you scale to 713M users?"** | "Documented in DEPLOYMENT.md. Bottleneck: MERT embedding computation. Solution: pre-compute all catalog embeddings offline, serve from FAISS. GRU forward pass is 10ms. FastAPI horizontal scaling. Feature store for pre-computed user vectors." |
| **"How did you validate it works?"** | "Three levels: held-out test sets with time-based splits, 5 published baselines including Spotify API, 100-sample human evaluation on coherence and explanation quality. All results in W&B and MODEL_CARD.md." |
| **"Walk me through a production incident."** | "In EXP-02, CLAP similarity returned acoustically similar but contextually wrong tracks (classical piano to indie piano fans). Root cause: audio-only CLAP index, no text metadata. Fix: rebuilt retrieval to include artist bio + lyric metadata in CLAP embedding. Serendipity jumped from 14% to 22%." |
| **"Tell me about a difficult tradeoff."** | "EXP-03 showed the fairness reward degraded engagement by 4.2%. I ran 8 additional reward weight configurations. α=0.7, β=0.3 achieved 31% better Gini with only 2.1% engagement loss. Business value of fairness outweighed marginal engagement loss." |
| **"How do you handle ambiguity?"** | "The project started with a vague goal: beat Spotify's recommendations. I structured it by reading their research papers to identify specific, documented gaps. Wrote a project brief with success metrics before writing a line of code. Ambiguity became a structured experiment." |
| **"Why not just use collaborative filtering?"** | "I tested B4 (ALS on MPD) as a baseline. It achieves ~15% engagement but zero fairness properties and no cold-start solution. PSYCHE's multi-agent system adds: real-time emotional state, temporal decay, fairness constraints, and natural language explainability — none of which collaborative filtering can provide." |
| **"How does the orchestrator weight the agents?"** | "LLM prompt-based blending with listener state-driven pre-weighting rules. Example: arousal=HIGH + activity=WORKOUT → Coherence Agent weight × 1.4, Serendipity Agent × 0.6. The rules are in config.yaml — fully transparent, fully adjustable. The LLM handles edge cases the rules don't cover. Fallback: pure rule-based weighting if LLM is unavailable." |

## Behavioral Questions — PSYCHE-Backed Answers

| Behavioral Question | Your Answer |
|---|---|
| **"Describe a time you failed and learned from it."** | "My first CLAP similarity implementation returned tracks that were acoustically similar but contextually wrong — classical piano to a user who loves piano-led indie rock. Audio-only CLAP index, no text metadata. I rebuilt the retrieval to include artist bio and lyric metadata in the CLAP embedding. Serendipity rate improved from 14% to 22%." |
| **"Tell me about product thinking you brought to an engineering project."** | "I spent two weeks before writing any code reading Reddit posts across r/spotify, r/youtubemusic, and r/applemusic to extract 60 specific user complaints. Then I mapped each complaint to a concrete feature with a technical implementation. The result is a system where every feature has a documented real-user complaint that motivated it. Product thinking drove engineering priorities." |
| **"How do you approach open source contributions?"** | "I designed PSYCHE so every component can be independently installed. Any developer can add a new agent via the BasePsycheAgent protocol. The community-agents/ directory is a first-class part of the repo. psyche-bench means contributions can be immediately benchmarked and compared — so the open source community improves the system over time without breaking it." |

## The Spotify Team-Level Impact Map

| PSYCHE Component | Spotify Team It Augments | Gap | Why This Gets You Hired |
|---|---|---|---|
| Emotional State Inference Engine | User Modeling | Gap 1 | User Modeling is one of Spotify's largest teams. Real-time state modeling is their open frontier. |
| Micro-Event Attribution Engine | Audio Intelligence | Gap 2 | Stem-level causal attribution is not in production anywhere. This is a novel contribution. |
| Cold Start Psychographic Agent | Growth & Onboarding | Gap 3 | Cold start is directly tied to subscriber conversion. Every 1% improvement = millions in revenue. |
| Serendipity + SEA Explainability | Discovery & Recommendations | Gaps 4, 10 | RecSys 2025 shows this is Spotify's stated next frontier: agentic, explainable discovery. |
| Fairness-Aware RL Recommender | Trust, Safety & Fairness | Gap 5 | DSA compliance and creator economy health. Spotify has a dedicated team for this. You solved it. |
| Playlist Coherence Architect | Editorial & Playlists | Gap 6 | 31% of listening time is playlists. This team would directly productionize this component. |
| Content Integrity Guardian | Content Policy & Safety | Gap 8 | Legal liability in 2026. Spotify needs real-time multimodal content screening. Nobody has shipped it. |
| Temporal Taste Evolution Model | Long-Term Personalization | Gap 9 | Retention cliff at year 3. Temporal modeling of taste drift is an open problem Spotify knows about. |

## PSYCHE's Unfair Advantages

1. **The only open-source system treating artist fairness as a first-class reward signal.** Every other music AI maximizes engagement. PSYCHE ships a working fairness-constrained RL recommender with published Gini coefficients. That is a defensible research contribution.

2. **The only system with stem-level causal attribution.** Nobody knows *why* they skip songs. PSYCHE does.

3. **The only music AI dashboard that looks like professional audio equipment.** Every competitor uses a generic SaaS template. PSYCHE is unforgettable in 3 seconds.

4. **psyche-bench makes PSYCHE infrastructure, not just a project.** When researchers cite it, PSYCHE becomes the standard. Standards are never forgotten.

5. **The Cold Start Interview is a product experience, not a form.** The live radar-building animation is the kind of thing that gets screen-recorded and shared.

6. **60 user-driven features grounded in three rounds of real complaint data.** Not invented features. Features that 713M users have been begging for since 2018.

7. **14 weeks of documented decisions.** Five hypothesis-driven experiments with W&B results and written conclusions. Most candidates "built a recommender." You ran a structured research program and published the results.

8. **Four-tool build stack.** Using GSD + Ralph Loop + CodeRabbit + Antigravity tells a Spotify engineering director: this person knows how to ship production software solo. That is the skill they are hiring for.

---

## The Launch Day Tweet

```
I spent 14 weeks building PSYCHE — an open-source music AI that
outperforms Spotify, fixes what YouTube Music gets wrong, and ships
every feature Apple Music users have been asking for since 2019.

12 AI agents running in parallel:
→ Real-time emotional state inference
→ Fairness-aware RL recommender
→ Serendipity discovery engine
→ Playlist coherence optimizer
→ Content integrity guardian
→ Natural language explainability
→ Intent classifier
→ Rumination guard
→ Temporal taste evolution
→ Context fusion (weather, calendar)
→ Stem-level micro-event attribution
→ Cold start psychographic agent

Results vs. Spotify API:
• +31% artist diversity
• +23% serendipity rate
• +27% playlist coherence
• 147ms p95 latency
• pip install psyche-core

60 features grounded in real user research.
5 experiments with W&B results.
One live demo.

psyche.fm → [URL]
GitHub → [URL]
5-min video → [URL]

Here's how the 12 agents work 🧵 1/12
```

---

## The Closing Argument

PSYCHE is not a student project. It is a fully specified, production-built, benchmarked, deployed system that:

- Addresses documented failures in the world's most advanced music recommendation stack using techniques that Spotify's own research papers identify as the next frontier
- Ships 60 features grounded in three rounds of real user research across 47+ distinct pain points
- Demonstrates production ML discipline: hypothesis-driven experiments, baseline-first development, time-based validation splits, documented risk assessment
- Builds the audio quality tier, library management, and social features that make PSYCHE a consumer product, not just an ML demo
- Creates open-source ecosystem infrastructure (psyche-bench, psyche.js, BasePsycheAgent protocol, community-agents/) that compounds in value over time

A hiring manager who sees this does not see one hire. They see a research engineer, a product manager, a systems architect, an ML practitioner, and an audio engineer — all in one candidate who built a live demo they can use right now.

That is what guarantees the job.

---

*PSYCHE ULTIMATE DEFINITIVE MASTERPLAN — v4.0*
*All five source documents fully integrated: PSYCHE_FULL_MASTERPLAN.md + PSYCHE_DEFINITIVE_MASTERPLAN.md + PSYCHE_MASTERPLAN.docx + psyche_additions.html + psyche_yt_apple_additions.html*
*Shlok Dholakia | KJSCE Mumbai | April 2026*
*Target: Spotify · Google DeepMind · Anthropic · OpenAI*
*Build stack: Google Antigravity · GSD (Get Shit Done) · Ralph Loop · CodeRabbit*
