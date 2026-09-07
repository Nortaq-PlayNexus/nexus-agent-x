<p align="center">
  <img src="https://img.shields.io/badge/NEXUS-LOCAL%20AI%20OS-B8FF1E?style=flat-square&labelColor=0a0e1a" alt="nexus" />
</p>

# NEXUS :: LOCAL AI OPERATING SYSTEM

**Ollama is the cortex. NEXUS is the body, memory, and civilization.** A local-first autonomous AI platform that turns a modest model into a reasoning, planning, remembering, verifying, learning machine — controllable and transparent.

<p align="center">
  <img src="https://img.shields.io/badge/PYTHON-%3E%3D3.11-ffc430?style=flat-square&logo=python&logoColor=ffc430&labelColor=0a0e1a" alt="python"/>
  <img src="https://img.shields.io/badge/AGENTS-19-B8FF1E?style=flat-square&labelColor=0a0e1a" alt="agents"/>
  <img src="https://img.shields.io/badge/TOOLS-16-3dd5ff?style=flat-square&labelColor=0a0e1a" alt="tools"/>
  <img src="https://img.shields.io/badge/VERSION-2.1.0-00E5FF?style=flat-square&labelColor=0a0e1a" alt="version"/>
  <img src="https://img.shields.io/badge/LOCAL-FIRST-100%25-B8FF1E?style=flat-square&labelColor=0a0e1a" alt="local"/>
  <a href="LICENSE"><img src="https://img.shields.io/badge/LICENSE-MIT-ff3b3b?style=flat-square&labelColor=0a0e1a" alt="license"/></a>
</p>

<pre>
IDENT ......... NEXUS-01
CLASS ......... AUTONOMOUS AI OPERATING SYSTEM
STATUS ........ ONLINE / ACTIVE
CORTEX ........ OLLAMA
MESH .......... 19 SPECIALISTS · 16 TOOLS
LINK .......... /nexus-agent-x
</pre>

---

## // 01 :: SIGNAL

**NEXUS Agent X** is a local-first AI platform that turns a modest Ollama model into a full autonomous operating system. Not a chatbot — a **reasoning, planning, remembering, verifying, learning machine that operates your computer while remaining controllable and transparent.**

No cloud. No vendor lock-in. Zero data leaving your machine unless you explicitly allow it.

> Ported and upgraded **10000X → 1000X** from the original `kjg.txt` blueprint (88 sections, ~35k chars) → **ULTRA v2.1 implementation-ready OS** — now with executable Python package, 19 agent prompts, 16 tool manifests, and 8 passing tests.

---

## What it does

| Capability | Description |
|---|---|
| **Reasoning + Planning** | Intent detection → Task Graph DAG with dependencies, critical path, and verification gates |
| **Memory** | 6 stores (Working/Episodic/Semantic/Procedural/Preference/Project) + vector + graph, project-scoped |
| **Multi-Agent Mesh** | 19 specialists (Commander, Planner, Coder, Reviewer, Vision, etc.) as role prompts with handoff protocol |
| **Tool Layer** | Universal Tool Manifest with permissions, risk levels, sandboxing, and rollback |
| **Vision** | Semantic screen understanding — `click(button="Build")` not `click(724,382)` |
| **Verification** | Evidence-based verifier; agent claims must be reproduced |
| **Learning** | Controlled skill formation with confidence gates and versioning |
| **Security** | Capability matrix (READ_FILES → ACCESS_SECRETS), policy engine, Docker/gVisor sandbox, audit log |
| **Offline-First** | Works with no internet: chat, code, files, RAG, vision, voice, automation |

---

## Architecture

```
User / UI (Desktop/Web/CLI/Voice)
        ↓  NEXUS Core Bus (Event + Task Graph)
Reasoning ↔ Memory ↔ Planning
        ↓
Agent Orchestrator (Commander → Specialists)
        ↓
Tool Layer | Skill Layer | Agent Mesh
        ↓
Execution Layer (Files/Terminal/Browser/Git/Vision/Apps)
        ↓
Ollama Runtime (Model Router + VRAM-aware Queue)
```

See full spec: [`docs/NEXUS-ULTRA-SPEC.md`](docs/NEXUS-ULTRA-SPEC.md) — 30 sections, DDL, TypeScript interfaces, and failure tables.

---

## Quick start

```bash
# Clone
git clone https://github.com/Nortaq-PlayNexus/nexus-agent-x.git
cd nexus-agent-x

# Install (editable)
pip install -e ".[dev]"

# Bootstrap DB + check Ollama
python scripts/bootstrap.py
# or
make db

# Run via CLI (new in v2.1)
nexus run --task "Build a Vite React app and verify the build" --mode autopilot
nexus memory search "Rust" --topk 5
nexus version

# Legacy skeleton still works
python core/orchestrator/index.py --task "Build a Vite React app and verify the build"

# Tests (8 passed)
pytest -q

# Docker
docker compose up --build
# or with Ollama sidecar
docker compose --profile with-ollama up
```

