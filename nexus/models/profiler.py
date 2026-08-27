"""Hardware Profiler — inspect CPU/GPU/RAM/VRAM to auto-configure (ULTRA §5)."""
import platform, json, pathlib

try:
    import psutil
except ImportError:
    psutil = None  # type: ignore

try:
    import GPUtil  # optional
except ImportError:
    GPUtil=None

class HardwareProfiler:
    def profile(self) -> dict:
        if psutil is None:
            # Fallback when psutil not installed (CI minimal)
            return {
                "cpu": {"model": platform.processor() or platform.machine(), "cores": 4, "threads": 8, "util": 0.0},
                "ram": {"total_mb": 16384, "free_mb": 8192, "util": 50.0},
                "storage": {"free_gb": 100, "type": "NVMe"},
                "gpu": []
            }
        mem=psutil.virtual_memory()
        disk=psutil.disk_usage("/")
        data={
            "cpu": {"model": platform.processor() or platform.machine(), "cores": psutil.cpu_count(logical=False), "threads": psutil.cpu_count(logical=True), "util": psutil.cpu_percent(interval=0.2)},
            "ram": {"total_mb": mem.total//1024//1024, "free_mb": mem.available//1024//1024, "util": mem.percent},
            "storage": {"free_gb": disk.free//1024//1024//1024, "type": "NVMe"},
            "gpu": []
        }
        if GPUtil:
            try:
                for g in GPUtil.getGPUs():
                    data["gpu"].append({"vendor":"NVIDIA","model":g.name,"vram_total_mb":int(g.memoryTotal),"vram_free_mb":int(g.memoryFree),"util":g.load,"temp_c":g.temperature})
            except Exception: pass
        return data

    def recommend(self, profile: dict | None = None) -> dict:
        p=profile or self.profile()
        ram_free=p["ram"]["free_mb"]
        vram_free=p["gpu"][0]["vram_free_mb"] if p["gpu"] else 0
        return {
            "concurrency": max(1, ram_free//4000),
            "context_window": min(32768, ram_free//4 * 256),
            "max_model_vram_mb": int(vram_free*0.85) if vram_free else 6000,
            "keep_small_model_warm": True
        }
