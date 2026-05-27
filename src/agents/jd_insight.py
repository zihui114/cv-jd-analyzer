from pathlib import Path
from src import llm

_PROMPT = (Path(__file__).parent.parent.parent / "prompts" / "jd_insight.md").read_text(encoding="utf-8")

def analyze(jd_parsed: str) -> str:
    prompt = _PROMPT.replace("{jd_parsed}", jd_parsed)
    return llm.call(prompt)
