from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
import tempfile
import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

VECTOR_STORE = None
MEMORY = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

class ChatRequest(BaseModel):
    query: str
    history: list

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    global VECTOR_STORE, MEMORY

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    loader = PyPDFLoader(tmp_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    VECTOR_STORE = FAISS.from_documents(docs, embeddings)

    MEMORY.clear()

    os.remove(tmp_path)
    return {"message": "PDF processado e vetores armazenados."}

@app.post("/chat/")
async def chat_with_pdf(chat: ChatRequest):
    if VECTOR_STORE is None:
        return {"error": "Nenhum PDF foi processado ainda."}

    llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), temperature=0)

    MEMORY.chat_memory.messages = []
    for turn in chat.history:
        role = turn.get("role")
        content = turn.get("content")
        if role == "user":
            MEMORY.chat_memory.add_user_message(content)
        elif role == "assistant":
            MEMORY.chat_memory.add_ai_message(content)

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=VECTOR_STORE.as_retriever(),
        memory=MEMORY,
        return_source_documents=False
    )

    result = qa_chain.run(chat.query)
    return {"answer": result}
