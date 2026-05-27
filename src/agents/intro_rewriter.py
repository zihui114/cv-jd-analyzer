from pathlib import Path
from src import llm

_PROMPT = (Path(__file__).parent.parent.parent / "prompts" / "intro_rewriter.md").read_text(encoding="utf-8")

def rewrite(intro: str, cv: str, jd_parsed: str) -> str:
    prompt = (
        _PROMPT
        .replace("{intro}", intro)
        .replace("{cv}", cv)
        .replace("{jd_parsed}", jd_parsed)
    )
    return llm.call(prompt)
