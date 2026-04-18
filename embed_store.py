from github_fetch import get_github_docs
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os
load_dotenv()

GITHUB_TOKEN=os.getenv("GITHUB_TOKEN")


# Step 1 — fetch
docs = get_github_docs(GITHUB_TOKEN)
print(f"Fetched {len(docs)} documents")

# Step 2 — chunk
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)
print(f"{len(chunks)} chunks ready for embedding")

# Step 3 — embed locally
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Step 4 — store and save
vectorstore = FAISS.from_documents(chunks, embeddings)
vectorstore.save_local("faiss_index")
print("Vector store saved!")