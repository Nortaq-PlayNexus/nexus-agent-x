"""NEXUS CLI — typer-based entrypoint matching PlayNexus standards (neuralforge, swarmforge)."""
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="NEXUS Agent X — Local Autonomous AI OS")
console = Console()

@app.command()
def run(task: str = typer.Option(..., "--task", "-t", help="Task to execute"), mode: str = typer.Option("assistant", help="assistant|autopilot|sandbox")):
    """Run a task through the orchestrator."""
    from nexus.core.orchestrator import Orchestrator
    orch = Orchestrator(mode=mode)
    result = orch.run(task)
    console.print(f"[green]Task completed:[/green] {result}")

@app.command()
def serve(host: str = "127.0.0.1", port: int = 8000):
    """Start local API server (placeholder)."""
    console.print(f"[cyan]NEXUS serving on {host}:{port} (stub)[/cyan]")

@app.command()
def memory_search(query: str, topk: int = 5):
    """Search memory."""
    from nexus.memory.retrieval import MemoryRetrieval
    r = MemoryRetrieval()
    hits = r.search(query, topk=topk)
    table = Table(title=f"Memory search: {query}")
    table.add_column("Score"); table.add_column("Type"); table.add_column("Content")
    for h in hits:
        table.add_row(f"{h['score']:.2f}", h["type"], h["content"][:80])
    console.print(table)

@app.command()
def version():
    from nexus import __version__
    console.print(f"NEXUS Agent X v{__version__}")

def main():
    app()

if __name__ == "__main__":
    main()
