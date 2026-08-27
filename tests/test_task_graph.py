from nexus.core.task_graph import TaskGraph, TaskNode

def test_topo_sort():
    nodes=[TaskNode(id="a",title="a"), TaskNode(id="b",title="b",dependencies=["a"]), TaskNode(id="c",title="c",dependencies=["b"])]
    g=TaskGraph(nodes)
    order=[n.id for n in g.topo_sort()]
    assert order==["a","b","c"]

def test_cycle_detection():
    nodes=[TaskNode(id="a",title="a",dependencies=["b"]), TaskNode(id="b",title="b",dependencies=["a"])]
    g=TaskGraph(nodes)
    try:
        g.topo_sort(); assert False, "should raise"
    except ValueError as e: assert "Cycle" in str(e)

def test_critical_path():
    nodes=[TaskNode(id="a",title="a",estimate_minutes=5), TaskNode(id="b",title="b",dependencies=["a"],estimate_minutes=10), TaskNode(id="c",title="c",dependencies=["a"],estimate_minutes=2)]
    g=TaskGraph(nodes)
    cp=g.critical_path()
    assert cp[0].id=="a" and cp[-1].id=="b"
