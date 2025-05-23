import streamlit as st
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(
    page_title="AskMyDoc Chat",
    page_icon="💬",
    layout="wide"
)

for key, default in {
    "messages": [],
    "processing": False,
    "current_page": 1
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

st.title("📄 AskMyDoc")
st.write("Ask me anything about the PDF you’re viewing!")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

query = st.chat_input(
    "Ask a question about the document...",
    disabled=st.session_state.processing
)

def ask_extension(query, page):
    js = f"""
      new Promise((resolve) => {{
        chrome.runtime.sendMessage(
          {{ type: 'PROCESS_QUERY', data: {{ query: {query!r}, page: {page} }} }},
          (resp) => {{
            resolve(resp);
          }}
        );
      }})
    """
    return streamlit_js_eval(js_expressions=js)


if query:
    st.session_state.messages.append({"role": "user", "content": query})
    st.session_state.processing = True
    st.rerun()  

if st.session_state.processing:
    last = st.session_state.messages[-1]
    if last["role"] == "user":
        resp = ask_extension(last["content"], st.session_state.current_page)
        reply_text = resp.get("content", "<no content>")
        st.session_state.messages.append(
            {"role": "assistant", "content": reply_text})
        st.session_state.processing = False
        st.rerun()
