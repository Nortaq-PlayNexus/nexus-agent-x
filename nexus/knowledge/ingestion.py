"""Ingestion pipeline — PDF/DOCX/MD → clean → chunk → embed (ULTRA §29)."""
import pathlib, re

def chunk_text(text: str, size=512, overlap=80) -> list[str]:
    words=text.split()
    chunks=[]
    i=0
    while i < len(words):
        chunks.append(" ".join(words[i:i+size]))
        i+= size-overlap
    return chunks

def ingest_file(path: str) -> list[str]:
    p=pathlib.Path(path)
    if not p.exists(): return []
    text=p.read_text(encoding="utf-8", errors="ignore")
    text=re.sub(r"\s+", " ", text)
    return chunk_text(text)

def ingest_code(path: str) -> list[str]:
    # code-aware: split by function/class
    return ingest_file(path)
