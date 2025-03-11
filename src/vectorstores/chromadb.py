from src.config.config import CONFIG
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from typing import List
import os

# Im gonna just recreate the db each time and not worry about persisting the db between runs
# If I were to persist the db and host it somewhere, I would make some functions to handle
# some more db operations like adding documents, deleting documents, etc.
# Reference for future me: https://python.langchain.com/docs/integrations/vectorstores/chroma/
class ChromaDBManager:
    """A class for creating and managing ChromaDB instances.
        Args:
            path (str): The path to the ChromaDB instance, defaults to CONFIG.CHROMA_DB_PATH
    """
    def __init__(self, path: str = CONFIG.CHROMA_DB_PATH):
        if not path:
            raise ValueError("ChormaDB: Path is required, either provide it on init or set the CHROMA_DB_PATH in the config")
        self.path = path

        # This could be instantiated on a new embeddings manager class probably
        self.embeddings = OpenAIEmbeddings(model=CONFIG.OPENAI_EMBEDDING_MODEL)


    def create_vector_store(self, documents: List[Document]):
        """Create a vector store from a list of documents.
        Args:
            documents (List[Document]): The documents to create the vector store from.
        Returns:
            ChromaDB: The ChromaDB instance.
        """
        if not documents:
            raise ValueError("ChormaDB: Provide a list of documents")
        
        self.vector_store = Chroma.from_documents(documents, self.embeddings, persist_directory=self.path)
        # Return the db instance
        return self.vector_store
        
    def get_retriever_from_vector_store(self, vector_store: Chroma):
        """Get a retriever from a vector store.
        Args:
            vector_store (Chroma): The vector store to get the retriever from.
        Returns:
            Retriever: The retriever.
        """
        return vector_store.as_retriever(kwargs={"k": CONFIG.VECTOR_STORE_K})
