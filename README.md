# 大學生就業指南｜RAG

這個專案透過中文對話，協助大學生整理自己的知識與技能，並從專案收錄的 104 職缺中探索相關的職業方向。介面使用 Streamlit，結合檢索增強生成（RAG）與本機語言模型，產生可接續提問的職能分析報告。

## 系統流程

1. **職能訪談**由 GPT-4o mini 負責。模型 根據 `job.db` 內的職能資料引導對話，從使用者的背景、興趣與經驗整理出知識（K）和技能（S）。
2. **職業與職缺檢索**使用 ChromaDB。`BAAI/bge-m3` 將職能描述轉成向量。ChromaDB 先比對 `competency` 找出相近職業，再以這些職業篩選 `job_104` 中的職缺。
3. **報告與追問**在 Streamlit 介面中進行。程式從 SQLite 補齊職缺內容，交由 Ollama 的 Llama 3.1 生成報告。使用者可在 Streamlit 側欄查看報告，並在對話中追問職缺細節與連結。

訪談階段的對話會送往 OpenAI API，報告階段則由本機 Ollama 處理。

## 快速開始

以下命令適用於 Windows PowerShell。請先安裝 Git、64 位元 Python 3.10 和 [Ollama for Windows](https://docs.ollama.com/windows)，並準備具備 `gpt-4o-mini` 存取權限的 OpenAI API 金鑰。Clone 時需要使用可存取此私人 repo 的 GitHub 帳號。

### 1. 取得專案並安裝依賴

```powershell
git clone https://github.com/bloodtrail0511/RAG.git
Set-Location RAG
py -3.10 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt streamlit==1.38.0 openai==1.44.0 ollama==0.3.3
```

`requirements.txt` 記錄了 ChromaDB、FlagEmbedding 與 PyTorch 等依賴。安裝指令同時補上 Streamlit 介面使用的 `streamlit`、`openai` 和 `ollama`。

### 2. 準備模型並啟動介面

開啟 Ollama，並在專案根目錄執行下列指令。把 `<你的 OpenAI API 金鑰>` 換成自己的金鑰，供目前的 PowerShell 工作階段使用。

```powershell
ollama pull llama3.1
$env:OPENAI_API_KEY = '<你的 OpenAI API 金鑰>'
.\.venv\Scripts\python.exe -m streamlit run streamlit_test3.py
```

打開終端機顯示的 `Local URL`，預設為 `http://localhost:8501`。首次執行時，FlagEmbedding 需要從 Hugging Face 下載 [BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3)。專案已包含 SQLite 資料及 ChromaDB 索引，可直接使用。

可以從「我是資管系大四生，做過 Python 資料分析專題，也喜歡把分析結果做成儀表板」開始，再根據畫面中的提問補充經驗。報告產生後，可以追問推薦職缺的工作內容、應徵條件或職缺連結。

## 主要檔案

| 檔案或目錄 | 用途 |
| --- | --- |
| [`streamlit_test3.py`](streamlit_test3.py) | 職能訪談、報告與追問的網頁入口 |
| [`職業內涵5_整體流程.py`](職業內涵5_整體流程.py) | 在終端機執行訪談、檢索與報告流程 |
| [`Database_sqlite.py`](Database_sqlite.py)、[`Database_chroma.py`](Database_chroma.py) | SQLite 查詢、文字向量化與 ChromaDB 檢索 |
| [`job.db`](job.db) | SQLite 資料，包含 79 筆職能資料及 2,198 筆 104 職缺 |
| [`Database/`](Database/) | `competency` 和 `job_104` 的 ChromaDB 向量索引 |
| [`example.py`](example.py) | SQLite 條件查詢和 ChromaDB 向量查詢範例 |
| [`store_competency.py`](store_competency.py)、[`update_job_104.py`](update_job_104.py) | 將職能資料及已分類的職缺寫入索引 |
| [`other code/`](other%20code/) | 資料蒐集、匯入及模型測試腳本 |

## 使用時留意

- 職缺來源是 repo 內附的資料快照。職缺狀態與應徵資訊請以原始職缺頁為準。
- 訪談轉入報告的條件依賴模型輸出預期的完成句與職能清單格式。格式偏離時，介面可能停留在訪談階段，或無法取得足夠的職缺來產生報告。
- `Database_chroma.py` 的直接執行區塊會刪除兩個索引集合。查詢範例請執行 `example.py`。
