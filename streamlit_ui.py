import streamlit as st
import requests
import sys
from exception.exceptions import WeatherReportException

base_url = "http://localhost:8000"

st.set_page_config(
    page_title = "🌦️ AI Weather Expert",
    page_icon= "🌦️",
    layout = "centered",
    initial_sidebar_state = "auto"
)

st.title("🌦️ Weather Report Agentic Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Upload Documents")
    st.markdown("Upload **weather and climate specific PDFs or DOCX** to create knowledge base.")
    uploaded_files = st.file_uploader(
        label = "Choose files",
        type = ['.pdf','docx'],
        accept_multiple_files=True
    )
    
    if st.button("Upload and Ingest"):
        if uploaded_files:
            files = []
            for f in uploaded_files:
                file_data = f.read()
                if not file_data:
                    continue
                files.append(("files",(getattr(f,"name","files.pdf"),file_data,f.type)))

            if files:
                try:
                    with st.spinner("Uploading and Ingesting file"):
                        response = requests.post(url=f"{base_url}/upload",files=files)
                        if response.status_code==200:
                              st.success("✅ Files uploaded and processed successfully!")
                        else:
                            st.error("❌ Upload failed: " + response.text)
                except Exception as e:
                    raise WeatherReportException(e,sys)
            else: 
                 st.warning("Some files were empty or unreadable.")

# Display chat history
st.header("💬 Chat")
for chat in st.session_state.messages:
    if chat["role"] == "user":
        st.markdown(f"**🧑 You:** {chat['content']}")
    else:
        st.markdown(f"**🤖 Bot:** {chat['content']}")

# Chat input box at bottom
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Your message", placeholder="e.g. What's the weather in New Delhi")
    submit_button = st.form_submit_button("Send")

if submit_button and user_input.strip():
    try:
        # Show user message
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Show thinking spinner while backend processes
        with st.spinner("Bot is thinking..."):
            payload = {"question": user_input}
            response = requests.post(f"{base_url}/query", json=payload)

        if response.status_code == 200:
            answer = response.json().get("answer", "No answer returned.")
            st.session_state.messages.append({"role": "bot", "content": answer})
            st.rerun()  # 🔁 fixed here
        else:
            st.error("❌ Bot failed to respond: " + response.text)

    except Exception as e:
        raise WeatherReportException(e, sys)