---

## Project structure

```
nexus-agent-x/
├── nexus/                      # Python package (pip install -e .)
│   ├── core/ {orchestrator,bus,task_graph,context}
│   ├── memory/ {store,retrieval,consolidation}
│   ├── models/ {router,profiler}
│   ├── agents/ {registry + 19 prompts in agents/prompts/}
│   ├── tools/ {registry}
│   ├── security/ {permissions,audit}
│   ├── knowledge/ {ingestion,graph}
│   ├── scheduler/ vision/ voice/
│   └── cli.py (typer: nexus run/serve/memory)
├── agents/prompts/             # 19 markdown role prompts
├── tools/manifest/             # 16 JSON tool contracts
├── config/ {models,policies,hardware}.json
├── db/schema.sql               # SQLite WAL + permissions seed
├── plugins/{browser,github}/
├── ui/{index.html,app.js}      # Command Centre stub
├── tests/ (8 tests)  examples/  scripts/bootstrap.py
├── .github/workflows/ci.yml  Dockerfile  docker-compose.yml  Makefile
└── docs/{NEXUS-ULTRA-SPEC.md,ARCHITECTURE.md,API.md}
```

Matches the recommended structure in [`docs/NEXUS-ULTRA-SPEC.md:284`](docs/NEXUS-ULTRA-SPEC.md).

---

## Build order — 9 phases with exit gates

| Phase | Scope | Gate |
|---|---|---|
| 1 — Core | Ollama + Model Router + Tool Registry + Orchestrator + SQLite + UI | Chat + tool call + persist + model switch |
| 2 — Memory | Working/Episodic/Semantic + sqlite-vec + scorer + Memory UI | Recall across restart with >0.8 relevance |
| 3 — Agents | Commander, Planner, Coder, Researcher, Reviewer, Debugger | "Build a CLI" produces DAG and delegates |
| 4 — Tools | Filesystem, Terminal, Git, Browser, Vision, Python | Agents build/test/commit sandboxed |
| 5 — Intelligence | Task Graph, Verification, Self-Correction, Research Engine | Failed task auto-recovers; citations present |
| 6 — Learning | Skill Registry, Discovery, Procedural Memory | Novel task creates reusable skill |
| 7 — Multimodal | Vision, OCR, STT (Whisper.cpp), TTS (Piper) | Screenshot → semantic action + voice round-trip |
| 8 — Autonomous | Scheduler, Background Agents, Event Bus, Project Manager | Scheduled task fires; file watcher triggers |
| 9 — Advanced | Simulation, Digital Twin, Dynamic Routing, Resource Scheduling | Simulated plan catches failure before execution |

See [`docs/NEXUS-ULTRA-SPEC.md:330`](docs/NEXUS-ULTRA-SPEC.md) for full gates + pseudocode.

---

## Security

Capabilities: `READ_FILES, WRITE_FILES, DELETE_FILES, EXECUTE_COMMANDS, NETWORK_ACCESS, BROWSER_ACCESS, SYSTEM_CONTROL, INSTALL_SOFTWARE, ACCESS_SECRETS`

Every tool call: `Permission Manager → Policy (allow/deny/ask) → Risk Assessment → Sandbox (Host/Docker/gVisor) → Execute → Verify → Audit Log`

- Secrets in OS keychain (Windows Credential Manager), never in prompts
- Checkpoints before destructive ops (git stash / file snapshot → rollback on fail)
- Audit log is append-only, exportable

---

## Evaluation — Golden tasks (run on every change)

```bash
pytest tests/ -k golden
# 1. Remember preference across restart
# 2. Create Vite app, build, fix error, verify PASS
# 3. Summarize PDF via ingestion → vector → cited summary
# 4. Click Build button in screenshot → semantic click → verified
# 5. Schedule daily 9am: check git status → fires
```

If any golden task regresses → block release.

---

## Standards

Consistent with PlayNexus repos (`neuralforge`, `swarmforge`, `archon`, `sentinel`):

- **License:** MIT © 2026 PlayNexus
- **Python:** ≥3.11, `pyproject.toml` with `setuptools`, `rich`, `pyyaml`
- **Docs:** Centered header + badges + features + quick start + structure
- **Git:** Conventional commits, `main` branch, PR template-ready

---

## Original

- `kjg.txt` — original 88-section blueprint (backed up as `docs/kjg.BACKUP.txt` if present)
- `docs/NEXUS-ULTRA-SPEC.md` — ULTRA 10000X upgrade (this repo's source of truth)

---

## License

MIT — see [LICENSE](LICENSE)
