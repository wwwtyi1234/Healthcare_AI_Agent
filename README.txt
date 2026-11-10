醫療門診行政資訊 AI 助理 - Windows 初始專案

本版本是開發階段 1：基本 LLM 問答介面，尚未具備 RAG 或完整 Agent 工具調用。

1. 安裝 Python 3.11，安裝時勾選 Add Python to PATH。
2. 解壓縮本專案。
3. 在專案資料夾網址列輸入 cmd，按 Enter。
4. 依序執行：

py -3.11 -m venv .venv
.venv\\Scripts\\activate
python -m pip install --upgrade pip
pip install -r requirements.txt

5. 將 .env.example 複製一份並改名為 .env。
6. 用記事本開啟 .env，將 GROQ_API_KEY= 後方換成自己的 Groq API Key。
7. 執行：

streamlit run app.py

瀏覽器通常會開啟 http://localhost:8501
停止程式：回到命令提示字元按 Ctrl+C。

安全提醒：不要把 API Key 傳給別人、貼到公開網頁或上傳 GitHub。
若模型名稱不可用，請依 Groq 官方平台目前可用模型更新 GROQ_MODEL。
本程式僅供研究原型與一般行政資訊問答，不可用於診斷、治療或緊急醫療決策。
