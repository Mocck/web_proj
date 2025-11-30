import os
import re
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import glob


#  数据准备 (Data Preparation)
# 1. 获取所有 Markdown 文件路径
markdown_files = glob.glob("./markdown/*.md")

# 2. 读取所有文件
docs = []
for file_path in markdown_files:
    loader = TextLoader(file_path, encoding="utf-8")
    docs.extend(loader.load())

# 1. 文本分块
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
texts = text_splitter.split_documents(docs)

# 2. 索引构建 (Index Construction)
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-zh-v1.5", # 上下文窗口为512个token
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)

# 3. 构建 FAISS 向量数据库
vectorstore = FAISS.from_documents(texts, embeddings)

# 4. 保存索引到本地（建议存储在 data 目录）
save_path = "./data/vectorstores/faiss_index"
os.makedirs(save_path, exist_ok=True)
vectorstore.save_local(save_path)
