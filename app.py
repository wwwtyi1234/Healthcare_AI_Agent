
import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# 讀取環境變數
load_dotenv()

st.set_page_config(
    page_title="Healthcare AI Agent",
    page_icon="🏥"
)

st.title("🏥 醫療門診行政資訊 AI 助理")

st.caption(
    "開發階段 1：基本 LLM 問答介面"
)

# 從 .env 讀取 API Key
raw_key = os.getenv("GROQ_API_KEY", "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")
api_key = str(raw_key).encode("ascii", "ignore").decode("ascii").strip()

model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile").strip()

# 檢查 API 密鑰
if not api_key:
    st.error("找不到 Groq API Key，請檢查 .env 設定。")
    st.stop()

# 建立 Groq API 連線
client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)
SYSTEM_PROMPT = """
你是醫療機構門診行政資訊助理。

目前尚未連接醫院官方資料庫。

1. 不得編造醫院規定、費用及時間。
2. 協助一般門診行政資訊。
3. 不提供疾病診斷及治療建議。
4. 資訊不足時必須明確說明。
5. 使用繁體中文回答。
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

# 側邊欄
with st.sidebar:

    st.subheader("系統資訊")

    st.write(f"模型：{model}")

    st.write("目前階段：基本 LLM 問答")

    st.info(
        "下一階段加入 RAG 知識資料庫與 Agent 工具調用。"
    )

    if st.button("清除對話"):
        st.session_state.messages = []
        st.rerun()

# 顯示歷史對話
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 使用者輸入
user_input = st.chat_input(
    "例如：第一次到醫院看診，需要準備什麼？"
)

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    api_messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    api_messages.extend(
        st.session_state.messages[-12:]
    )

    with st.chat_message("assistant"):

        with st.spinner("AI 正在思考..."):

            try:

                result = client.chat.completions.create(
                    model=model,
                    messages=api_messages,
                    temperature=0.2,
                    max_tokens=900
                )

                answer = (
                    result.choices[0].message.content
                    or "目前沒有取得回答。"
                )

            except Exception as exc:

                answer = (
                    "API 呼叫失敗，請檢查設定。\n\n"
                    f"錯誤訊息：{str(exc)}"
                )

            st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

