import logging
from src.loaders.URLLoader import URLLoader
from src.loaders.PDFLoader import PDFLoader
from src.vectorstores.chromadb import ChromaDBManager
from src.processors.text_splitter import split_documents
from src.utils.logger import logger

def load_and_setup_retriever(url="https://www.promtior.ai"):
    """
    Load data from URL and PDF sources, process it, and set up a retriever
    
    Args:
        url: The URL to load data from
        
    Returns:
        A retriever for the loaded data
    """
    # Initialize loaders
    url_loader = URLLoader(url)
    pdf_loader = PDFLoader()
    
    # Load documents
    pdf_documents = pdf_loader.load()
    url_documents = url_loader.load()
    
    logger.info(f"Loaded {len(url_documents)} URL documents")
    logger.info(f"Loaded {len(pdf_documents)} PDF documents")

        
    # Split the documents into chunks
    processed_documents = split_documents(pdf_documents + url_documents)
    
    # Create the vector store
    vector_store_manager = ChromaDBManager()
    vector_store = vector_store_manager.create_vector_store(processed_documents)
    
    # Return the retriever
    return vector_store_manager.get_retriever_from_vector_store(vector_store) 