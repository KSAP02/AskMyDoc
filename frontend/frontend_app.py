import streamlit as st
import requests
import streamlit.components.v1 as components

BACKEND_URL = "http://localhost:8000/api/query"

st.set_page_config(
    page_title="AskMyDoc Chat",
    page_icon="💬",
    layout="wide"
)

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Add a session state for background processing
if "processing" not in st.session_state:
    st.session_state.processing = False

# Add a session state for the last query
if "last_query" not in st.session_state:
    st.session_state.last_query = None

# Display chat interface
st.title("📄 AskMyDoc")
st.write("Ask me anything about the PDF you're viewing!")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
query = st.chat_input("Ask a question about the document...", disabled=st.session_state.processing)

# Function to send query with PDF context if possible
def send_query(query):
    # First check if we're running inside the extension
    bridge_available = st.session_state.get("bridge_available", False)
    
    # Run this check on page load
    component_html = f"""
    <script>
      // Check if bridge API is available
      window.addEventListener('load', function() {
        // Check for bridge function
        const bridgeAvailable = typeof window.askWithPdfContext === 'function' || 
                               (window.parent && typeof window.parent.askWithPdfContext === 'function');
        
        // Store in session state
        window.parent.postMessage({
          type: 'BRIDGE_CHECK',
          available: bridgeAvailable
        }, '*');
      });
    </script>
    """
    components.html(component_html, height=0)
    
    try:
        if bridge_available:
            # Use the bridge API (with PDF context)
            # This would need a streamlit component to execute JavaScript
            # For now, we'll use direct backend call
            response = requests.post(BACKEND_URL, json={"query": query})
        else:
            # Direct backend call (no PDF context)
            response = requests.post(BACKEND_URL, json={"query": query})
            
        return response.json()
        
    except Exception as e:
        return {"error": str(e)}
