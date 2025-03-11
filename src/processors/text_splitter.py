from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List
from src.config.config import CONFIG

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CONFIG.TEXT_SPLITTER_CHUNK_SIZE,
    chunk_overlap=CONFIG.TEXT_SPLITTER_CHUNK_OVERLAP,
)

def split_documents(documents: List[Document]):
    return text_splitter.split_documents(documents)

