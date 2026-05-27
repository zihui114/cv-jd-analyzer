#!/usr/bin/env python3
import os
import re
import tempfile
from flask import Flask, render_template, request, jsonify

from src.pdf_parser import parse_pdf
from src.agents import jd_parser, jd_insight, fit_analyzer, interview_all, cover_letter, intro_rewriter
from src.file_manager import save_output

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024


def extract_meta(jd_parsed: str) -> tuple[str, str]:
    company = re.search(r"公司[：:]\s*(.+)", jd_parsed)
    position = re.search(r"職位[：:]\s*(.+)", jd_parsed)
    return (
        company.group(1).strip() if company else "未知公司",
        position.group(1).strip() if position else "未知職位",
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    # CV
    cv_file = request.files.get("cv_file")
    cv_text = request.form.get("cv_text", "").strip()

    if cv_file and cv_file.filename:
        suffix = os.path.splitext(cv_file.filename)[1].lower()
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            cv_file.save(tmp.name)
            tmp_name = tmp.name
        try:
            cv = parse_pdf(tmp_name) if suffix == ".pdf" else open(tmp_name, encoding="utf-8").read()
        finally:
            os.unlink(tmp_name)
    elif cv_text:
        cv = cv_text
    else:
        return jsonify({"error": "請提供 CV 內容（貼上文字或上傳檔案）"}), 400

    # JD
    jd = request.form.get("jd_text", "").strip()
    if not jd:
        return jsonify({"error": "請貼上 JD 內容"}), 400

    modules = request.form.getlist("modules")
    if not modules:
        return jsonify({"error": "請至少選擇一個分析模組"}), 400

    intro = request.form.get("intro_text", "").strip()

    try:
        jd_parsed = jd_parser.parse(jd)
        company, position = extract_meta(jd_parsed)

        results = {}

        if "insight" in modules:
            results["insight"] = jd_insight.analyze(jd_parsed)

        if "fit" in modules:
            results["fit"] = fit_analyzer.analyze(cv, jd_parsed, company, position)

        if "interview" in modules:
            results["interview"] = interview_all.generate(cv, jd_parsed, company, position)

        if "cover" in modules:
            results["cover"] = cover_letter.generate(cv, jd_parsed, company, position)

        if "rewrite" in modules:
            if not intro:
                results["rewrite"] = "_請在「自我介紹」欄位填入目前的版本，再重新分析。_"
            else:
                results["rewrite"] = intro_rewriter.rewrite(intro, cv, jd_parsed)

        for module, content in results.items():
            save_output(content, company, position, module)

        return jsonify({"company": company, "position": position, "results": results})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5001)
