#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path

from src.file_manager import read_file, save_output
from src.agents import jd_parser, cv_matcher, cover_letter, interview_prep, weakness_analyzer

MODULES = ["all", "match", "cover", "interview", "weakness"]


def extract_meta(jd_parsed: str) -> tuple[str, str]:
    company = re.search(r"公司[：:]\s*(.+)", jd_parsed)
    position = re.search(r"職位[：:]\s*(.+)", jd_parsed)
    return (
        company.group(1).strip() if company else "未知公司",
        position.group(1).strip() if position else "未知職位",
    )


def run(cv_path: str, jd_path: str, mode: str):
    print(f"讀取 CV：{cv_path}")
    cv = read_file(cv_path)

    print(f"讀取 JD：{jd_path}")
    jd = read_file(jd_path)

    print("解析 JD...")
    jd_parsed = jd_parser.parse(jd)
    company, position = extract_meta(jd_parsed)
    print(f"  → {company} / {position}")

    results = {}

    if mode in ("all", "match", "weakness"):
        print("執行匹配度分析...")
        results["match"] = cv_matcher.analyze(cv, jd_parsed, company, position)
        path = save_output(results["match"], company, position, "match_analysis")
        print(f"  → 已存到 {path}")

    if mode in ("all", "weakness"):
        print("執行弱項診斷...")
        results["weakness"] = weakness_analyzer.analyze(
            cv, jd_parsed, results["match"], company, position
        )
        path = save_output(results["weakness"], company, position, "weakness_analysis")
        print(f"  → 已存到 {path}")

    if mode in ("all", "cover"):
        print("生成 Cover Letter...")
        results["cover"] = cover_letter.generate(cv, jd_parsed, company, position)
        path = save_output(results["cover"], company, position, "cover_letter")
        print(f"  → 已存到 {path}")

    if mode in ("all", "interview"):
        print("預測面試題...")
        results["interview"] = interview_prep.generate(cv, jd_parsed, company, position)
        path = save_output(results["interview"], company, position, "interview_prep")
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
        help="執行模組：all / match / cover / interview / weakness（預設：all）",
    )
    args = parser.parse_args()

    cv_path = Path(args.cv).expanduser()
    jd_path = Path(args.jd).expanduser()

    if not cv_path.exists():
        print(f"錯誤：找不到 CV 檔案：{cv_path}", file=sys.stderr)
        sys.exit(1)
    if not jd_path.exists():
        print(f"錯誤：找不到 JD 檔案：{jd_path}", file=sys.stderr)
        sys.exit(1)

    run(str(cv_path), str(jd_path), args.mode)


if __name__ == "__main__":
    main()
