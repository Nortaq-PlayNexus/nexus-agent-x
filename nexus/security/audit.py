"""Audit Log — append-only (ULTRA §43)."""
import sqlite3, uuid, hashlib, json
from datetime import datetime

class AuditLog:
    def __init__(self, db_path="nexus.db"):
        self.db_path=db_path

    def log(self, agent: str, task_id: str, tool: str, args: dict, result: dict, permission: str, verification: str):
        aid=str(uuid.uuid4())
        h=hashlib.sha256(json.dumps(args, sort_keys=True).encode()).hexdigest()[:16]
        try:
            con=sqlite3.connect(self.db_path)
            con.execute("INSERT INTO audit_logs(id,timestamp,agent,task_id,tool,args_hash,result) VALUES (?,?,?,?,?,?,?)",
                        (aid, datetime.utcnow().isoformat()+"Z", agent, task_id, tool, h, json.dumps(result)[:2000]))
            con.commit(); con.close()
        except Exception: pass
        return aid
