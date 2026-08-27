"""Vision Perception — screenshot → OCR → semantic screen (ULTRA §11)."""
import pathlib

class VisionPerception:
    def screenshot(self, path="screenshot.png"):
        # stub: in prod use mss + PIL
        return {"path": path, "size": [1920,1080]}

    def to_semantic(self, screenshot) -> dict:
        # stub: would call vision model (LLaVA/Qwen-VL)
        return {"windows": [{"title":"VS Code","bounds":[0,0,1920,1080],"elements":[{"role":"button","label":"Build","bounds":[120,80,180,40]}]}]}

    def find(self, semantic, label: str):
        for w in semantic.get("windows",[]):
            for e in w.get("elements",[]):
                if e.get("label")==label: return e
        return None
