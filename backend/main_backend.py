from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
import uvicorn
import fitz # PyMuPdf
from dotenv import load_dotenv
import docx2txt
import os

app = FastAPI()

# ----------------------------------- CORE FUNCTIONS -----------------------------------
def extract_pdf_pages(file_bytes: bytes) -> list[str]:
    """
    Extracts text from each page of a PDF and returns a list where each index corresponds to a page.
    
    :param file_bytes: The raw bytes of the PDF file
    :return: List of strings, each string is the text from one page
    """
    pages_text = []

    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            page_text = page.get_text().strip()
            pages_text.append(page_text)

    return pages_text

def parse_file_contents(file_bytes: bytes, file_name: str) -> str:
    file_type = file_name.split('.')[-1].lower()

    if file_type == 'pdf':
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            return "\n".join([page.get_text() for page in doc])

    elif file_type in ['doc', 'docx']:
        temp_path = f"/tmp/{file_name}"
        with open(temp_path, 'wb') as f:
            f.write(file_bytes)
        return docx2txt.process(temp_path)

    else:
        raise ValueError("Unsupported file type")

# ------------------------------- DATA MODELS -------------------------------
class pdfParserRequest(BaseModel):
    file: UploadFile = File(...)

class ChatMessage(BaseModel):
    user_message: str
    assistant_response: str
    page_number: int

class ChatRequest(BaseModel):
    message: str
    page_number: int
    chat_history: list[ChatMessage] = []
    
# ------------------------------- FAST API ENDPOINTS -------------------------------
@app.post("/parse_pdf")
async def parse_pdf(file: UploadFile = File(...)):
    contents = await file.read()
    try:
         # Handle the case where filename might be None
        filename = file.filename or "unknown.pdf"
        text = parse_file_contents(contents, filename)
        print(f"✅ PDF parsed successfully: {filename}")
        return {"text": text}
    except ValueError as e:
        return {"error": str(e)}

@app.post("/chat")
async def chat(request: ChatRequest):
    """Handle chat messages with context from parsed PDF"""
    try:
        print(f"💬 Chat query received: '{request.message}'")
        print(f"📖 Page number: {request.page_number}")
        print(f"📚 Chat history length: {len(request.chat_history)}")

        response = f"Based on page {request.page_number} content and your question '{request.message}', here's the response..."
        
        return {"response": response}
        
    except Exception as e:
        return {"error": str(e)}

    
# ---------------------------- TESTING ENTRY POINT FOR TERMINAL ----------------------------
import tkinter as tk
from tkinter import filedialog

def main():
    # Hide the main tkinter window
    root = tk.Tk()
    root.withdraw()

    # Open the file dialog to select PDF or DOCX
    file_path = filedialog.askopenfilename(
        title="Select a PDF or DOCX file",
        filetypes=[("PDF files", "*.pdf"), ("Word Documents", "*.docx *.doc")]
    )

    if not file_path:
        print("No file selected.")
        return

    file_name = os.path.basename(file_path)
    with open(file_path, "rb") as f:
        file_bytes = f.read()
        
    page_wise_parsed = extract_pdf_pages(file_bytes)
    for i, page in enumerate(page_wise_parsed):
        print(f"\n--- Page {i+1} ---\n{page}")

    try:
        complete_parsed_text = parse_file_contents(file_bytes, file_name)
        print("\n--- Extracted Text Start ---\n")
        print(complete_parsed_text)
        print("\n--- Extracted Text End ---")
    except ValueError as e:
        print(f"Error: {e}")

# ---------------------------- RUN MODE ----------------------------

if __name__ == "__main__":
    # uvicorn.run("backend:app", host="127.0.0.1", port=8000, reload=True)
    main()
