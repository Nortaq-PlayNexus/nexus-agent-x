# API — NEXUS Agent X

## CLI

```bash
nexus run --task "Build a Vite app" --mode autopilot
nexus memory search "Rust" --topk 5
nexus serve --host 127.0.0.1 --port 8000
nexus --help
```

## Python

```python
from nexus.core.orchestrator import Orchestrator
orch = Orchestrator(mode="assistant")
res = orch.run("Summarize docs/kjg.txt")
print(res)

from nexus.memory.store import MemoryStore
store = MemoryStore()
store.add("pref: verbose=false", type="preference")

from nexus.models.router import ModelRouter
router = ModelRouter()
print(router.select({"need":{"coding":1.0}}))

from nexus.core.task_graph import TaskGraph, TaskNode
g = TaskGraph([TaskNode(id="a",title="a")])
print(g.topo_sort())
```

## REST (stub, `nexus serve`)

- `POST /run {task, mode}` → orchestrator result
- `GET /events` → SSE stream
- `GET /memory/search?q=` → hits
- `GET /health` → profiler + queue depth
