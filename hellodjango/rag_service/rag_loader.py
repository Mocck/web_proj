from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os

# 全局变量，用于存放 vectorstore 对象
vectorstore = None

def load_vectorstore():
    global vectorstore
    if vectorstore is not None:
        return vectorstore  # 已加载过则直接返回

    faiss_url = r"c:/users/zhaow/desktop/web_proj/rag/data/vectorstores/faiss_index"

    # 检查路径
    if not os.path.exists(faiss_url):
        raise FileNotFoundError(f"FAISS index not found at {faiss_url}")

    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh-v1.5")
    vectorstore = FAISS.load_local(faiss_url, embeddings, allow_dangerous_deserialization=True)
    print("✅ FAISS 向量索引已加载")
    return vectorstore
