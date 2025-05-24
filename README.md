# 📚 AskMyDoc: Interactive PDF Chat Assistant

AskMyDoc is a modern, user-friendly application that lets you have intelligent conversations with your PDF documents. Built with a sleek web interface, it combines the power of document processing with an intuitive chat experience.

## 🌟 Features

- **Interactive PDF Viewer**: Full-screen, responsive PDF display with page navigation
- **Context-Aware Chat**: Ask questions about specific pages of your document
- **Smart History**: Keeps track of your conversations with page references
- **Clean Interface**: Split-screen design with PDF viewer and chat side by side

## 🏗️ Architecture

The project is built with a modern tech stack:

- **Frontend**: Streamlit for a responsive and interactive UI
- **Backend**: FastAPI for high-performance API endpoints
- **Document Processing**: PyMuPDF for efficient PDF handling
- **Browser Extension**: For enhanced PDF viewing capabilities

## 🔧 Components

1. **Frontend (`frontend/`)**: 
   - Streamlit-based web interface
   - Real-time PDF viewing
   - Chat interface with page selection
   - Session management

2. **Backend (`backend/`)**: 
   - FastAPI server
   - Document parsing and text extraction
   - Chat message processing
   - PDF page management

3. **Extension (`extension/`)**: 
   - Browser integration
   - Enhanced PDF viewing
   - Custom styling and controls

4. **Agents (`agents/`)**: 
   - AI processing modules
   - Document analysis
   - Response generation

## 🚀 Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the backend server:
   ```bash
   uvicorn backend.main_backend:app --reload
   ```

3. Launch the frontend:
   ```bash
   streamlit run frontend/frontend_app.py
   ```

## 💡 How to Use

1. Upload your PDF document
2. Navigate through pages using the built-in viewer
3. Select a specific page to ask questions about
4. Type your questions in the chat interface
5. Get contextual responses based on the document content

## 🔄 Flow

1. **Document Upload**: PDFs are parsed and processed on upload
2. **Page Navigation**: Users can browse the document freely
3. **Question Asking**: Select a page and ask questions
4. **Smart Responses**: Get answers based on document context
5. **History Tracking**: Keep track of all Q&A with page references

## 🛠️ Technical Details

- **PDF Processing**: Uses PyMuPDF for accurate text extraction
- **API Communication**: RESTful endpoints with FastAPI
- **State Management**: Streamlit session state for user data
- **UI Components**: Custom CSS for optimal viewing experience

## 📋 Requirements

- Python 3.8+
- FastAPI
- Streamlit
- PyMuPDF
- Additional dependencies in `requirements.txt`

---

🎯 **Goal**: Make document interaction as natural as chatting with a knowledgeable assistant who has read and understood your documents thoroughly.
