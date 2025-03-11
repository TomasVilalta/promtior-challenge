#!/usr/bin/env python
from fastapi import FastAPI
from langserve import add_routes
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from src.config.config import CONFIG
import logging
from src.vectorstores.url_retriever import URLRetriever
from src.loaders.URLLoader import URLLoader
from src.loaders.PDFLoader import PDFLoader
from src.vectorstores.chromadb import ChromaDBManager
from src.processors.text_splitter import split_documents
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('uvicorn.error')

# URLs to include in the retriever (can be configured as needed)
urls = [
    "https://www.promtior.ai/service"
]

urlLoader= URLLoader(urls)
pdfLoader = PDFLoader()

# pdfDocuments = pdfLoader.load()
urlDocuments = urlLoader.load()

# Split the documents into chunks
processedDocuments = split_documents(urlDocuments)

# Create the vector store
vectorStoreManager = ChromaDBManager()
vectorStore = vectorStoreManager.create_vector_store(processedDocuments)
retriever = vectorStoreManager.get_retriever_from_vector_store(vectorStore)

# Create the prompt template with the correct input parameter name
prompt = ChatPromptTemplate.from_template(
    """
    You are a helpful assistant that can answer questions solely based on the following text:
    {context}
    Question: {input}
    Answer:
    """
)

model = ChatOpenAI(model="gpt-4o-mini")
document_chain = create_stuff_documents_chain(
    model,
    prompt
)

rag_chain= (
    {"context": retriever, "input": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)








# # Create the document chain
# document_chain = create_stuff_documents_chain(
#     model,
#     prompt
# )

# rag_chain=create_retrieval_chain(
#     retriever,
#     document_chain
# )

# rag_chain=(
#     {"context": retriever, "input": RunnablePassthrough()}
#     |
#     prompt
#     |
#     model
#     |
#     StrOutputParser()
# )

# # Initialize the FastAPI app
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

# Add routes for the joke endpoint
md1 = ChatOpenAI(model="gpt-4o-mini")
prt2 = ChatPromptTemplate.from_template("tell me a joke about {topic}")
add_routes(
    app,
    prt2 | md1,
    path="/joke",
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=CONFIG.HOST, port=CONFIG.PORT) 

