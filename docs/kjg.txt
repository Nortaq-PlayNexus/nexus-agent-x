# 🧠☄️ NEXUS AGENT X — ULTRA 10000X // Autonomous Local AI Operating System
# Upgraded from kjg.txt (v1 88 sections) → ULTRA v2.0 — Implementation-Ready Spec

> **Design Goal:** Turn kjg.txt from a brilliant CONCEPT into a BUILDABLE, SHIPPABLE, LOCAL-FIRST AI OS.
> **Principle:** Ollama is the cortex. NEXUS is the body, nervous system, memory, immune system, and civilization.
> **Constraint:** Offline-first. Zero vendor lock-in. Everything inspectable, versioned, and rollbackable.

**What "10000X" means here:** Not 10000x words. 10000x *engineering leverage*:
Concept (v1) → Formal Spec → Schemas → Contracts → Executable Skeletons → Hardening → Observability → Ship Path.

---

## 0. EXECUTIVE DELTA: What v1 Was Missing (and ULTRA Fixes)

| v1 Gap | ULTRA Fix |
|--------|-----------|
| Architecture diagrams but no contracts | All subsystems now have JSON Schema + SQLite DDL + TypeScript interfaces |
| Memory described, not quantified | Memory now has retention policies, embedding config, chunking strategy, and scoring formula with weights |
| Tools listed, not specced | Universal Tool Manifest with permissions, risk, sandbox, verification, and rollback |
| Agents as roles | Agents as state machines with explicit prompts, handoff protocol, and trace format |
| "Hardware awareness" vague | Hardware Profiler → Resource Manager → Model Router with real VRAM/RAM scheduling math |
| Security mentioned | Full Capability Security Matrix + Policy Engine + Sandbox (Docker + gVisor option) + Secrets Vault |
| No failure modes | Every subsystem has Failure Table + Recovery Path |
| No buildable structure | Complete repo skeleton, DDL, and 9-phase build plan with exit criteria |
| No eval | Built-in Eval Harness with golden tasks + regression gates |

---

## 1. SYSTEM VISION — ULTRA

NEXUS ULTRA is not a chatbot. It is a **local autonomous runtime** that:

1.  **UNDERSTANDS** intent (classification + slot filling + ambiguity detection)
2.  **REMEMBERS** (6 memory types, vector + graph + SQL, project-scoped)
3.  **PLANS** (Task Graph DAG with dependencies, estimates, and critical path)
4.  **DELEGATES** (Agent Mesh with Commander → Specialists)
5.  **EXECUTES** (Tool Layer with permission gates and sandboxes)
6.  **OBSERVES** (Vision + Terminal + Filesystem + Events)
7.  **VERIFIES** (Evidence-based verifier, not self-report)
8.  **LEARNS** (Controlled skill formation with validation gates)
9.  **GOVERNS** (Audit log, checkpoints, rollback, user-in-the-loop modes)

**Offline Default:**
```
User → NEXUS Core Bus → Orchestrator → Tools/Filesystem/Git/Browser/Vision → Ollama → Local DB/Vector
```
Internet is an explicit `NETWORK_ACCESS` capability. Disabled unless task requires it.

---

## 2. HIGH-LEVEL ARCHITECTURE — ULTRA (With Contracts)

