# -*- coding: utf-8 -*-
import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
st.set_page_config(page_title="Healthcare AI Agent", page_icon="🏥")
st.title("🏥 醫療門診行政資訊 AI 助理")
st.caption("開發階段 1：基本問答介面。尚未連接醫院官方資料庫，也不提供診斷或治療建議。")

api_key = "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"
model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile").strip()

if not api_key:
    st.error("尚未設定 GROQ_API_KEY。請在專案資料夾建立 .env，並填入 Groq API Key。")
    st.stop()

client = OpenAI(api_key=str(api_key).encode('ascii', 'ignore').decode('ascii'), base_url="https://api.groq.com/openai/v1")
SYSTEM_PROMPT = """
你是醫療機構門診行政資訊助理。
目前沒有連接醫院官方資料庫，因此不得假裝知道特定醫院的最新規定、費用、時間、電話或地址。
只協助一般行政流程資訊；不提供疾病診斷、用藥或治療建議。
資訊不足時明確說明，不可編造。使用繁體中文回答。
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.subheader("系統資訊")
    st.write(f"模型：{model}")
    st.write("目前階段：基本 LLM 問答")
    st.info("下一階段加入官方資料檢索（RAG）與 Agent 工具調用。")
    if st.button("清除對話"):
        st.session_state.messages = []
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("例如：第一次到醫院看診，通常要先確認哪些行政事項？")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    api_messages.extend(st.session_state.messages[-12:])

    with st.chat_message("assistant"):
        with st.spinner("正在整理回答..."):
            try:
                result = client.chat.completions.create(
                    model=model,
                    messages=api_messages,
                    temperature=0.2,
                    max_tokens=900
                )
                answer = result.choices[0].message.content or "目前沒有取得文字回答。"
            except Exception as exc:
                answer = "呼叫模型時發生錯誤，請確認 API Key、模型名稱及網路連線。\n\n錯誤訊息：" + str(exc)
            st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
