import streamlit as st
import requests
import base64
from io import BytesIO
import fitz  # PyMuPDF for PDF processing

# Configure Streamlit page
st.set_page_config(
    page_title="PDF Chat Assistant",
    layout="wide",
)

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
        
        /* Ensure columns take full height */
        .stColumns > div {
            height: 100vh !important;
        }
        
        /* Remove any gap between columns */
        .stColumns {
            gap: 0rem !important;
        }
    </style>
""", unsafe_allow_html=True)

BACKEND_URL = "http://localhost:8000"

def get_pdf_page_count(pdf_bytes):
    """Get total number of pages in PDF"""
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        page_count = len(doc)
        doc.close()
        return page_count
    except:
        return 0

def send_chat_message(message, page_number, chat_history):
    """Send question+page+history to /chat endpoint."""
    payload = {
        "message": message, 
        "page_number": page_number,
        "chat_history": chat_history
    }
    resp = requests.post(f"{BACKEND_URL}/chat", json=payload, timeout=30)
    if resp.ok:
        return resp.json().get("response", "No response received")
    return f"Error {resp.status_code}: {resp.text}"

# Initialize session state - only what we need
if "pdf_uploaded" not in st.session_state:
    st.session_state.pdf_uploaded = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_page" not in st.session_state:
    st.session_state.current_page = 1

# Upload & parse PDF
if not st.session_state.pdf_uploaded:
    st.markdown("## Upload your PDF to get started")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        pdf_bytes = uploaded_file.read()
        
        # Send to parse_pdf endpoint
        try:
            files = {"file": (uploaded_file.name, pdf_bytes, "application/pdf")}
            response = requests.post(f"{BACKEND_URL}/parse_pdf", files=files, timeout=60)
            response.raise_for_status()
            
            # Store only what we need
            st.session_state.pdf_bytes = pdf_bytes
            st.session_state.pdf_name = uploaded_file.name
            st.session_state.total_pages = get_pdf_page_count(pdf_bytes)
            st.session_state.pdf_uploaded = True
            
            st.success("✅ PDF parsed successfully!")
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Failed to parse PDF: {e}")

# Main interface - PDF viewer + Chat
else:
    col1, col2 = st.columns([7, 3])
    
    with col1:
        # PDF Viewer
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
        
        # Page info overlay
        st.markdown(f"""
        <div style="position: fixed; bottom: 10px; left: 10px; background: rgba(255,255,255,0.9); 
                    padding: 5px 10px; border-radius: 5px; font-size: 12px; z-index: 1000;">
            📖 {st.session_state.pdf_name} | Page {st.session_state.current_page} of {st.session_state.total_pages}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Chat Assistant")
        
        # Display chat history
        for chat in st.session_state.chat_history:
            with st.chat_message("user"):
                st.write(chat["user_message"])
                st.caption(f"📄 Page: {chat['page_number']}")
            
            with st.chat_message("assistant"):
                st.write(chat["assistant_response"])
        
        # Chat input
        if prompt := st.chat_input("Ask about the PDF content..."):
            # Display user message immediately
            with st.chat_message("user"):
                st.write(prompt)
                st.caption(f"📄 Page: {st.session_state.current_page}")
            
            # Get response from backend
            with st.chat_message("assistant"):
                with st.spinner("Processing..."):
                    response = send_chat_message(
                        prompt, 
                        st.session_state.current_page,
                        st.session_state.chat_history
                    )
                    st.write(response)
            
            # Add to chat history
            st.session_state.chat_history.append({
                "user_message": prompt,
                "assistant_response": response,
                "page_number": st.session_state.current_page
            })
        
        # Controls
        st.markdown("---")
        col_clear, col_upload = st.columns(2)
        
        with col_clear:
            if st.button("🗑️ Clear Chat"):
                st.session_state.chat_history = []
                st.rerun()
        
        with col_upload:
            if st.button("📤 New PDF"):
                st.session_state.clear()
                st.rerun()
