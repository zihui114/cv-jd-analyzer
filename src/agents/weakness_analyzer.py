from pathlib import Path
from src import llm

_PROMPT = (Path(__file__).parent.parent.parent / "prompts" / "weakness_analyzer.md").read_text(encoding="utf-8")

def analyze(cv: str, jd_parsed: str, match_analysis: str, company: str, position: str) -> str:
    prompt = (
        _PROMPT
        .replace("{cv}", cv)
        .replace("{jd_parsed}", jd_parsed)
        .replace("{match_analysis}", match_analysis)
        .replace("{company}", company)
        .replace("{position}", position)
    )
    return llm.call(prompt)
