# AskMyDoc - PDF Chat Assistant

A Chrome extension that enhances PDF viewing with a side-by-side chat interface powered by Streamlit. Ask questions about any PDF you're viewing and get instant answers.

## Features

- **Split Screen Interface**: View PDFs and chat in the same browser tab
- **PDF Viewer**: Built with PDF.js for high-quality rendering
- **Interactive Chat**: Ask questions about the PDF content
- **FastAPI Backend**: Processes queries and generates responses
- **Streamlit Frontend**: Clean and responsive chat interface

## System Architecture

- **Extension**: Chrome extension that detects PDF files and injects the split UI
- **Frontend**: Streamlit application providing the chat interface
- **Backend**: FastAPI server that processes queries and returns responses

## Setup Instructions

### Prerequisites

- Python 3.8+
- Chrome/Chromium browser
- pip

### Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/AskMyDoc.git
cd AskMyDoc
```

2. Install backend dependencies:
```bash
cd backend
pip install -r requirements.txt
cd ..
```

3. Install frontend dependencies:
```bash
pip install streamlit
```

### Running the Application

1. Start both the backend and frontend services:
```bash
./run.sh
```

2. Load the extension in Chrome:
   - Open Chrome and navigate to `chrome://extensions/`
   - Enable "Developer mode" (toggle in top right)
   - Click "Load unpacked" and select the `extension` folder from this project

3. Open any PDF in Chrome to test the extension

## Usage

1. Open any PDF file in Chrome
2. The extension will automatically detect the PDF and inject the split screen interface
3. Ask questions about the PDF in the chat interface on the right
4. Receive responses based on the PDF content

## Troubleshooting

- If the extension doesn't appear, make sure both the backend (port 8000) and frontend (port 8501) services are running
- Check Chrome's DevTools console for error messages
- Ensure the PDF is properly loading in the viewer
- If communication fails, try refreshing the page

## Development

- `extension/content.js`: Handles PDF detection, UI injection, and API communication (combined functionality)
- `extension/pdf-viewer.html`: PDF viewer template
- `frontend/frontend_app.py`: Streamlit chat interface
- `backend/main_backend.py`: FastAPI backend for processing queries
- `backend/pdf_processor.py`: PDF content extraction and query processing
- `run.sh`: Script to start all services

## Recent Changes

- **Simplified Architecture**: Combined content.js and background.js into a single file
- **Improved Communication**: Direct API calls from content script to backend
- **Enhanced UI**: Split screen with adjustable panels
- **Better Error Handling**: More detailed error messages and fallbacks