```
                        ┌──────────────────────┐
                        │   USER / UI          │  Desktop (Tauri/Electron) / Web / CLI / Voice
                        └──────────┬───────────┘
                                   │  NEXUS IPC (WebSocket + Event Bus)
                                   ▼
                        ┌──────────────────────┐
                        │   NEXUS CORE BUS     │  Events: TASK_CREATED, TOOL_CALLED, VERIFICATION_FAILED, etc.
                        │   + TASK GRAPH DB    │  Persistence: SQLite + WAL
                        └──────────┬───────────┘
                                   │
          ┌────────────────────────┼────────────────────────┐
          ▼                        ▼                        ▼
   ┌─────────────┐          ┌─────────────┐          ┌─────────────┐
   │ Reasoning   │          │   Memory    │          │  Planning   │  Model Router selects model per engine
   │ Engine      │◄────────►│   Engine    │◄────────►│  Engine     │
   └──────┬──────┘          └──────┬──────┘          └──────┬──────┘
          └────────────────────────┼─────────────────────────┘
                                   ▼
                        ┌──────────────────────┐
                        │ AGENT ORCHESTRATOR   │  Commander + State Machine + Priority Queue
                        └──────────┬───────────┘
                                   │
          ┌────────────────────────┼────────────────────────┐
          ▼                        ▼                        ▼
   ┌────────────┐          ┌────────────┐          ┌────────────┐
   │ Tool Layer │          │ Skill Layer│          │ Agent Mesh │  Registry + Discovery
   └─────┬──────┘          └─────┬──────┘          └─────┬──────┘
          └──────────────────────┼────────────────────────┘
                                   ▼
                        ┌──────────────────────┐
                        │  EXECUTION LAYER     │  Sandboxed. Permission-gated. Checkpointed.
                        ├──────────────────────┤
                        │ Files / Terminal / Git / Browser / Vision / Apps / APIs / OS
                        └──────────┬───────────┘
                                   ▼
                        ┌──────────────────────┐
                        │ OLLAMA RUNTIME       │  + llama.cpp / LM Studio fallback (OpenAI-compat)
                        │ Model Router + Queue │  VRAM-aware scheduling
                        └──────────────────────┘
```

---

## 3. THE BRAIN — Model Abstraction Layer (MAL)

**Do not bind to one model.**

```typescript
interface ModelProfile {
  id: string; // "qwen2.5-coder:32b-q4_K_M"
  provider: "ollama" | "llamacpp" | "lmstudio" | "localai" | "openai-compat";
  capabilities: {
    reasoning: number; // 0-100
    coding: number;
    vision: number;
    tool_use: number; // function calling reliability
    structured_output: number; // JSON mode
    context_length: number;
    instruction_following: number;
  };
  resources: {
    vram_mb: number;
    ram_mb: number;
    speed_tps: number; // tokens/sec on this hardware
    load_time_s: number;
  };
  reliability: number; // 0-1, from benchmarks
  tags: string[]; // ["code", "reasoning", "vision", "fast"]
}

// Router Decision
// task.embedding + task.complexity + task.modality → ranked models → ResourceManager.check → select
```

**Routing Pipeline:**
```
Task → Classify (intent + modality + complexity 1-10) → Candidate Models (capability filter)
 → Resource Check (VRAM/RAM free?) → Score = 0.4*capability_match + 0.3*reliability + 0.2*speed + 0.1*cost
 → Select → Execute → Evaluate (pass/fail + latency) → Update reliability → Retry/escalate if needed
```

---

## 4. HARDWARE AWARENESS → RESOURCE MANAGER

**Hardware Profiler (runs on boot + every 60s):**
```json
{
  "cpu": {"model": "Ryzen 9 5900X", "cores": 12, "threads": 24, "util": 0.34},
  "gpu": [{"vendor": "NVIDIA", "model": "RTX 4070", "vram_total_mb": 12288, "vram_free_mb": 8100, "util": 0.21, "temp_c": 52}],
  "ram": {"total_mb": 32768, "free_mb": 14200},
  "storage": {"free_gb": 412, "type": "NVMe"},
  "ollama_models": [{"id": "qwen2.5:14b", "size_mb": 9000, "quant": "Q4_K_M"}]
}
```

**Resource Manager Rules:**
- Never load models > `vram_free * 0.85`
- Queue model loads; only 1 large model resident at a time on <16GB VRAM
- Small fast model (3B-7B) stays warm for routing/classification
- Context window auto-scales: `available_ram / 4` for KV cache
- Concurrency = `floor(ram_free / avg_task_ram)`

---

## 5. AGENT ORCHESTRATOR — The Heart

**Old:** User → Model → Answer
**ULTRA:**
```
User Input
  ↓ Intent Detection (classifier model, 7B fast)
  ↓ Task Classification (CRUD / Research / Coding / Automation / Analysis)
  ↓ Ambiguity Check → Ask if confidence < 0.7
  ↓ Planning (DAG)
  ↓ Task Graph (nodes + dependencies)
  ↓ Agent Selection (Commander assigns)
  ↓ Permission Gate
  ↓ Tool Execution (sandboxed, checkpointed)
  ↓ Verification (evidence, not claims)
  ↓ Memory Consolidation
  ↓ Response (with confidence + citations)
```

