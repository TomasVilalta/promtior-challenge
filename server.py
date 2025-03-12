#!/usr/bin/env python
from fastapi import FastAPI
from langserve import add_routes
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from src.config.config import CONFIG
import logging
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
# urls = ["https://www.promtior.ai", "https://www.promtior.ai/services", "https://www.promtior.ai/use-cases", "https://www.promtior.ai/contacto"]
url = "https://www.promtior.ai"

urlLoader= URLLoader(url)
pdfLoader = PDFLoader()

pdfDocuments = pdfLoader.load()
urlDocuments = urlLoader.load()

logger.info(urlDocuments[0].page_content[:1000])

# Split the documents into chunks
processedDocuments = split_documents(pdfDocuments + urlDocuments)

# Create the vector store
vectorStoreManager = ChromaDBManager()
vectorStore = vectorStoreManager.create_vector_store(processedDocuments)
retriever = vectorStoreManager.get_retriever_from_vector_store(vectorStore)


# Create the prompt template with the correct input parameter name
prompt = ChatPromptTemplate.from_template(
    """
    You are a helpful, friendly, and engaging assistant that can answer questions about the following text,
    you are eager to get people excited about the topic and help them understand it better.
    if the user asks for a topic that is not related to the context, mention that you are only able to answer questions about the context provided.
    Context is: {context}
    Questionis: {input}
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


# Create the document chain
document_chain = create_stuff_documents_chain(
    model,
    prompt
)


rag_chain=(
    {"context": retriever, "input": RunnablePassthrough()}
    |
    prompt
    |
    model
    |
    StrOutputParser()
)

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=CONFIG.HOST, port=CONFIG.PORT) 

