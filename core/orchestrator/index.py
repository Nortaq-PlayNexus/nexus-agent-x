"""
NEXUS Agent X — Orchestrator skeleton (Phase 1)
Implements: intent → DAG → permission gate → sandbox → verify → consolidate
See docs/NEXUS-ULTRA-SPEC.md §5, §6, §13
"""
import json, hashlib

def classify_task(user_input: str) -> dict:
    # TODO: call fast model (7B) via Ollama
    return {"intent": "coding", "complexity": 6, "modality": "text"}

def create_dag(intent: dict) -> list[dict]:
    return [
        {"id": "t1", "title": "Plan architecture", "status": "PENDING", "dependencies": [], "agent": "architect", "risk": "LOW"},
        {"id": "t2", "title": "Implement", "status": "PENDING", "dependencies": ["t1"], "agent": "coder", "risk": "MED"},
        {"id": "t3", "title": "Verify build", "status": "PENDING", "dependencies": ["t2"], "agent": "tester", "risk": "LOW", "verification": {"method": "build", "command": "npm run build"}},
    ]

def permission_gate(node: dict, policies: dict) -> bool:
    # TODO: check config/policies.json + Permission Manager
    return True

def execute(node: dict) -> dict:
    # TODO: dispatch to Tool Layer with sandbox
    return {"ok": True, "output": f"executed {node['id']}"}

def verify(node: dict, result: dict) -> dict:
    # TODO: evidence-based verifier — never trust claims
    return {"pass": True, "evidence": 1}

if __name__ == "__main__":
    user_input = "Build a Vite React app and verify the build"
    intent = classify_task(user_input)
    dag = create_dag(intent)
    print(json.dumps({"intent": intent, "dag": dag}, indent=2))
    for node in dag:
        assert permission_gate(node, {})
        result = execute(node)
        v = verify(node, result)
        print(f"{node['id']} verify: {v}")
