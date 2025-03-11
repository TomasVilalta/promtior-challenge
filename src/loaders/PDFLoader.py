from langchain_community.document_loaders import PyPDFDirectoryLoader
from src.config.config import CONFIG
import logging
import os
from pathlib import Path
from typing import List
from langchain.schema import Document

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# I would probably make a factory for this? 
# Or maybe a singleton for every loader type, this is fine for now
class PDFLoader:
    def __init__(self, data_path = CONFIG.PDF_DATA_PATH):
        # This is probably ugly and not the best way to do this, but it works, sorry :(
        current_file = Path(__file__)
        project_root = current_file.parent.parent.parent
        self.data_path = os.path.join(project_root, data_path)
        logger.info(f"PDF path: {self.data_path}")


    def validate(self) -> bool:
        """Check if directory exists and contains PDF files"""
        if not os.path.exists(self.data_path):
            return False
        
        # Check if directory contains at least one PDF file
        pdf_files = [f for f in os.listdir(self.data_path) 
                    if f.lower().endswith('.pdf')]
        return len(pdf_files) > 0


    def load(self) -> List[Document]:
        """Load documents from PDF directory"""
        if not self.validate():
            # Imma raise an error here, ideally the app shouldn't crash and 
            # just return an empty list, but this is a little easier and helps 
            # with debugging
            raise FileNotFoundError(f"No PDF files found in: {self.data_path}")
        loader = PyPDFDirectoryLoader(self.data_path)
        return loader.load()
    
    
    
