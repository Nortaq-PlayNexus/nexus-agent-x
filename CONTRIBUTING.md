# Contributing to NEXUS Agent X

We follow PlayNexus repo standards (same as neuralforge/swarmforge/archon).

## Setup

```bash
pip install -e ".[dev]"
make db
pytest
```

## PRs

- Branch from `main`, conventional commits (`feat:`, `fix:`, `docs:`)
- `ruff check` + `pytest` must pass (CI enforces)
- Add tests for new tools/agents
- Update `docs/` if behavior changes

## Golden tasks

Every PR must not regress:

1. Remember preference across restart
2. Create Vite app, build, fix error, verify PASS
3. Summarize PDF via ingestion → vector → cited summary
4. Click Build button in screenshot → semantic → verified
5. Schedule daily 9am: check git status

Run: `pytest -k golden` (when golden tests added)
