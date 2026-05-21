import os
from datetime import date
from pathlib import Path

BASE_OUTPUT = Path(__file__).parent.parent / "data" / "output"

def read_file(path: str) -> str:
    path = Path(path).expanduser()
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        from src.pdf_parser import parse_pdf
        return parse_pdf(str(path))
    return path.read_text(encoding="utf-8")

def save_output(content: str, company: str, position: str, module: str) -> Path:
    today = date.today().isoformat()
    out_dir = BASE_OUTPUT / today
    out_dir.mkdir(parents=True, exist_ok=True)

    slug = f"{company}_{position}".replace(" ", "_").replace("/", "-")
    filename = f"{module}_{slug}.md"
    out_path = out_dir / filename

    # 避免覆蓋：若已存在則加版號
    version = 2
    while out_path.exists():
        out_path = out_dir / f"{module}_{slug}_v{version}.md"
        version += 1

    out_path.write_text(content, encoding="utf-8")
    return out_path
