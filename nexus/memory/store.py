"""Memory Store — 6 types, SQLite + optional sqlite-vec (ULTRA §12-20)."""
import sqlite3, uuid, json
from datetime import datetime, timedelta

TYPES = ["working","episodic","semantic","procedural","preference","project"]

class MemoryStore:
    def __init__(self, db_path: str = "nexus.db"):
        self.db_path = db_path
        self._ensure()

    def _ensure(self):
        # schema loaded via db/schema.sql at install; ensure tables exist
        try:
            con = sqlite3.connect(self.db_path)
            con.execute("CREATE TABLE IF NOT EXISTS memories (id TEXT PRIMARY KEY, type TEXT, project_id TEXT, content TEXT, embedding BLOB, importance REAL, created_at TEXT, version INT)")
            con.commit(); con.close()
        except Exception: pass

    def add(self, content: str, type: str = "semantic", project_id: str | None = None, importance: float = 0.5) -> str:
        assert type in TYPES, type
        mid = str(uuid.uuid4())
        con = sqlite3.connect(self.db_path)
        con.execute("INSERT INTO memories(id,type,project_id,content,importance,created_at,version) VALUES (?,?,?,?,?,?,1)",
                    (mid, type, project_id, content, importance, datetime.utcnow().isoformat()+"Z"))
        con.commit(); con.close()
        return mid

    def list(self, type: str | None = None, project_id: str | None = None, limit=50):
        q = "SELECT id,type,content,importance,created_at FROM memories WHERE 1=1"
        params=[]
        if type: q+=" AND type=?"; params.append(type)
        if project_id: q+=" AND project_id=?"; params.append(project_id)
        q+=" ORDER BY created_at DESC LIMIT ?"; params.append(limit)
        con=sqlite3.connect(self.db_path)
        rows=con.execute(q, params).fetchall()
        con.close()
        return [{"id":r[0],"type":r[1],"content":r[2],"importance":r[3],"created_at":r[4]} for r in rows]

    def forget(self, mem_id: str):
        con=sqlite3.connect(self.db_path)
        con.execute("DELETE FROM memories WHERE id=?",(mem_id,)); con.commit(); con.close()

    def working_expire(self, ttl_hours=1):
        cutoff=(datetime.utcnow()-timedelta(hours=ttl_hours)).isoformat()+"Z"
        con=sqlite3.connect(self.db_path)
        con.execute("DELETE FROM memories WHERE type='working' AND created_at < ?", (cutoff,)); con.commit(); con.close()
