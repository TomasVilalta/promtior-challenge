from langchain_community.document_loaders import PyPDFDirectoryLoader
from src.config.config import CONFIG
import logging
import os
from pathlib import Path
from typing import List
from langchain.schema import Document


# I would probably make a factory for this? 
# Also maybe make a base class for all loaders?
class PDFLoader:
    def validate(self, data_path) -> bool:
        """Check if directory exists and contains PDF files"""
        if not os.path.exists(data_path):
            return False
        
        # Check if directory contains at least one PDF file
        pdf_files = [f for f in os.listdir(data_path) 
                    if f.lower().endswith('.pdf')]
        return len(pdf_files) > 0


    def load(self, data_path) -> List[Document]:
        """Load documents from PDF directory"""
        if not self.validate(data_path):
            # Imma raise an error here, ideally the app shouldn't crash and 
            # just return an empty list, but this is a little easier and helps 
            # with debugging
            raise FileNotFoundError(f"No PDF files found in: {data_path}")
        loader = PyPDFDirectoryLoader(data_path)
        return loader.load()
    
    
    
