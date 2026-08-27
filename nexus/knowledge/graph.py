"""Knowledge Graph — lightweight entity/relation store (ULTRA §30)."""
import sqlite3, json, uuid

class KnowledgeGraph:
    def __init__(self, db_path="nexus.db"):
        self.db_path=db_path
        self._ensure()
    def _ensure(self):
        try:
            con=sqlite3.connect(self.db_path)
            con.execute("CREATE TABLE IF NOT EXISTS kg_nodes (id TEXT PRIMARY KEY, label TEXT, type TEXT)")
            con.execute("CREATE TABLE IF NOT EXISTS kg_edges (id TEXT PRIMARY KEY, src TEXT, dst TEXT, rel TEXT)")
            con.commit(); con.close()
        except Exception: pass
    def add_entity(self, label, type="concept"):
        nid=str(uuid.uuid4()); con=sqlite3.connect(self.db_path); con.execute("INSERT INTO kg_nodes VALUES (?,?,?)",(nid,label,type)); con.commit(); con.close(); return nid
    def add_relation(self, src, dst, rel):
        eid=str(uuid.uuid4()); con=sqlite3.connect(self.db_path); con.execute("INSERT INTO kg_edges VALUES (?,?,?,?)",(eid,src,dst,rel)); con.commit(); con.close(); return eid
    def neighbors(self, label):
        con=sqlite3.connect(self.db_path); rows=con.execute("SELECT dst,rel FROM kg_edges JOIN kg_nodes n ON n.id=src WHERE n.label=?",(label,)).fetchall(); con.close(); return rows
