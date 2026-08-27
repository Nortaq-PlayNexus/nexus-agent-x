"""Tool Registry — manifest validation + dispatch (ULTRA §10)."""
import json, pathlib

class ToolRegistry:
    def __init__(self, manifest_dir="tools/manifest"):
        self.dir=pathlib.Path(manifest_dir)
        self.tools={}
        if self.dir.exists():
            for f in self.dir.glob("*.json"):
                try: self.tools[f.stem]=json.loads(f.read_text(encoding="utf-8"))
                except Exception: pass

    def get(self, name: str): return self.tools.get(name)
    def list(self): return list(self.tools.keys())
    def validate(self, name: str, args: dict) -> bool:
        m=self.get(name)
        if not m: return False
        for req in m.get("parameters",{}).get("required",[]):
            if req not in args: return False
        return True
