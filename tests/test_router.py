from nexus.models.router import ModelRouter

def test_router_select(tmp_path=None):
    r=ModelRouter(config_path="config/models.json")
    assert len(r.profiles)>=2
    task={"need":{"coding":1.0}, "type":"coding"}
    sel=r.select(task)
    assert sel is not None
    assert "id" in sel
