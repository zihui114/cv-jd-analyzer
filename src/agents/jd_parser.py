from pathlib import Path
from src import llm

_PROMPT = (Path(__file__).parent.parent.parent / "prompts" / "jd_parser.md").read_text(encoding="utf-8")

def parse(jd: str) -> str:
    prompt = _PROMPT.replace("{jd}", jd)
    return llm.call(prompt)
