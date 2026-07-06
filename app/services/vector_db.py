import json
import os
import torch
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DATA_PATH = os.path.join(BASE_DIR, "data","it_engineer_chatbot_150_fixed.json")
PERSIST_DIR = os.path.join(BASE_DIR, "chroma_db")
COLLECTION_NAME = "it_engineer_errors"

def load_json_data():
    with open(DATA_PATH, "r", encoding = "utf-8") as f:
        return json.load(f)
    

def build_document(item):
    search_content = f"""
{item.get('title', '')}
{item.get('error_message', '')}
{item.get('error_code') or ''}
{', '.join(item.get('keywords', []))}
{' '.join(item.get('examples', []))}
""".strip()
    metadata = {
        "id": item.get("id",""),
        "category": item.get("category", ""),
        "error_code": item.get("error_code", ""),
        "subcategory": item.get("subcategory", ""),
        "title": item.get("title", ""),
        "description": item.get("description", ""),
        "cause": " / ".join(item.get("cause", [])),
        "diagnosis": " / ".join(item.get("diagnosis", [])),
        "solution": " / ".join(item.get("solution", [])),
        "examples": " / ".join(item.get("examples", [])),
        "command_example": " / ".join(item.get("command_example", [])),
        "caution": item.get("caution", ""),
        "source_url": item.get("source_url", ""),
    }
    

    return Document(page_content=search_content, metadata=metadata)


def get_embedding_model():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"임베딩 모델 디바이스: {device}")

    return HuggingFaceEmbeddings(
        model_name="BAAI/bge-m3",
        model_kwargs={"device": device},
        encode_kwargs={"normalize_embeddings": True}
    )

embedding_model = get_embedding_model()
data = load_json_data()
documents = [build_document(item) for item in data]

if os.path.exists(PERSIST_DIR) and os.listdir(PERSIST_DIR):
    vectorstore =Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embedding_model,
        collection_name=COLLECTION_NAME,
    )
    print(f"기존 Chroma DB 로드 완료. 문서 수 : {vectorstore._collection.count()}")
else:
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        persist_directory=PERSIST_DIR,
        collection_name=COLLECTION_NAME,
    )
    print(f"Chroma DB 생성 완료. 문서 수 : {vectorstore._collection.count()}")
