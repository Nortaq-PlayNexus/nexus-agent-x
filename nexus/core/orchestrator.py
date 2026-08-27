"""Orchestrator — state machine THINKING→PLANNING→EXECUTING→VERIFYING→LEARNING (ULTRA §83, §27)."""
from .task_graph import TaskGraph, TaskNode
from .bus import EventBus
from nexus.security.permissions import PermissionManager
import uuid, time

STATES = ["IDLE","THINKING","PLANNING","EXECUTING","OBSERVING","VERIFYING","LEARNING","COMPLETE","ERROR"]

class Orchestrator:
    def __init__(self, mode: str = "assistant", bus: EventBus | None = None):
        self.mode = mode
        self.bus = bus or EventBus()
        self.perm = PermissionManager()
        self.state = "IDLE"

    def _transition(self, to: str):
        assert to in STATES, to
        self.state = to
        self.bus.emit("TASK_STARTED", {"state": to})

    def plan(self, user_input: str) -> TaskGraph:
        self._transition("PLANNING")
        # Minimal heuristic planner — replace with LLM planner in production
        if "website" in user_input.lower() or "vite" in user_input.lower():
            nodes = [
                TaskNode(id="research", title="Research stack", objective="Choose stack", agent="researcher", tools=["knowledge.search"]),
                TaskNode(id="design", title="Design", objective="Wireframe + schema", agent="architect", dependencies=["research"]),
                TaskNode(id="code", title="Code", objective="Implement", agent="coder", dependencies=["design"], tools=["filesystem.write","terminal.exec"]),
                TaskNode(id="test", title="Test & Verify", objective="Build passes", agent="tester", dependencies=["code"], tools=["terminal.exec"], verification={"method":"build","command":"npm run build"}),
            ]
        else:
            nodes = [TaskNode(id="t1", title=user_input[:40], objective=user_input, agent="commander", tools=["filesystem.read"])]
        g = TaskGraph(nodes)
        self.bus.emit("PLAN_CREATED", {"nodes": g.to_dict()})
        return g

    def execute_node(self, node: TaskNode) -> dict:
        self._transition("EXECUTING")
        # Permission gate
        for tool in node.tools:
            decision = self.perm.check(tool)
            if decision == "deny":
                return {"ok": False, "error": f"Permission denied for {tool}"}
            if decision == "ask" and self.mode == "assistant":
                # In assistant mode, log ask — real UI would modal
                self.bus.emit("TOOL_CALLED", {"tool": tool, "decision": "ask", "node": node.id})
        self.bus.emit("TOOL_CALLED", {"tool": node.tools, "node": node.id})
        # Simulated execution — wire to real tools in Phase 4
        time.sleep(0.01)
        return {"ok": True, "output": f"Executed {node.id}"}

    def verify(self, node: TaskNode, result: dict) -> dict:
        self._transition("VERIFYING")
        # Evidence-based — check verification contract
        if node.verification.get("method") == "build":
            # stub: would run node.verification["command"] and check exit code + artifacts
            passed = result.get("ok", False)
        else:
            passed = result.get("ok", False)
        if not passed:
            self.bus.emit("VERIFICATION_FAILED", {"node": node.id, "result": result})
        return {"pass": passed, "confidence": 0.92 if passed else 0.31}

    def run(self, user_input: str) -> dict:
        self._transition("THINKING")
        graph = self.plan(user_input)
        for node in graph.topo_sort():
            node.status = "RUNNING"
            result = self.execute_node(node)
            v = self.verify(node, result)
            if v["pass"]:
                node.status = "DONE"
                self.bus.emit("TASK_COMPLETED", {"node": node.id})
            else:
                node.status = "FAILED"
                if node.retries < 3:
                    node.retries += 1
                    node.status = "PENDING"  # replan
                else:
                    self._transition("ERROR")
                    return {"status": "FAILED", "node": node.id, "verification": v}
        self._transition("LEARNING")
        # consolidation stub
        self.bus.emit("MEMORY_CREATED", {"task": user_input})
        self._transition("COMPLETE")
        return {"status": "COMPLETE", "nodes": graph.to_dict()}

    def run_with_retry(self, user_input: str, budget: int = 3):
        for attempt in range(budget):
            res = self.run(user_input)
            if res["status"] == "COMPLETE": return res
        return res
