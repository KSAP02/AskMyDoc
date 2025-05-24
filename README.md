---

# 📚 AskMyDoc: Interactive PDF Chat Assistant

AskMyDoc is an AI-powered assistant that allows users to interact conversationally with their PDF documents. Whether you’re reading research papers, technical documentation, or business reports, AskMyDoc makes it easy to ask detailed questions about specific pages and get intelligent, context-aware responses.

---

## 🚀 Features

* 📄 Page-wise intelligent context retrieval
* 🤖 ReAct-style LLM responses with chat history awareness
* 🧠 FAISS vector store for fast semantic search
* 🔍 Clarifying follow-up questions using reflective reasoning
* 🖥️ Split-screen UI for chat and PDF viewer

---

## ⚙️ Tech Stack

| Layer           | Tools/Tech Used                                    |
|----------------|-----------------------------------------------------|
| Backend         | Python, FastAPI, LangChain, JSearch API |
| Frontend        | Streamlit                                          |
| Vector Search | FAISS                             |
| LLM & NLP       | OpenAI LLMs |
| PDF Parsing   | PyMuPDF (fitz)                    |
| Agents          | ReAct, RAG, Chatbot, Embeddings|
| Agent Logic   | OpenAI GPT-3.5 Turbo              |
| Storage       | In-memory (for now)               |
| Embeddings      | OpenAI (`text-embedding-3-small`) |

---

## 🔄 Workflow Overview

### 🎛️ Frontend Workflow (Streamlit)

1. User uploads a PDF file.
2. PDF is displayed in an embedded viewer.
3. User selects a page and types a query in the chat window.
4. Streamlit sends a POST request to the FastAPI backend with:

   * User query
   * Selected page number
   * Chat history

---

### 🔧 Backend Workflow (FastAPI)

```mermaid
graph TD
    A[User uploads PDF] --> B[Parse PDF into pages]
    B --> C[Chunk each page into text chunks]
    C --> D[Embed chunks using OpenAI API]
    D --> E[Store embeddings in FAISS per page]
    F[User sends a query] --> G[Retrieve context from FAISS using page±1]
    G --> H[Assemble prompt with context + history]
    H --> I[Call LLM with ReAct system prompt]
    I --> J[Send response back to frontend]
```

---

## 🧠 Backend Internals

* **PDF Parsing**: Uses PyMuPDF to extract clean page-wise text.
* **Chunking**: Each page's text is split into semantically coherent/aware chunks using langchain semantic chunking method.
* **Embedding**: Chunks are embedded using OpenAI's embedding model.
* **Vector Stores**: A separate FAISS index is built for each page.
* **Context Retrieval**:

  * From FAISS: Retrieves top-k relevant chunks from the current page and neighboring pages.
* **LLM Prompt Assembly**:

  * Constructs a system prompt guiding the ReAct reasoning agent.
  * Injects the user query, relevant context, and conversation history.
* **Response Generation**:

  * Uses GPT-3.5-Turbo to produce natural, context-aware answers or follow-up questions.

---

## 🔮 Future Work

* **Context Classification**:

  * Differentiate between generic (global document-level) and targeted (page-specific) queries to dynamically choose between full-text vs. page-level retrieval.
* **Global Embedding Search**:

  * Build a full-document FAISS index for answering more abstract, cross-page questions.
* **Improved Chunking**:

  * Implement semantic-aware chunking using BERTScore or token-overlap thresholds.

---

## 📦 Installation

```bash
git clone https://github.com/your-repo/askmydoc.git
cd askmydoc
pip install -r requirements.txt
streamlit run app.py
```

---

## 🛠️ Endpoints Summary

| Endpoint            | Method | Description                                 |
| ------------------- | ------ | ------------------------------------------- |
| `/parse_pdf`        | POST   | Parses and chunks PDF, builds vector stores |
| `/get_llm_response` | POST   | Returns chat-based response using context   |

---

## 💡 How to Contribute

We welcome contributions! Whether it's UI improvements, new features, or better vector handling—every bit helps.

---