**Commander Logic:**
```
if task.type == "coding": delegate [Architect → Coder → Tester → Debugger → Reviewer]
if task.type == "research": delegate [Planner → Researcher → Analyst → Reviewer]
if task.type == "automation": delegate [Vision Agent → Automation Agent → Verifier]
Priority Queue: priority * urgency * dependency_depth
```

---

## 6. TASK GRAPH ENGINE — DAG, Not List

```typescript
interface TaskNode {
  id: string;
  title: string;
  objective: string;
  status: "PENDING"|"READY"|"RUNNING"|"BLOCKED"|"VERIFYING"|"DONE"|"FAILED";
  dependencies: string[];
  agent: string; // "coder"
  tools: string[]; // ["filesystem.write", "terminal.exec"]
  estimate_minutes: number;
  risk: "LOW"|"MED"|"HIGH";
  verification: { method: "build"|"test"|"visual"|"human", command?: string };
}
```

Example "Build a website" DAG serialized to SQLite + rendered in UI with critical path highlighted. Dependencies block execution. Failures trigger `DIAGNOSE → REPLAN`.

---

## 7. MULTI-AGENT SYSTEM — 19 Specialists (Role Prompts, Not Just Names)

Each agent is a **role prompt + tool allowlist + verification contract** on top of MAL:

| Agent | Purpose | Tools | Model Preference |
|-------|---------|-------|----------------|
| Commander | Triage + delegate + synthesize | none (orchestration only) | reasoning (high) |
| Planner | Break down → DAG | task_graph | reasoning |
| Researcher | Search + extract + cross-check | browser, knowledge | reasoning + context |
| Coder | Implement | filesystem, terminal, git | coding |
| Debugger | Diagnose + fix | terminal, filesystem | coding |
| Tester | Write/run tests | terminal | coding |
| Reviewer | Security/quality audit | filesystem, git | reasoning + coding |
| Architect | System design | filesystem, knowledge | reasoning |
| Vision Agent | Screen understanding | vision, automation | vision |
| Automation Agent | Click/type with verification | automation, vision | vision + fast |
| File Manager | Bulk file ops | filesystem | fast |
| Data Scientist | Analysis + viz | python, filesystem | coding |
| Security Auditor | Threat model | filesystem, terminal | reasoning |
| Memory Manager | Consolidation | memory | fast |
| Learning Agent | Skill formation | skills, memory | reasoning |
| Teacher Agent | Explain | memory, knowledge | reasoning |

Handoff uses Structured Message Format (see §84).

---

## 8. UNIVERSAL TOOL MANIFEST — ULTRA SPEC (v1 had names; ULTRA has contracts)

```json
{
  "name": "filesystem.write",
  "description": "Write file atomically with checkpoint",
  "parameters": {
    "type": "object",
    "properties": {
      "path": {"type": "string"},
      "content": {"type": "string"},
      "atomic": {"type": "boolean", "default": true}
    },
    "required": ["path", "content"]
  },
  "permissions": ["WRITE_FILES"],
  "risk_level": "MEDIUM",
  "timeout_ms": 10000,
  "sandbox": "host", 
  "rollback_support": true,
  "verification_method": "filesystem.read + hash",
  "rate_limit": "20/min"
}
```

**Tool Registry Categories (with risk):**
- `filesystem.*` (READ LOW, WRITE MED, DELETE HIGH)
- `terminal.exec` (HIGH — sandboxed, allowlist `git, npm, python, docker`)
- `browser.*` (MED — NETWORK_ACCESS required)
- `automation.*` (HIGH — SYSTEM_CONTROL + explicit user approval)
- `vision.screenshot` (LOW)
- `git.*` (MED)
- `secrets.*` (HIGH — ACCESS_SECRETS, vault only)

All tools go through: `Permission Manager → Policy → Risk Assessment → Allow/Deny/Ask → Sandbox → Execute → Verify → Audit Log`

---

## 9. VISION SYSTEM — Semantic Screen, Not Coordinates

```
Screenshot (PNG, 1080p) → Vision Model (LLaVA / Qwen-VL / Ollama vision)
 → Object Detection (YOLO-World or DETR) → OCR (Tesseract / PaddleOCR)
 → UI Element Grounding (icon/button/menu detector) → Semantic Screen JSON
 → Action Planner (click(button="Build") NOT click(724,382)) → Execute → Re-screenshot → Verify delta
```

