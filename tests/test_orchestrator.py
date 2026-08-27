from nexus.core.orchestrator import Orchestrator

def test_orchestrator_run():
    orch=Orchestrator(mode="autopilot")
    res=orch.run("Build a Vite React app and verify the build")
    assert res["status"]=="COMPLETE"
    assert len(res["nodes"])>=2

def test_fast_task():
    orch=Orchestrator(mode="autopilot")
    res=orch.run("Hello")
    assert res["status"]=="COMPLETE"
