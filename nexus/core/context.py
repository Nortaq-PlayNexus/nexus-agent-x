"""Context Engine — assembles SYSTEM+USER+TASK+MEMORY+DOCS+TOOLS+STATE within token budget (ULTRA §46)."""
from dataclasses import dataclass

@dataclass
class Context:
    system: str = "You are NEXUS Agent X — local, verified, offline-first."
    user: str = ""
    task: str = ""
    memory: list = None
    documents: list = None
    tools: list = None
    state: str = ""

    def assemble(self, budget_tokens: int = 8000) -> str:
        parts = [
            f"SYSTEM: {self.system}",
            f"USER: {self.user}",
            f"TASK: {self.task}",
            f"MEMORY: {self.memory or []}",
            f"DOCS: {self.documents or []}",
            f"TOOLS: {self.tools or []}",
            f"STATE: {self.state}",
        ]
        text = "\n\n".join(parts)
        # naive compression stub — real uses summarizer model
        if len(text) > budget_tokens * 4:  # ~4 chars/token
            text = text[:budget_tokens*4] + "\n...[truncated, summarized]"
        return text

def compress_context(long_text: str, keep_tokens: int = 2000) -> str:
    """Summarizer stub — in prod call small fast model to keep facts/decisions/state."""
    if len(long_text) <= keep_tokens*4: return long_text
    # keep head + tail
    return long_text[:keep_tokens*2] + "\n[compressed]\n" + long_text[-keep_tokens*2:]