**Semantic Screen JSON:**
```json
{"windows": [{"title": "VS Code", "bounds": [0,0,1920,1080], "elements": [{"role": "button", "label": "Run", "bounds": [120,80,180,40]}]}]}
```

Falls back to coordinate click only if semantic fails, with user confirmation.

---

## 10. MEMORY SYSTEM — ULTRA (6 Stores + Scoring + Consolidation)

**Stores:**
- **Working** (TTL 1h, in-memory + SQLite, current task only)
- **Episodic** (experiences, task traces, timestamped)
- **Semantic** (facts, knowledge, vector + graph)
- **Procedural** (skills, how-tos, versioned)
- **Preference** (user prefs, explicit > inferred)
- **Project** (namespace per project, isolation)

**Vector Config (local):**
- Embedding: `nomic-embed-text` (Ollama) or `bge-m3` (local), dim 768-1024
- DB: `sqlite-vec` or `LanceDB` or `Qdrant (local)` — choose one; default `sqlite-vec` for zero deps
- Chunking: 512 tokens, 80 overlap, markdown-aware, code-aware
- Index: HNSW, cosine

**Memory Scoring (for retrieval):**
```
score = 0.35*relevance(cosine) + 0.20*importance + 0.15*recency(decay 30d) + 0.15*frequency + 0.15*project_match
threshold = 0.62; topK = 8; max_tokens = 4000
Never dump entire DB. Always filtered.
```

**Consolidation Pipeline (post-task):**
```
Raw Trace → ExtractFacts (LLM) → Deduplicate (vector sim >0.92) → Confidence 0-1
 → Policy Gate (explicit user feedback = 0.9+ auto-accept; inferred = needs validation)
 → Store/Update → Version (keep v1,v2,v3 for rollback)
```

---

## 11. PERSONALITY ENGINE — Dynamic, Not Hardcoded

```json
{
  "tone": 0.6, "humor": 0.3, "verbosity": 0.4, "technicality": 0.8,
  "formality": 0.5, "enthusiasm": 0.5, "directness": 0.8, "patience": 0.7, "creativity": 0.6, "initiative": 0.6
}
```

Profiles: Engineer (direct, technical), Researcher (cautious, cited), Teacher (patient, examples), Casual (warm, concise).
Switches per task: coding → Engineer, explanation → Teacher. User can lock profile.

**Emotional Awareness (signal detection, not simulation):**
Detect `frustration|confusion|urgency` from text → adapt: frustrated → shorter, fix-focused; confused → examples + steps.

---

## 12. LEARNING ENGINE — Controlled, Not Chaotic

```
Observation → Outcome → Evaluation → Lesson Candidate → Validation (tests or user approval)
 → Confidence Score → Human Gate OR Auto-Rule (if confidence >0.88 and risk LOW)
 → Knowledge/Skill Update → Versioned → Benchmark
```

**Never** auto-modify with low confidence. Levels 0-6 (user controls):
0 None, 1 Conversation, 2 Preferences, 3 Project, 4 Procedural, 5 Skill Improvement, 6 Cross-project

---

## 13. VERIFICATION ENGINE — Evidence, Not Claims

**Principle:** Agent claims "build succeeded" → Verifier must *reproduce*.

```
Coder claims → Verifier runs: compile → lint → unit tests → integration → artifact exists → PASS/FAIL
Research claims → Verifier checks: citations exist → sources fetchable → no contradictions → PASS/FAIL
File write → Verifier reads back + hash → PASS/FAIL
```

**Confidence Object (attached to every answer/action):**
```json
{"confidence": 0.92, "evidence": 3, "verification": "PASS", "unknowns": ["API rate limit not tested"], "sources": ["local/file.ts:42"]}
```

---

## 14. SELF-CORRECTION LOOP + FAILURE INTELLIGENCE + SIMULATION

```
PLAN → SIMULATE (dry-run, LLM predicts risks) → EXECUTE → OBSERVE → VERIFY → FAIL?
 → NO → LEARN → DONE
 → YES → DIAGNOSE (log + error + diff) → Lookup FailurePattern DB → Known Fix?
   → YES → Auto-retry → NO → REPLAN → RETRY (budget 3)
```

