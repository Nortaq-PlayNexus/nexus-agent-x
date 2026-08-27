"""Memory Retrieval — scoring relevance+importance+recency+frequency+project (ULTRA §19)."""
import math, sqlite3
from datetime import datetime

def _recency_score(created_at: str) -> float:
    try:
        dt=datetime.fromisoformat(created_at.replace("Z","+00:00"))
        days=(datetime.utcnow().replace(tzinfo=dt.tzinfo)-dt).total_seconds()/86400
        return math.exp(-days/30)  # 30-day decay
    except Exception: return 0.5

class MemoryRetrieval:
    def __init__(self, db_path="nexus.db"):
        self.db_path=db_path

    def search(self, query: str, topk=8, project_id=None):
        # TF-IDF stub — replace with vector cosine when sqlite-vec available
        con=sqlite3.connect(self.db_path)
        rows=con.execute("SELECT id,type,content,importance,created_at,project_id FROM memories").fetchall()
        con.close()
        scored=[]
        q_terms=set(query.lower().split())
        for r in rows:
            content=r[2] or ""
            relevance=len(q_terms & set(content.lower().split())) / max(1,len(q_terms))
            importance=r[3] or 0.5
            recency=_recency_score(r[4] or "")
            project_match=1.0 if r[5]==project_id else (0.5 if project_id is None else 0.2)
            # frequency stub 0.5
            score=0.35*relevance + 0.20*importance + 0.15*recency + 0.15*0.5 + 0.15*project_match
            if score>=0.35:  # threshold lower for stub
                scored.append({"id":r[0],"type":r[1],"content":content,"score":score,"importance":importance})
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:topk]
