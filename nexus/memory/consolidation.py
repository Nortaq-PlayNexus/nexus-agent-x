"""Memory Consolidation — extract facts → dedup → version (ULTRA §20)."""
from .store import MemoryStore

def consolidate(raw_trace: str, project_id=None, store: MemoryStore | None = None):
    store=store or MemoryStore()
    # stub: extract first sentence as fact
    fact=raw_trace.strip().split("\n")[0][:500] if raw_trace else ""
    if not fact: return None
    # dedup stub: check existing
    existing=store.list(limit=100)
    for e in existing:
        if e["content"]==fact: return e["id"]
    return store.add(fact, type="episodic", project_id=project_id, importance=0.7)
