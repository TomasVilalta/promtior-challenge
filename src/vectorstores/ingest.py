from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

from uuid import uuid4
import logging
import os
from pathlib import Path
# import the .env file
from dotenv import load_dotenv
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFRetriever:
    def __init__(self):
        # Get the project root directory (2 levels up from this file)
        current_file = Path(__file__)
        project_root = current_file.parent.parent.parent
        
        # Use absolute paths based on the project root
        self.data_path = os.path.join(project_root, "data")
        self.chroma_path = os.path.join(project_root, "chroma_db")
        
        logger.info(f"PDF path: {self.data_path}")
        logger.info(f"Chroma DB path: {self.chroma_path}")

    def load_documents(self):
        # Check if file exists before loading
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"PDF file not found at: {self.data_path}")
            
        loader = PyPDFDirectoryLoader(self.data_path)
        raw_documents = loader.load()
        return raw_documents
    
    def split_documents(self, raw_documents):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=100,
        )
        chunks = text_splitter.split_documents(raw_documents)
        return chunks
    
    def openai_embeddings(self):
        db = Chroma.from_documents(
            documents=self.split_documents(self.load_documents()),
            embedding=OpenAIEmbeddings(),
            persist_directory=self.chroma_path,
        )
        return db
    
    
    
