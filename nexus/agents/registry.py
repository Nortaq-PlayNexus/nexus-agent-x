"""Agent Registry — 19 specialists with tool allowlists + prompts (ULTRA §8-9)."""
import pathlib, json

AGENTS = [
    {"id":"commander","role":"Commander","purpose":"Triage + delegate + synthesize","tools":[],"model_pref":"reasoning"},
    {"id":"planner","role":"Planner","purpose":"Break down → DAG","tools":["task_graph"],"model_pref":"reasoning"},
    {"id":"researcher","role":"Researcher","purpose":"Search + extract + cross-check","tools":["browser.search","knowledge.search"],"model_pref":"reasoning"},
    {"id":"reasoner","role":"Reasoner","purpose":"Deep reasoning","tools":[],"model_pref":"reasoning"},
    {"id":"coder","role":"Coder","purpose":"Implement","tools":["filesystem.write","terminal.exec","git.commit"],"model_pref":"coding"},
    {"id":"debugger","role":"Debugger","purpose":"Diagnose + fix","tools":["terminal.exec","filesystem.read"],"model_pref":"coding"},
    {"id":"tester","role":"Tester","purpose":"Write/run tests","tools":["terminal.exec"],"model_pref":"coding"},
    {"id":"reviewer","role":"Reviewer","purpose":"Security/quality audit","tools":["filesystem.read","git.diff"],"model_pref":"reasoning"},
    {"id":"architect","role":"Architect","purpose":"System design","tools":["filesystem.read","knowledge.search"],"model_pref":"reasoning"},
    {"id":"documenter","role":"Documenter","purpose":"Docs","tools":["filesystem.write"],"model_pref":"reasoning"},
    {"id":"analyst","role":"Analyst","purpose":"Data analysis","tools":["python.exec","filesystem.read"],"model_pref":"reasoning"},
    {"id":"data_scientist","role":"Data Scientist","purpose":"Analysis + viz","tools":["python.exec"],"model_pref":"coding"},
    {"id":"security_auditor","role":"Security Auditor","purpose":"Threat model","tools":["filesystem.read","terminal.exec"],"model_pref":"reasoning"},
    {"id":"file_manager","role":"File Manager","purpose":"Bulk file ops","tools":["filesystem.read","filesystem.write"],"model_pref":"fast"},
    {"id":"browser_agent","role":"Browser Agent","purpose":"Search + navigate","tools":["browser.search","browser.navigate"],"model_pref":"reasoning"},
    {"id":"vision_agent","role":"Vision Agent","purpose":"Screen understanding","tools":["vision.screenshot","vision.ocr"],"model_pref":"vision"},
    {"id":"system_agent","role":"System Agent","purpose":"OS control","tools":["automation.click","automation.type"],"model_pref":"vision"},
    {"id":"automation_agent","role":"Automation Agent","purpose":"Click/type verified","tools":["automation.click","vision.screenshot"],"model_pref":"vision"},
    {"id":"memory_manager","role":"Memory Manager","purpose":"Consolidation","tools":["memory.search"],"model_pref":"fast"},
]

class AgentRegistry:
    def __init__(self, prompts_dir="agents/prompts"):
        self.prompts_dir=pathlib.Path(prompts_dir)

    def list(self): return AGENTS
    def get(self, agent_id: str): return next((a for a in AGENTS if a["id"]==agent_id), None)
    def prompt(self, agent_id: str) -> str:
        p=self.prompts_dir / f"{agent_id}.md"
        if p.exists(): return p.read_text(encoding="utf-8")
        ag=self.get(agent_id)
        if not ag: return "You are NEXUS Agent X."
        return f"You are {ag['role']} — {ag['purpose']}. Tools: {', '.join(ag['tools']) or 'none (orchestration)'}."
