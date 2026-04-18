# RAG-Based AI GitHub Assistant ("The Curator") 🧠💻

A modern, full-stack AI coding assistant that acts as your personalized GitHub Portfolio Advisor. Built with **FastAPI**, **LangChain**, and **Google Gemini**, this tool pulls your GitHub repositories, indexes them locally using **FAISS** vector embeddings, and provides a stunning, interactive chat interface to answer highly specific queries about your coding structures, tech stacks, and architectural decisions.

## ✨ Features

- **Retrieval-Augmented Generation (RAG):** Accurately answers architectural and codebase questions strictly grounded in your actual GitHub project files.
- **Live GitHub Integration:** Dynamically fetches and categorizes your non-forked personal repositories.
- **FastAPI Backend:** Lightweight, lightning-fast Python server providing seamless data flow.
- **Vanilla JS + HTML Frontend:** Blazing fast, reactive user interface styled with modern Tailwind CSS.
- **Rich AI Output:** Code syntax highlighting via `highlight.js` and markdown parsing via `marked.js` out of the box.
- **Knowledge Graphing Built-In:** Supports visual code ecosystem mapping using the `graphifyy` library.

---

## 🛠️ Tech Stack

**Backend System:**
- **[FastAPI](https://fastapi.tiangolo.com/)**: REST API and static file serving.
- **[LangChain](https://www.langchain.com/)**: Orchestration of the RAG pipeline.
- **[FAISS](https://faiss.ai/)**: Facebook AI Similarity Search for local vector storage.
- **[HuggingFace Sentence Transformers](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)**: Open-source embedding models (`all-MiniLM-L6-v2`).
- **[Google Gemini](https://ai.google.dev/)**: Powerful LLM integration (`gemma-4-31b-it` / `gemini-1.5-flash`).
- **[PyGithub](https://pygithub.readthedocs.io/en/latest/)**: Direct communication with the GitHub API.

**Frontend Interface:**
- **Vanilla JavaScript**: Pure JS logic for seamless API fetching and page state.
- **Tailwind CSS**: Modern utility-first styling for dark mode zen-like UI.
- **Marked.js & Highlight.js**: Safe markdown bubble generation and code formatting.

---

## 🚀 Getting Started

### 1. Prerequisites 
- **Python 3.10+**
- A GitHub Personal Access Token (PAT).
- A Google Gemini API Key.

### 2. Installation Setup

Clone the repository and jump into it:
```bash
git clone https://github.com/Dibyo1/RAG-Based-AI-Github-Assistant.git
cd RAG-Based-AI-Github-Assistant
```

Install the required Python dependencies:
```bash
pip install fastapi uvicorn python-dotenv langchain langchain-community langchain-google-genai langchain-huggingface faiss-cpu sentence-transformers PyGithub
```

### 3. Environment Variables
Create a `.env` file in the root directory and populate it with your specific API keys:

```ini
GITHUB_TOKEN=your_github_personal_access_token_here
GEMINI_API_KEY=your_google_gemini_api_key_here
```

### 4. Build the Local Vector Database
Before launching the server, you need to embed your GitHub projects. Run the embedding script to generate the local `faiss_index` folder:

```bash
python embed_store.py
```

### 5. Fire up the Development Server
Run the FastAPI application via `uvicorn`. This serves both the backend pipeline and the static frontend UI.

```bash
uvicorn main:app --reload --port 8000
```

Simply open your browser to [http://localhost:8000](http://localhost:8000) and step into the **Welcome Screen** to begin chatting with The Curator!

---

## 🏗️ Project Architecture Overview

```text
├── .env                  # Secure Environment Config
├── .gitignore            # Hidden Files/Caches configuration 
├── chat.html             # Advisor Chat Interface UI
├── index.html            # Landing / Welcome Page
├── embed_store.py        # Fetches Code & Generates Local FAISS Vector Embeddings
├── github_fetch.py       # Helper functions to securely connect to PyGithub
├── main.py               # Complete FastAPI Server and LCEL Action Chain
├── rag_chain.py          # (Optional Setup) Logic components 
├── faiss_index/          # Auto-generated offline vector database map
└── graphify-out/         # Visual graph exports 
```
