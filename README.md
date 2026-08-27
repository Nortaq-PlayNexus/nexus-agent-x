<div align="center">

# NEXUS Agent X

**Local Autonomous AI Operating System — Ollama is the cortex. NEXUS is the body, memory, and civilization.**

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-%3E%3D3.11-3776AB?logo=python&logoColor=white)](https://python.org)
[![Local-First](https://img.shields.io/badge/Local--First-100%25-00C853?logo=ollama)](https://ollama.com)
[![Offline](https://img.shields.io/badge/Offline-Capable-FF6D00)](docs/NEXUS-ULTRA-SPEC.md)

</div>

**NEXUS Agent X** is a local-first AI platform that turns a modest Ollama model into a full autonomous operating system. Not a chatbot — a **reasoning, planning, remembering, verifying, learning machine that operates your computer while remaining controllable and transparent.**

No cloud. No vendor lock-in. Zero data leaving your machine unless you explicitly allow it.

> Ported and upgraded 10000X from the original `kjg.txt` blueprint (88 sections, ~35k chars) → **ULTRA v2.0 implementation-ready spec** with contracts, DDL, and executable skeletons.

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

# Inspect the ULTRA spec (the upgraded kjg.txt)
cat docs/NEXUS-ULTRA-SPEC.md

# Database — create SQLite + vector index
sqlite3 nexus.db < db/schema.sql

# Config — edit model profiles & policies
cat config/models.json
cat config/policies.json

# Run orchestrator skeleton (Phase 1)
python core/orchestrator/index.py --task "Build a Vite React app and verify the build"
```

---

## Project structure

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
├── scheduler/  plugins/  ui/{desktop,web,cli}/  voice/  vision/
├── config/  db/  docs/  tools/manifest/
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
