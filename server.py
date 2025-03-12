#!/usr/bin/env python
import logging
from fastapi import FastAPI
from langserve import add_routes
from src.config.config import CONFIG
from src.data_loader import load_and_setup_retriever
from src.chains.rag_chain import create_rag_chain


# Load data and set up retriever
retriever = load_and_setup_retriever(CONFIG.URL_TO_LOAD)

# Create the RAG chain
rag_chain = create_rag_chain(retriever)

# Initialize the FastAPI app
app = FastAPI(
    title=CONFIG.APP_TITLE,
    version=CONFIG.APP_VERSION,
    description=CONFIG.APP_DESCRIPTION,
)

# Add routes for the RAG endpoint
add_routes(
    app,
    rag_chain,
    path="/rag",
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=CONFIG.HOST, port=CONFIG.PORT) 

