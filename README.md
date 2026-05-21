# CV / JD Analyzer

輸入 CV 與職缺描述（JD），自動生成四份求職分析文件：

- **匹配度分析**：JD 要求 vs CV 佐證，逐條對照
- **弱項診斷**：找出缺口並給出補強建議
- **Cover Letter**：客製化繁中求職信，僅引用 CV 實際事實
- **面試題預測**：技術題 + 行為題，附「為什麼會問」與 STAR 提示

## 快速開始

### 安裝

```bash
git clone https://github.com/zihui114/cv-jd-analyzer.git
cd cv-jd-analyzer
pip install -r requirements.txt
```

### 設定 API Key

申請免費 Groq API Key：[console.groq.com](https://console.groq.com)

```bash
cp .env.example .env
# 編輯 .env，填入你的 GROQ_API_KEY
```

### 準備輸入檔

| 檔案 | 位置 | 格式 |
|------|------|------|
| CV | `data/cv/` | `.md` 或 `.txt`（建議從 PDF 複製貼上） |
| JD | `data/jd/` | `.md` 或 `.txt`（從 104 / LinkedIn 貼上即可） |

### 執行

```bash
# 全部四個模組
python main.py --cv data/cv/zh.md --jd data/jd/company_job.md

# 只跑特定模組
python main.py --cv data/cv/zh.md --jd data/jd/company_job.md --mode cover
python main.py --cv data/cv/zh.md --jd data/jd/company_job.md --mode match
python main.py --cv data/cv/zh.md --jd data/jd/company_job.md --mode interview
python main.py --cv data/cv/zh.md --jd data/jd/company_job.md --mode weakness
```

輸出自動存到 `data/output/YYYY-MM-DD/`，不會覆蓋舊版本（自動加 `_v2`、`_v3`）。

## 專案結構

```
cv-jd-analyzer/
├── main.py                  # CLI 入口
├── requirements.txt
├── .env.example
├── src/
│   ├── llm.py               # Groq API 封裝
│   ├── pdf_parser.py        # PDF 文字解析
│   ├── file_manager.py      # 輸出檔管理
│   └── agents/
│       ├── jd_parser.py     # JD 結構化解析
│       ├── cv_matcher.py    # 匹配度分析
│       ├── cover_letter.py  # Cover Letter 生成
│       ├── interview_prep.py # 面試題預測
│       └── weakness_analyzer.py # 弱項診斷
├── prompts/                 # 各 agent 的 prompt 模板
├── data/
│   ├── jd/                  # 放 JD 檔案
│   └── output/              # 生成結果（依日期分資料夾）
```

## 模型

預設使用 [Groq](https://groq.com) 的 `llama-3.3-70b-versatile`，免費且支援繁體中文。

若要換模型，修改 `src/llm.py` 第 18 行的 `model` 參數即可。

## 限制

- CV 若為 Canva 製作的 PDF，文字可能無法解析，建議另存純文字版
- Cover Letter 僅引用 CV 中存在的事實，找不到佐證時會標記 `[需確認]`
- 不會自動修改 `data/cv/` 原始 CV 檔案