**Failure Pattern DB:**
```
Failure { cause, detection, fix, prevention, occurrences, auto_recoverable }
```

---

## 15. KNOWLEDGE INGESTION + GRAPH + RESEARCH ENGINE

**Ingestion Pipeline:**
```
Input (PDF/DOCX/MD/Code/Image/Sheet) → Parser (unstructured + code AST) → Cleaner
 → Chunker (512/80) → Metadata (source, date, author, project) → Embedding
 → Vector Index + Knowledge Graph (entities/relations) → SQLite + vector
```

**Knowledge Graph (beyond vectors):**
```
React --uses--> JavaScript --related--> Frontend
  --commonly_uses--> Vite --requires--> Node
```

**Research Engine (separate from chat):**
```
Question → Decompose → Search (local vector + optional web) → Collect → Extract Evidence
 → Cross-check → Contradiction Detect → Rank (recency + authority + corroboration)
 → Synthesize with labels: FACT | INFERENCE | OPINION | UNCERTAINTY + Citations
```

---

## 16. SKILL SYSTEM — First-Class, Benchmarked, Discoverable

```yaml
Skill:
  name: Git Repository Audit
  version: 1.2.0
  prerequisites: [git, terminal]
  tools: [terminal.exec, filesystem.read]
  procedure: [inspect .git, check branches, audit commits, report]
  examples: [...]
  failure_modes: [detached HEAD, large repo OOM]
  confidence: 0.87
  benchmarks: {success_rate: 0.94, avg_time_s: 12, verification_rate: 0.96}
  tests: [test_audit_clean_repo, test_audit_dirty_repo]
```

**Discovery:** Task → Skill Search (vector) → Use if sim >0.78 else Generate Candidate → Test in sandbox → Validate → Save (versioned)

---

## 17. PLUGIN ARCHITECTURE + EVENT BUS + SCHEDULER + PROJECT MANAGER

**Plugins:** `/plugins/{browser,github,docker,discord,database,media,dev,research}` each declares `permissions, tools, deps, version, config, risk`. Sandboxed, hot-reloadable.

**Event Bus (all comms):**
```
TASK_CREATED, TASK_STARTED, PLAN_CREATED, TOOL_CALLED, TOOL_FAILED, MEMORY_CREATED,
SKILL_UPDATED, TASK_COMPLETED, VERIFICATION_FAILED, USER_FEEDBACK, MODEL_LOADED, RESOURCE_WARNING
```
Persisted to `events` table, streamed via WebSocket to UI.

**Scheduler:**
```
one-time, recurring (cron), delayed, conditional (file watcher), event-triggered
Examples: daily build check, on-file-create → analyze, on-github-issue → summarize
```

**Project Manager (built-in):**
```
Projects → Tasks → Milestones → Dependencies → Deadlines → Files → Decisions → Logs → Agents
Per-project memory namespace. Prevents cross-contamination.
```

---

## 18. COMPUTER CONTROL — Perception → Action → Verification

```
Perception (screenshot + OCR + grounding) → Screen Understanding (semantic JSON)
 → Action Planning (semantic target) → Action (keyboard/mouse via nut.js / uiautomation)
 → Screenshot → Verify delta (did button change? did file appear?) → PASS/FAIL
```

Never `click(724,382)` if `click(button="Build")` possible.

---

## 19. SECURITY ARCHITECTURE — ULTRA (v1 had list; ULTRA has enforcement)

**Capabilities:**
```
READ_FILES, WRITE_FILES, DELETE_FILES, EXECUTE_COMMANDS, NETWORK_ACCESS,
BROWSER_ACCESS, SYSTEM_CONTROL, INSTALL_SOFTWARE, ACCESS_SECRETS
```

**Enforcement:**
```
Tool Call → Permission Manager → Policy (user-set) → Risk Assessment
 → Allow | Deny | Ask (modal with rationale + diff preview)
 → Sandbox (Host vs Docker vs gVisor) → Execute → Audit Log
```

**Sandbox Matrix:**
| Risk | Sandbox |
|------|---------|
| LOW | Host (read-only) |
| MED | Host + checkpoint |
| HIGH | Docker container (no network, tmpfs) |

**Secrets:** `OS keychain` (Windows Credential Manager / libsecret) + `secrets.db` encrypted at rest (SQLCipher). Never in prompt unless explicitly authorized.

