from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

import logging
import os
from pathlib import Path
from typing import List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class URLRetriever:
    def __init__(self):
        # Get the project root directory (2 levels up from this file)
        current_file = Path(__file__)
        project_root = current_file.parent.parent.parent

        self.chroma_path = os.path.join(project_root, "chroma_db_url")
        logger.info(f"Chroma DB path for URLs: {self.chroma_path}")

    def load_urls(self):
        page_url = "https://www.promtior.ai/service"
        loader = WebBaseLoader(page_url)
        docs = []
        for doc in loader.load():
            docs.append(doc)
        return docs
    
    def create_embeddings(self):
        docs = self.load_urls()
        if (os.path.exists(self.chroma_path)):
            db = Chroma(
                embedding_function=OpenAIEmbeddings(),
                persist_directory=self.chroma_path,
            )
            return db
        else:
            db = Chroma.from_documents(
                documents=docs,
                embedding=OpenAIEmbeddings(),
                persist_directory=self.chroma_path,
            )
            return db
