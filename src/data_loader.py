import logging
from src.loaders.URLLoader import URLLoader
from src.loaders.PDFLoader import PDFLoader
from src.vectorstores.chromadb import ChromaDBManager
from src.processors.text_splitter import split_documents
from src.utils.logger import logger

def load_and_setup_retriever(url: str):
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
    
    # Load documents with basic error handling
    try:
        pdf_documents = pdf_loader.load()
        logger.info(f"Loaded {len(pdf_documents)} PDF documents")
    except Exception as e:
        logger.error(f"Error loading PDF documents: {str(e)}")
        pdf_documents = []  # Continue with empty list if PDF loading fails
        
    try:
        url_documents = url_loader.load()
        logger.info(f"Loaded {len(url_documents)} URL documents")
    except Exception as e:
        logger.error(f"Error loading URL documents from {url}: {str(e)}")
        url_documents = []  # Continue with empty list if URL loading fails
        
    # make sure we have at least something to load
    if not pdf_documents and not url_documents:
        logger.warning("No documents were loaded. The retriever may not work properly.")
        
    processed_documents = split_documents(pdf_documents + url_documents)
    
    vector_store_manager = ChromaDBManager()
    vector_store = vector_store_manager.create_vector_store(processed_documents)
    
    return vector_store_manager.get_retriever_from_vector_store(vector_store) 