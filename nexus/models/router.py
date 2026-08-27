"""Model Router — selects model per task using capability + resource scoring (ULTRA §4)."""
import json, pathlib

class ModelRouter:
    def __init__(self, config_path="config/models.json", profiler=None):
        self.config_path=config_path
        self.profiler=profiler
        self.profiles=self._load()

    def _load(self):
        p=pathlib.Path(self.config_path)
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8"))
        return []

    def score(self, task: dict, profile: dict) -> float:
        caps=profile.get("capabilities",{})
        need=task.get("need",{})
        # capability_match
        match=0
        for k in ["reasoning","coding","vision"]:
            if k in need:
                match+= caps.get(k,0) * need[k]
        match/=100 if need else 50
        reliability=profile.get("reliability",0.8)*100
        speed=profile.get("resources",{}).get("speed_tps",30)
        return 0.4*match + 0.3*reliability + 0.2*speed

    def select(self, task: dict):
        if not self.profiles: return None
        # filter by VRAM if profiler available
        if self.profiler:
            rec=self.profiler.recommend()
            max_vram=rec["max_model_vram_mb"]
            candidates=[p for p in self.profiles if p.get("resources",{}).get("vram_mb",0) <= max_vram]
            if candidates: pool=candidates
            else: pool=self.profiles
        else: pool=self.profiles
        ranked=sorted(pool, key=lambda p: self.score(task,p), reverse=True)
        return ranked[0]

    def classify_task(self, text: str) -> dict:
        t=text.lower()
        if any(w in t for w in ["code","build","fix","compile","test"]): return {"type":"coding","need":{"coding":1.0,"reasoning":0.6},"complexity":6}
        if any(w in t for w in ["research","summarize","analyze","pdf"]): return {"type":"research","need":{"reasoning":1.0},"complexity":5}
        if any(w in t for w in ["click","screenshot","automate"]): return {"type":"automation","need":{"vision":1.0},"complexity":7}
        return {"type":"general","need":{"reasoning":0.7},"complexity":3}
