#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path

from src.file_manager import read_file, save_output
from src.agents import jd_parser, jd_insight, fit_analyzer, interview_all, cover_letter, intro_rewriter

MODULES = ["all", "insight", "fit", "interview", "cover", "rewrite"]


def extract_meta(jd_parsed: str) -> tuple[str, str]:
    company = re.search(r"公司[：:]\s*(.+)", jd_parsed)
    position = re.search(r"職位[：:]\s*(.+)", jd_parsed)
    return (
        company.group(1).strip() if company else "未知公司",
        position.group(1).strip() if position else "未知職位",
    )


def run(cv_path: str, jd_path: str, mode: str, intro_path: str | None = None):
    print(f"讀取 CV：{cv_path}")
    cv = read_file(cv_path)

    print(f"讀取 JD：{jd_path}")
    jd = read_file(jd_path)

    print("解析 JD...")
    jd_parsed = jd_parser.parse(jd)
    company, position = extract_meta(jd_parsed)
    print(f"  → {company} / {position}")

    if mode in ("all", "insight"):
        print("執行 JD 深度解讀...")
        result = jd_insight.analyze(jd_parsed)
        path = save_output(result, company, position, "insight")
        print(f"  → 已存到 {path}")

    if mode in ("all", "fit"):
        print("執行匹配度與弱項分析...")
        result = fit_analyzer.analyze(cv, jd_parsed, company, position)
        path = save_output(result, company, position, "fit")
        print(f"  → 已存到 {path}")

    if mode in ("all", "interview"):
        print("執行面試全準備...")
        result = interview_all.generate(cv, jd_parsed, company, position)
        path = save_output(result, company, position, "interview")
        print(f"  → 已存到 {path}")

    if mode in ("all", "cover"):
        print("生成 Cover Letter...")
        result = cover_letter.generate(cv, jd_parsed, company, position)
        path = save_output(result, company, position, "cover")
        print(f"  → 已存到 {path}")

    if mode == "rewrite":
        if not intro_path:
            print("錯誤：--mode rewrite 需要提供 --intro 自我介紹檔案路徑", file=sys.stderr)
            sys.exit(1)
        print(f"讀取自我介紹：{intro_path}")
        intro = read_file(intro_path)
        print("改寫自我介紹...")
        result = intro_rewriter.rewrite(intro, cv, jd_parsed)
        path = save_output(result, company, position, "rewrite")
        print(f"  → 已存到 {path}")

    print("\n完成。")


def main():
    parser = argparse.ArgumentParser(
        description="CV / JD Analyzer — 輸入 CV 與 JD，輸出求職分析"
    )
    parser.add_argument("--cv", required=True, help="CV 檔案路徑（.md / .pdf / .txt）")
    parser.add_argument("--jd", required=True, help="JD 檔案路徑（.md / .txt）")
    parser.add_argument(
        "--mode",
        default="all",
        choices=MODULES,
        help="執行模組：all / insight / fit / interview / cover / rewrite（預設：all）",
    )
    parser.add_argument("--intro", default=None, help="自我介紹檔案路徑（--mode rewrite 時必填）")
    args = parser.parse_args()

    cv_path = Path(args.cv).expanduser()
    jd_path = Path(args.jd).expanduser()

    if not cv_path.exists():
        print(f"錯誤：找不到 CV 檔案：{cv_path}", file=sys.stderr)
        sys.exit(1)
    if not jd_path.exists():
        print(f"錯誤：找不到 JD 檔案：{jd_path}", file=sys.stderr)
        sys.exit(1)

    intro_path = None
    if args.intro:
        intro_path = Path(args.intro).expanduser()
        if not intro_path.exists():
            print(f"錯誤：找不到自我介紹檔案：{intro_path}", file=sys.stderr)
            sys.exit(1)
        intro_path = str(intro_path)

    run(str(cv_path), str(jd_path), args.mode, intro_path)


if __name__ == "__main__":
    main()
