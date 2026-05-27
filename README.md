# CV / JD Analyzer

輸入 CV 與職缺描述（JD），自動生成五種求職分析文件：

| 模組 | 說明 |
|------|------|
| `insight` | JD 深度解讀：核心能力需求、門面話識別、公司困境推測、最重要的面試準備方向 |
| `fit` | 匹配度分析 + 弱項診斷：逐條對照 JD 要求 vs CV 佐證，找出缺口並給補強建議 |
| `interview` | 面試全準備：三個經歷亮點（STAR 結構）、技術題 + 行為題預測、附「為什麼會問」提示 |
| `cover` | Cover Letter：客製化繁中求職信，只引用 CV 實際事實，找不到佐證標記 `[需確認]` |
| `rewrite` | 自我介紹改寫：以 JD 為目標，改寫現有自我介紹的重點與開場邏輯 |

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

## 使用方式

### Web 介面（推薦）

```bash
python app.py
# 開啟瀏覽器前往 http://localhost:5001
```

貼上 CV 文字或上傳 PDF，貼上 JD，勾選模組，結果直接在瀏覽器顯示。

### CLI

```bash
# 全部模組
python main.py --cv data/cv/zh.md --jd data/jd/company_job.md

# 指定模組
python main.py --cv data/cv/zh.md --jd data/jd/company_job.md --mode insight
python main.py --cv data/cv/zh.md --jd data/jd/company_job.md --mode fit
python main.py --cv data/cv/zh.md --jd data/jd/company_job.md --mode interview
python main.py --cv data/cv/zh.md --jd data/jd/company_job.md --mode cover

# 自我介紹改寫（需額外提供現有自我介紹）
python main.py --cv data/cv/zh.md --jd data/jd/company_job.md --mode rewrite --intro intro.md
```

輸出自動存到 `data/output/YYYY-MM-DD/`，不會覆蓋舊版本（自動加 `_v2`、`_v3`）。

## 專案結構

```
cv-jd-analyzer/
├── main.py                  # CLI 入口
├── app.py                   # Flask Web 介面入口
├── requirements.txt
├── .env.example
├── src/
│   ├── llm.py               # Groq API 封裝
│   ├── pdf_parser.py        # PDF 文字解析
│   ├── file_manager.py      # 輸出檔管理
│   └── agents/
│       ├── jd_parser.py         # JD 結構化解析（前置步驟）
│       ├── jd_insight.py        # JD 深度解讀
│       ├── cv_matcher.py        # 匹配度分析
│       ├── weakness_analyzer.py # 弱項診斷
│       ├── fit_analyzer.py      # 匹配度 + 弱項（組合）
│       ├── cv_storyteller.py    # 經歷亮點與 STAR 整理
│       ├── question_predictor.py # 面試題預測
│       ├── interview_prep.py    # 面試準備建議
│       ├── interview_all.py     # 面試全準備（組合）
│       ├── cover_letter.py      # Cover Letter 生成
│       └── intro_rewriter.py    # 自我介紹改寫
├── prompts/                 # 各 agent 的 prompt 模板
├── templates/               # Web 介面前端
└── data/
    ├── cv/                  # 放 CV 檔案
    ├── jd/                  # 放 JD 檔案
    └── output/              # 生成結果（依日期分資料夾）
```

## 模型

預設使用 [Groq](https://groq.com) 的 `llama-3.3-70b-versatile`，免費且支援繁體中文。

若要換模型，修改 `src/llm.py` 的 `model` 參數即可。

## 限制

- CV 若為 Canva 製作的 PDF，文字可能無法解析，建議另存純文字版
- Cover Letter 僅引用 CV 中存在的事實，找不到佐證時會標記 `[需確認]`
- JD 建議使用繁體中文，英文 JD 輸出品質不穩定
