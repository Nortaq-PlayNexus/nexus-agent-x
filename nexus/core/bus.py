"""Event Bus — all subsystems communicate via typed events (ULTRA §36)."""
from collections import defaultdict
from datetime import datetime
import json, sqlite3, uuid, pathlib

EVENTS = [
    "TASK_CREATED","TASK_STARTED","PLAN_CREATED","TOOL_CALLED","TOOL_FAILED",
    "MEMORY_CREATED","SKILL_UPDATED","TASK_COMPLETED","VERIFICATION_FAILED","USER_FEEDBACK",
    "MODEL_LOADED","RESOURCE_WARNING"
]

class EventBus:
    def __init__(self, db_path: str = "nexus.db"):
        self.db_path = db_path
        self._handlers = defaultdict(list)

    def on(self, event_type: str, handler):
        self._handlers[event_type].append(handler)

    def emit(self, event_type: str, payload: dict):
        assert event_type in EVENTS or event_type.startswith("CUSTOM_"), f"Unknown event {event_type}"
        evt = {"id": str(uuid.uuid4()), "type": event_type, "payload": payload, "created_at": datetime.utcnow().isoformat()+"Z"}
        # persist
        try:
            con = sqlite3.connect(self.db_path)
            con.execute("INSERT INTO events(id,type,payload,created_at) VALUES (?,?,?,?)",
                        (evt["id"], evt["type"], json.dumps(evt["payload"]), evt["created_at"]))
            con.commit(); con.close()
        except Exception:
            pass
        for h in self._handlers[event_type]:
            try: h(evt)
            except Exception: pass
        return evt

    def history(self, limit=50):
        try:
            con = sqlite3.connect(self.db_path)
            rows = con.execute("SELECT type, payload, created_at FROM events ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
            con.close()
            return rows
        except Exception:
            return []
