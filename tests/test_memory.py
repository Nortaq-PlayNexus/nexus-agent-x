from nexus.memory.store import MemoryStore
from nexus.memory.retrieval import MemoryRetrieval
import tempfile, os

def test_memory_add_search():
    db=tempfile.mktemp(suffix=".db")
    s=MemoryStore(db_path=db)
    s.add("I prefer Rust", type="preference", importance=0.9)
    s.add("Python is great", type="semantic")
    r=MemoryRetrieval(db_path=db)
    hits=r.search("Rust preference")
    assert any("Rust" in h["content"] for h in hits)
    os.remove(db)

def test_working_expire():
    db=tempfile.mktemp(suffix=".db")
    s=MemoryStore(db_path=db)
    s.add("temp", type="working")
    s.working_expire(ttl_hours=-1)  # force expire
    assert len(s.list(type="working"))==0
    os.remove(db)
