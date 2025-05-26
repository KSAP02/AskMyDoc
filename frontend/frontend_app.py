import streamlit as st
import requests
import base64
import fitz  # PyMuPDF for PDF processing

# Configure Streamlit page settings

st.set_page_config(
    page_title = "AskMyDoc",
    page_icon = "📃",
    layout= "centered"
)
BACKEND_URL = "http://localhost:8000"
st.title("AskMyDoc 📃")

# Custom CSS for full-screen PDF viewer
st.markdown("""
    <style>
        /* Remove Streamlit's default padding and margins */
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
            max-width: 100% !important;
        }
        header, footer { visibility: hidden !important; }
        
        /* Remove default margins from main content */
        .main > div {
            padding-top: 0rem !important;
        }
        
        /* Full height PDF viewer */
        .pdf-viewer {
            height: 100vh !important;
            width: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        
        .pdf-viewer iframe {
            height: 100vh !important;
            width: 100% !important;
            border: none !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Remove any gap between columns */
        .stColumns {
            gap: 0rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# Utility Functions
def get_pdf_page_count(pdf_bytes):
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        page_count = len(doc)
        doc.close()
        return page_count
    except Exception:
        return 0

def send_chat_message(message, page_number, frontend_chat_history):
    try:
        payload = {
            "query": message,
            "page_num": page_number,
            "chat_history": frontend_chat_history
        }
        response = requests.post(f"{BACKEND_URL}/query_response", json=payload, timeout=30)
        print("response:", response.text)  # Debugging output
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return f"Connection error: {str(e)}"

# Session State Initialization
def initialize_session_state():
    if "pdf_uploaded" not in st.session_state:
        st.session_state.pdf_uploaded = False
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "current_page" not in st.session_state:
        st.session_state.current_page = 1

def clear_chat_history():
    st.session_state.chat_history = []

def reset_all_session_state():
    st.session_state.clear()

# Main Application
initialize_session_state()

if not st.session_state.pdf_uploaded:
    st.markdown("## Upload your PDF to get started")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        pdf_bytes = uploaded_file.read()
        try:
            files = {"file": (uploaded_file.name, pdf_bytes, "application/pdf")}
            with st.spinner("Parsing PDF..."):
                response = requests.post(f"{BACKEND_URL}/parse_pdf", files=files, timeout=120)
            print(response)
            st.session_state.pdf_bytes = pdf_bytes
            st.session_state.pdf_name = uploaded_file.name
            st.session_state.total_pages = get_pdf_page_count(pdf_bytes)
            st.session_state.pdf_uploaded = True
            st.success("✅ PDF parsed successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Failed to parse PDF: {e}")

else:
    col1, col2 = st.columns([7, 3])  # 70% for PDF, 30% for chat
    
    with col1:
        pdf_base64 = base64.b64encode(st.session_state.pdf_bytes).decode()
        pdf_display = f"""
        <div class="pdf-viewer">
            <iframe
                src="data:application/pdf;base64,{pdf_base64}#page={st.session_state.current_page}"
                width="100%"
                height="100%"
                type="application/pdf">
            </iframe>
        </div>
        """
        st.markdown(pdf_display, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="position: fixed; bottom: 10px; left: 10px; background: rgba(255,255,255,0.9); 
                    padding: 5px 10px; border-radius: 5px; font-size: 12px; z-index: 1000;">
            📖 {st.session_state.pdf_name} | Page {st.session_state.current_page} of {st.session_state.total_pages}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Chat Assistant 🤖")
        
        chat_page = st.selectbox(
            "Select page to query:",
            options=list(range(1, st.session_state.total_pages + 1)),
            index=st.session_state.current_page - 1,
            key="chat_page_selector",
            help="Choose which PDF page you want to ask questions about"
        )
        
        user_query = st.chat_input("Ask about the PDF content...")
        
        if user_query:
            # Add user message to chat history immediately
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_query
            })
            
            # Get assistant response
            with st.spinner("Processing your question..."):
                response = send_chat_message(
                    message=user_query,
                    page_number=chat_page,
                    frontend_chat_history=st.session_state.chat_history
                )
            
            # Add assistant response to chat history
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response
            })
            
            # Rerun to refresh the chat display
            st.rerun()
        
        # Display all chat messages within the scrollable container
        chat_history_container = st.container(height=600)  # Fixed height with scrolling
        with chat_history_container:
            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])
        
        st.markdown("---")
        col_clear, col_upload = st.columns(2)
        
        with col_clear:
            if st.button("🗑️ Clear Chat", help="Clear all chat history"):
                clear_chat_history()
                st.rerun()
        
        with col_upload:
            if st.button("📤 New PDF", help="Upload a different PDF"):
                reset_all_session_state()
                st.rerun()