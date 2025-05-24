
import streamlit as st
import requests
import base64
import fitz  # PyMuPDF for PDF processing


# Configure Streamlit page settings
st.set_page_config(
    page_title="PDF Chat Assistant",
    layout="wide",
)


BACKEND_URL = "http://localhost:8000"

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

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_pdf_page_count(pdf_bytes):
    """
    Count total number of pages in a PDF file
    
    Args:
        pdf_bytes (bytes): Raw PDF file bytes
        
    Returns:
        int: Number of pages in the PDF
    """
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        page_count = len(doc)
        doc.close()
        return page_count
    except Exception:
        return 0

def send_chat_message(message, page_number, frontend_chat_history):
    """
    Send chat message to backend API
    
    Args:
        message (str): User's question/message
        page_number (int): Page number user is asking about
        frontend_chat_history (list): Previous chat messages in frontend format
        
    Returns:
        str: Assistant's response or error message
    """
    try:
        # Prepare payload for backend - send chat history directly
        payload = {
            "message": message,
            "page_number": page_number,
            "chat_history": frontend_chat_history
        }
        
        # Send request to backend
        response = requests.post(f"{BACKEND_URL}/chat", json=payload, timeout=30)
        
        if response.ok:
            return response.json().get("response", "No response received")
        else:
            return f"Error {response.status_code}: {response.text}"
            
    except Exception as e:
        return f"Connection error: {str(e)}"

# =============================================================================
# SESSION STATE INITIALIZATION
# =============================================================================

def initialize_session_state():
    """Initialize all session state variables with default values"""
    if "pdf_uploaded" not in st.session_state:
        st.session_state.pdf_uploaded = False
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "current_page" not in st.session_state:
        st.session_state.current_page = 1

def clear_chat_history():
    """Clear all chat history"""
    st.session_state.chat_history = []

def reset_all_session_state():
    """Reset all session state (for new PDF upload)"""
    st.session_state.clear()

# =============================================================================
# MAIN APPLICATION
# =============================================================================

# Initialize session state
initialize_session_state()

# Upload & parse PDF section
if not st.session_state.pdf_uploaded:
    st.markdown("## Upload your PDF to get started")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        pdf_bytes = uploaded_file.read()
        
        # Send PDF to backend for parsing
        try:
            files = {"file": (uploaded_file.name, pdf_bytes, "application/pdf")}
            response = requests.post(f"{BACKEND_URL}/parse_pdf", files=files, timeout=60)
            
            # Store PDF data in session state
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
    col1, col2 = st.columns([7, 3])  # 70% for PDF, 30% for chat
    
    with col1:
        # PDF Viewer with embedded base64 data
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
        
        # Page info overlay (bottom-left corner)
        st.markdown(f"""
        <div style="position: fixed; bottom: 10px; left: 10px; background: rgba(255,255,255,0.9); 
                    padding: 5px 10px; border-radius: 5px; font-size: 12px; z-index: 1000;">
            📖 {st.session_state.pdf_name} | Page {st.session_state.current_page} of {st.session_state.total_pages}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # =================================================================
        # CHAT SECTION - SCROLLABLE CONTAINER
        # =================================================================
        
        st.markdown("### Chat Assistant")
        
        # Page selector dropdown - Users can select which page to query about
        chat_page = st.selectbox(
            "Select page to query:",
            options=list(range(1, st.session_state.total_pages + 1)),
            index=st.session_state.current_page - 1,
            key="chat_page_selector",
            help="Choose which PDF page you want to ask questions about"
        )
        
        # Chat container with scrollable area
        chat_container = st.container()
        with chat_container:
            # Display chat history
            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])
        
        # Chat input section
        user_query = st.chat_input("Ask about the PDF content...")
        
        if user_query:
            # Add user message to chat history
            st.chat_message("user").write(user_query)
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_query
            })
            
            # Get response from backend
            with st.chat_message("assistant"):
                with st.spinner("Processing your question..."):
                    response = send_chat_message(
                        message=user_query,
                        page_number=chat_page,
                        frontend_chat_history=st.session_state.chat_history
                    )
                    st.write(response)
            
            # Add assistant response to chat history
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response
            })
        
        # Control buttons
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