"""Permission Manager — capability gates (ULTRA §40)."""
import json, pathlib

CAPABILITIES=["READ_FILES","WRITE_FILES","DELETE_FILES","EXECUTE_COMMANDS","NETWORK_ACCESS","BROWSER_ACCESS","SYSTEM_CONTROL","INSTALL_SOFTWARE","ACCESS_SECRETS"]

TOOL_TO_CAP={
    "filesystem.read":"READ_FILES","filesystem.write":"WRITE_FILES","filesystem.delete":"DELETE_FILES",
    "terminal.exec":"EXECUTE_COMMANDS","browser.search":"NETWORK_ACCESS","browser.navigate":"BROWSER_ACCESS",
    "automation.click":"SYSTEM_CONTROL","automation.type":"SYSTEM_CONTROL",
}

class PermissionManager:
    def __init__(self, policy_path="config/policies.json"):
        self.policy_path=pathlib.Path(policy_path)
        self.policies=self._load()

    def _load(self):
        if self.policy_path.exists():
            try: return json.loads(self.policy_path.read_text(encoding="utf-8")).get("policies",{})
            except Exception: pass
        return {c:"ask" for c in CAPABILITIES}

    def check(self, tool: str) -> str:
        cap=TOOL_TO_CAP.get(tool, "EXECUTE_COMMANDS")
        return self.policies.get(cap, "ask")
