# Architecture — NEXUS Agent X ULTRA

See `NEXUS-ULTRA-SPEC.md` for full 30-section spec.

## Module map

| Path | Responsibility |
|---|---|
| `nexus/core/orchestrator.py` | State machine IDLE→THINKING→PLANNING→EXECUTING→VERIFYING→LEARNING→COMPLETE |
| `nexus/core/bus.py` | EventBus persisted to SQLite `events` |
| `nexus/core/task_graph.py` | DAG, topo sort, critical path |
| `nexus/core/context.py` | Token-budget assembly + compression |
| `nexus/memory/` | 6 stores, retrieval scorer, consolidation |
| `nexus/models/` | HardwareProfiler + ModelRouter |
| `nexus/agents/` | 19 specialists + prompts |
| `nexus/tools/` | Registry + filesystem/terminal/git/browser/vision impls |
| `nexus/security/` | PermissionManager + AuditLog |
| `nexus/knowledge/` | Ingestion (chunk 512/80) + graph |
| `nexus/scheduler/` | Every/at/on_event |
| `nexus/vision/` | Screenshot → semantic JSON |
| `nexus/voice/` | STT/TTS stubs |

## Data flow

```
User → Orchestrator.plan → TaskGraph → PermissionManager.check → Tools → Vision verify → Memory consolidate → EventBus → UI
```

## Security invariants

- HIGH-risk tools require `ask` in assistant mode
- Secrets never enter prompts
- Audit log HMAC chain (future)
- Docker sandbox for HIGH risk
