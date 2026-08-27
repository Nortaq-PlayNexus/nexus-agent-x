"""Task Graph DAG — dependencies, topo sort, critical path (ULTRA §7)."""
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class TaskNode:
    id: str
    title: str
    objective: str = ""
    status: str = "PENDING"  # PENDING|READY|RUNNING|BLOCKED|VERIFYING|DONE|FAILED
    dependencies: List[str] = field(default_factory=list)
    agent: str = "commander"
    tools: List[str] = field(default_factory=list)
    estimate_minutes: int = 5
    risk: str = "LOW"
    verification: Dict = field(default_factory=dict)
    retries: int = 0

class TaskGraph:
    def __init__(self, nodes: List[TaskNode]):
        self.nodes = {n.id: n for n in nodes}

    def ready(self) -> List[TaskNode]:
        """Nodes whose dependencies are DONE."""
        done = {nid for nid, n in self.nodes.items() if n.status == "DONE"}
        return [n for n in self.nodes.values() if n.status == "PENDING" and set(n.dependencies).issubset(done)]

    def topo_sort(self) -> List[TaskNode]:
        """Kahn's algorithm."""
        indeg = {nid: len(n.dependencies) for nid, n in self.nodes.items()}
        adj = {nid: [] for nid in self.nodes}
        for n in self.nodes.values():
            for d in n.dependencies:
                if d in adj: adj[d].append(n.id)
        q = [nid for nid, d in indeg.items() if d == 0]
        order = []
        while q:
            nid = q.pop(0)
            order.append(self.nodes[nid])
            for nb in adj[nid]:
                indeg[nb] -= 1
                if indeg[nb] == 0: q.append(nb)
        if len(order) != len(self.nodes):
            raise ValueError("Cycle detected in task graph")
        return order

    def critical_path(self) -> List[TaskNode]:
        order = self.topo_sort()
        dist = {n.id: n.estimate_minutes for n in order}
        prev = {n.id: None for n in order}
        for n in order:
            for m in self.nodes.values():
                if n.id in m.dependencies:
                    if dist[m.id] < dist[n.id] + m.estimate_minutes:
                        dist[m.id] = dist[n.id] + m.estimate_minutes
                        prev[m.id] = n.id
        end = max(dist, key=lambda k: dist[k])
        path = []
        cur = end
        while cur:
            path.append(self.nodes[cur])
            cur = prev[cur]
        return list(reversed(path))

    def to_dict(self):
        return [n.__dict__ for n in self.nodes.values()]
