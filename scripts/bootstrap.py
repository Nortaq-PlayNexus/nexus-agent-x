#!/usr/bin/env python
"""Bootstrap NEXUS DB + verify Ollama connectivity."""
import sqlite3, pathlib, requests

db=pathlib.Path("nexus.db")
schema=pathlib.Path("db/schema.sql")
if schema.exists():
    con=sqlite3.connect(str(db)); con.executescript(schema.read_text(encoding="utf-8")); con.commit(); con.close()
    print(f"DB ready: {db}")
try:
    r=requests.get("http://127.0.0.1:11434/api/tags", timeout=2)
    print(f"Ollama: {r.status_code} {len(r.json().get('models',[]))} models")
except Exception as e:
    print(f"Ollama not reachable (expected offline): {e}")
