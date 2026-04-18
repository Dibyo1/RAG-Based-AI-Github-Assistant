import os
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from github import Github, Auth

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

vectorstore = None
llm = None
prompt = None

def format_docs(docs):
    return "\n\n".join(
        f"[{doc.metadata.get('repo', 'Unknown')} - {doc.metadata.get('source', 'Unknown')}]\n{doc.page_content}"
        for doc in docs
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    global vectorstore, llm, prompt

    load_dotenv()

    if not os.path.exists("faiss_index"):
        raise RuntimeError("faiss_index not found. Run embed_store.py first.")

    if not os.getenv("GITHUB_TOKEN"):
        raise RuntimeError("GITHUB_TOKEN not set in .env")

    if not os.getenv("GEMINI_API_KEY"):
        raise RuntimeError("GEMINI_API_KEY not set in .env")

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.load_local(
        "faiss_index", embeddings, allow_dangerous_deserialization=True
    )

    llm = ChatGoogleGenerativeAI(
        model="gemma-4-31b-it",
        google_api_key=os.getenv("GEMINI_API_KEY")
    )

    prompt = PromptTemplate.from_template("""You are an expert portfolio advisor analyzing a developer's GitHub projects.
Use ONLY the context below to answer. If the answer isn't in the context, say so.
Always mention which repo you're referring to.
Always suggest improvements where relevant.
Be concise but specific.

Context:
{context}

Question: {question}
Answer:""")

    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str
    repo_filter: Optional[str] = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/repos")
def get_repos():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise HTTPException(status_code=500, detail="GITHUB_TOKEN not set in .env")
    try:
        auth = Auth.Token(token)
        g = Github(auth=auth)
        user = g.get_user()
        repos_data = []
        for repo in user.get_repos():
            if not repo.fork:
                repos_data.append({
                    "name": repo.name,
                    "description": repo.description,
                    "language": repo.language,
                    "stars": repo.stargazers_count,
                    "url": repo.html_url
                })
        return repos_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
def chat(req: ChatRequest):
    if not vectorstore or not llm or not prompt:
        raise HTTPException(status_code=500, detail="Server not correctly initialized")
    try:
        search_kwargs = {"k": 5}
        if req.repo_filter:
            search_kwargs["filter"] = {"repo": req.repo_filter}

        retriever = vectorstore.as_retriever(search_kwargs=search_kwargs)

        chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

        answer = chain.invoke(req.question)

        docs = retriever.invoke(req.question)
        sources = []
        seen = set()
        for doc in docs:
            repo = doc.metadata.get("repo", "Unknown")
            source = doc.metadata.get("source", "Unknown")
            if (repo, source) not in seen:
                seen.add((repo, source))
                sources.append({"repo": repo, "source": source})

        return {"answer": answer, "sources": sources}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def serve_index():
    return FileResponse("index.html")

@app.get("/chat-ui")
def serve_chat():
    return FileResponse("chat.html")