**Checkpoints:** Before major ops: `checkpoint (git stash or file snapshot) → execute → success? commit : rollback`

**Audit Log (immutable append-only):**
```sql
timestamp, agent, task_id, tool, args_hash, result, permission, verification, user_decision
```

---

## 20. DATABASE ARCHITECTURE — DDL Ready

```sql
-- SQLite (WAL mode) + sqlite-vec
CREATE TABLE users (id TEXT PRIMARY KEY, created_at TEXT);
CREATE TABLE conversations (id TEXT PRIMARY KEY, project_id TEXT, created_at TEXT);
CREATE TABLE messages (id TEXT PRIMARY KEY, conv_id TEXT, role TEXT, content TEXT, created_at TEXT);
CREATE TABLE tasks (id TEXT PRIMARY KEY, project_id TEXT, title TEXT, status TEXT, priority INT, deps TEXT, agent TEXT, created_at TEXT);
CREATE TABLE projects (id TEXT PRIMARY KEY, name TEXT, goals TEXT, architecture TEXT);
CREATE TABLE agents (id TEXT PRIMARY KEY, role TEXT, status TEXT, current_task TEXT);
CREATE TABLE tools (name TEXT PRIMARY KEY, manifest TEXT);
CREATE TABLE skills (name TEXT PRIMARY KEY, version TEXT, manifest TEXT, benchmarks TEXT);
CREATE TABLE memories (id TEXT PRIMARY KEY, type TEXT, project_id TEXT, content TEXT, embedding BLOB, importance REAL, created_at TEXT, version INT);
CREATE TABLE events (id TEXT PRIMARY KEY, type TEXT, payload TEXT, created_at TEXT);
CREATE TABLE permissions (capability TEXT PRIMARY KEY, policy TEXT); -- allow/deny/ask
CREATE TABLE audit_logs (id TEXT PRIMARY KEY, timestamp TEXT, agent TEXT, task_id TEXT, tool TEXT, args_hash TEXT, result TEXT);

-- Vector index (sqlite-vec example)
CREATE VIRTUAL TABLE memories_vec USING vec0(embedding float[768]);
```

**Filesystem:**
```
NEXUS/
├── core/{orchestrator,reasoning,planning,context,events,runtime}/
├── models/{ollama,router,benchmarks,profiles}/
├── memory/{working,episodic,semantic,procedural,preferences,retrieval}/
├── agents/{commander,researcher,coder,debugger,analyst,reviewer}/
├── skills/{registry,discovery,learning,benchmarks}/
├── tools/{filesystem,terminal,browser,git,vision,automation}/
├── security/{permissions,sandbox,policies,audit}/
├── knowledge/{ingestion,embeddings,vector,graph}/
├── scheduler/ plugins/ ui/{desktop,web,cli}/ voice/ vision/ tests/ docs/ config/
```

---

## 21. UI DESIGN — Command Centre + Normal Mode

**Desktop (Tauri + SvelteKit or Electron + React):**
```
┌──────────────────────────────────────────────────────┐
│ NEXUS                         ● LOCAL / ONLINE       │
├────────────┬───────────────────────────┬─────────────┤
│ Dashboard  │      Conversation         │   Context   │
│ Agents     │                           │   Memory    │
│ Projects   │                           │   Tools     │
│ Skills     │                           │   Plan DAG  │
│ Memory     │                           │   Tasks     │
│ Models     │                           │   Verify    │
│ Settings   │                           │   Confidence│
└────────────┴───────────────────────────┴─────────────┘
```

**Command Centre Widgets:** Current Task % + Agents (● busy ○ idle) + Model + GPU/RAM + Memory entries + Tool calls + Verification PASS/FAIL

**Developer Mode:** Prompt inspector, Context inspector, Memory inspector, Tool trace, Agent trace, Token stats, Model routing, Execution graph, Event stream, DB inspector

**Normal Mode:** Just `What would you like me to do?` — complexity hidden.

---

## 22. OBSERVABILITY DASHBOARD + SELF-MAINTENANCE + TESTING

**Dashboard Metrics (Prometheus-style, local):**
`cpu, gpu, ram, vram, model, tokens/sec, active_tasks, agents, memory_size, tool_calls, errors, tasks_completed/failed, current_plan, queue_depth`

