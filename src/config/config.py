import os
from dotenv import load_dotenv
from src.utils.logger import logger

load_dotenv()

# We dont need the api key in the config class for our use case, langchain will handle it
# So I will just check if it exists so I can raise an error if it doesn't
api_key = os.getenv("OPENAI_API_KEY", None)

if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set, please provide it in the .env file")

class _Config:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    # Model config
    OPENAI_MODEL_NAME: str = "gpt-4o-mini"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-large"

    # Text splitter config
    TEXT_SPLITTER_CHUNK_SIZE: int = 1200
    TEXT_SPLITTER_CHUNK_OVERLAP: int = 100

    # Vector store config - the number of results to return from the vector store retriever
    VECTOR_STORE_K: int = 5

    # Data config
    PDF_DATA_PATH: str = os.getenv("PDF_DATA_PATH", "data")
    CHROMA_DB_PATH: str = os.getenv("CHROMA_DB_PATH", "chroma_db")
    URL_TO_LOAD: str = os.getenv("URL_TO_LOAD", "https://www.promtior.ai")

    #App config
    PORT: int = int(os.getenv("PORT", 8000))
    HOST: str = os.getenv("HOST", "localhost")
    APP_TITLE: str = os.getenv("APP_TITLE", "LangChain Server")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0")
    APP_DESCRIPTION: str = os.getenv("APP_DESCRIPTION", "A simple api server using Langchain's Runnable interfaces")



CONFIG = _Config()
