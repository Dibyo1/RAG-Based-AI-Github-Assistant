from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")

# Step 1 — load vector store
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# Step 2 — prompt
prompt = ChatPromptTemplate.from_template("""
You are an expert portfolio advisor analyzing a developer's GitHub projects.
Use ONLY the context below to answer. If the answer isn't in the context, say so.
Always mention which repo you're referring to.

Context:
{context}

Question: {question}

Answer:
""")

# Step 3 — Gemini as LLM
llm = ChatGoogleGenerativeAI(
    model="gemma-4-31b-it",
    google_api_key=GEMINI_API_KEY,
    temperature=0.3
)

# Step 4 — chain
def format_docs(docs):
    return "\n\n".join(
        f"[{d.metadata.get('repo', 'unknown')} - {d.metadata.get('source', '')}]\n{d.page_content}"
        for d in docs
    )

chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# Step 5 — chat loop
print("GitHub Portfolio Advisor ready! Type 'exit' to quit.\n")
while True:
    question = input("You: ").strip()
    if question.lower() == "exit":
        break
    if not question:
        continue
    answer = chain.invoke(question)
    print(f"\nAdvisor: {answer}\n")