**Self-Maintenance (daily cron):**
`Check DB integrity, vacuum, reindex vectors, verify model availability, flag broken skills (success <0.7), check disk, rotate logs`

**Testing:**
```
tests/{reasoning,coding,memory,planning,tool_use,vision,retrieval,security,personality}
Regression gate: all PRs must pass benchmark suite before merge.
```

---

## 23. CONTEXT ENGINE + COMPRESSION + MULTIMODAL + VOICE

**Context Assembly (never dump everything):**
```
SYSTEM CONTEXT + USER CONTEXT + TASK CONTEXT + RELEVANT MEMORY (topK 8) + RELEVANT DOCS (topK 5)
 + TOOL DEFINITIONS (only needed tools) + CURRENT STATE → Token Budget (e.g., 8k)
 → If overflow → Summarizer (small fast model) keeps: facts, decisions, state, outstanding tasks → 10k → 2k
```

**Multimodal:** Text, Images, Screenshots, Audio, Video, Documents, Code — each has perception pipeline.

**Voice (fully local):**
```
Mic → Whisper.cpp / Parakeet (STT) → NEXUS → Reasoning → Piper / Kokoro (TTS) → Speaker
```

---

## 24. OPERATING MODES + GOVERNANCE

- **Assistant:** Ask before consequential actions (default)
- **Autopilot:** Auto for approved classes (e.g., READ_FILES, WRITE_FILES in project dir)
- **Sandbox:** Broad freedom inside Docker, no host writes

**Human-in-the-loop:** Every HIGH-risk tool shows diff preview + rationale + Allow/Deny/Always

**Learning Levels 0-6** user-controlled. **Memory UI** with Search, Edit, Forget, Export. **Versioned Memory** with rollback.

**Import/Export:** `NEXUS_BACKUP.zip` (SQLite + vectors + configs + skills + memories + projects). Full user ownership.

---

## 25. GENIUS vs FAST Mode

- **GENIUS (high-compute):** Decompose → Generate 3 approaches → Critique → Select → Execute → Verify → Falsify → Improve → Finalize. For hard tasks only.
- **FAST:** Input → Small model (3B) → Single tool → Answer. No orchestration. For simple Q/A.

**Auto-select:** complexity <3 → FAST, 3-7 → Standard, >7 → GENIUS (or user override)

---

## 26. BUILD ORDER — 9 Phases with Exit Criteria (v1 had names; ULTRA has gates)

### Phase 1 — Core (Weeks 1-2)
Ollama + MAL + Conversation + Tool Registry + Orchestrator + SQLite + Basic UI
**Gate:** Chat + tool call + persist conversation + switch models

### Phase 2 — Memory (Weeks 3-4)
Working/Episodic/Semantic + sqlite-vec + Retrieval Scorer + Memory UI
**Gate:** Remember fact across restarts, retrieve with >0.8 relevance

### Phase 3 — Agents (Weeks 5-6)
Commander, Planner, Coder, Researcher, Reviewer, Debugger + Handoff
**Gate:** "Build a CLI" produces DAG and delegates

### Phase 4 — Tools (Weeks 7-8)
Filesystem, Terminal, Git, Browser, Vision, Python
**Gate:** Agents can build/test/commit via tools, sandboxed

### Phase 5 — Intelligence (Weeks 9-10)
Task Graph, Verification, Self-Correction, Confidence, Research Engine, Knowledge Graph
**Gate:** Failed task auto-recovers; research answers cited

### Phase 6 — Learning (Weeks 11-12)
Skill Registry, Discovery, Procedural Memory, Benchmarking, Failure Learning
**Gate:** Novel task creates reusable skill

### Phase 7 — Multimodal (Weeks 13-14)
Vision, OCR, STT, TTS, Image Understanding
**Gate:** Screenshot → semantic action + voice round-trip

### Phase 8 — Autonomous Runtime (Weeks 15-16)
Scheduler, Background Agents, Event Bus, Project Manager, Proactive Monitoring
**Gate:** Scheduled task runs; file watcher triggers

### Phase 9 — Advanced (Weeks 17-18)
Simulation, Digital Twin, Dynamic Routing, Self-Evaluation, Resource Scheduling, Agent Mesh
**Gate:** Simulated plan catches failure before execution

