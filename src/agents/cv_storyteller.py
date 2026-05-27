from pathlib import Path
from src import llm

_PROMPT = (Path(__file__).parent.parent.parent / "prompts" / "cv_storyteller.md").read_text(encoding="utf-8")

def analyze(cv: str, jd_parsed: str) -> str:
    prompt = _PROMPT.replace("{jd_parsed}", jd_parsed).replace("{cv}", cv)
    return llm.call(prompt)