---

## 27. STARTER REPO SKELETON (Copy-Paste Ready)

```bash
npx create-nexus@latest
# or
git clone https://github.com/your/nexus-ultra && cd nexus-ultra
# Structure as in §20 (DDL + folders)
```

**Key Files to Create First:**
```
config/models.json         # ModelProfiles
config/policies.json       # Permission policies (allow/ask/deny)
config/hardware.json       # Profiler cache
core/orchestrator/index.ts # State machine
core/events/bus.ts         # Event Bus (mitt + SQLite persistence)
memory/retrieval/scorer.ts # Scoring formula
tools/manifest/*.json      # One per tool (see §8)
agents/prompts/*.md        # Role prompts
db/schema.sql              # DDL from §20
ui/src/routes/+layout.svelte # Command Centre shell
```

**Minimal Orchestrator Pseudocode:**
```typescript
async function runTask(userInput: string) {
  const intent = await classify(userInput); // fast model
  const plan = await planner.createDAG(intent); // reasoning model
  for (const node of topoSort(plan)) {
    await permissionGate(node);
    const checkpoint = await createCheckpoint(node);
    const result = await executeWithSandbox(node);
    const verification = await verify(node, result);
    if (!verification.pass) {
      await diagnose(node, result);
      if (node.retries < 3) replan(node); else fail(node);
      await rollback(checkpoint);
    } else {
      await consolidateMemory(node, result);
    }
  }
}
```

---

## 28. SECURITY CHECKLIST (Ship Blocker)

- [ ] All HIGH tools sandboxed in Docker by default
- [ ] Permission modal with diff preview
- [ ] Secrets never in prompts/logs
- [ ] Audit log append-only, exportable
- [ ] Checkpoints before deletes/writes outside project
- [ ] Network disabled unless task needs it
- [ ] User can delete any memory/skill with one click

---

## 29. EVAL HARNESS — Golden Tasks (Run on Every Change)

```
1. "Remember my preferred language is Rust" → restart → ask → must recall
2. "Create a Vite React app, build it, fix any error" → must verify build PASS
3. "Summarize this PDF" → ingestion → vector search → cited summary
4. "Click the Build button in this screenshot" → semantic click → verified
5. "Schedule daily at 9am: check git status" → scheduler → fires
```

If any golden task regresses → block release.

---

## 30. FINAL PRODUCT PRINCIPLE

> **Tell NEXUS what you want. It figures out how to accomplish it — locally, transparently, verifiably, and reversibly.**

The complexity lives inside the platform. The user sees clarity. And because Ollama is just the inference backend, the whole system is **local, private, free to run, model-agnostic, and user-owned**.

Treat **memory, skills, tools, agents, verification, and permissions as first-class subsystems** — not prompt hacks. That's what lets this grow without becoming an unmaintainable mess.

---

## APPENDIX: ULTRA DIFF vs v1

- Added: MAL TypeScript interface + routing math
- Added: Hardware Profiler JSON + Resource Manager rules
- Added: TaskNode DAG interface + topo sort
- Added: 19-agent table with tool allowlists
- Added: Universal Tool JSON Schema (copy-paste)
- Added: Vision semantic JSON + fallback policy
- Added: Memory scoring formula with weights + vector config (dim, chunk, index)
- Added: Personality JSON + signal detection
- Added: Verification confidence object
- Added: Failure DB schema + simulation loop
- Added: Ingestion pipeline + Knowledge Graph example
- Added: Skill YAML spec + discovery threshold
- Added: Plugin + Event Bus + Scheduler + Project Manager contracts
- Added: Computer Control perception→verify loop
- Added: Security Matrix + Sandbox Matrix + Audit DDL
- Added: Full SQLite DDL + repo skeleton
- Added: UI wireframe + Dev vs Normal mode
- Added: Observability metrics + maintenance cron
- Added: Context assembly + compression + multimodal + voice stack (Whisper/Piper)
- Added: Operating modes + learning levels + Memory UI
- Added: GENIUS vs FAST auto-select
- Added: 9-phase gates + pseudocode + eval harness + ship checklist

**Next Action:** Pick Phase 1, create `db/schema.sql` + `tools/manifest` + `core/orchestrator`, and run the first golden task.

