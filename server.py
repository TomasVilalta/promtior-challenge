#!/usr/bin/env python
import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from src.config.config import CONFIG
from src.data_loader import load_and_setup_retriever
from src.chains.rag_chain import create_rag_chain
import traceback
from src.utils.logger import logger

# There's definitely a better way to load stuff before the app starts
try:
    retriever = load_and_setup_retriever()
    # Create the RAG chain
    rag_chain = create_rag_chain(retriever)
except Exception as e:
    logger.error(f"Error during initialization: {str(e)}")
    logger.error(traceback.format_exc())
    raise


# Initialize the FastAPI app
app = FastAPI(
    title=CONFIG.APP_TITLE,
    version=CONFIG.APP_VERSION,
    description=CONFIG.APP_DESCRIPTION,
)

# Allow all origins,
# THIS IS NOT SAFE FOR PRODUCTION, but it's fine for now
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}")
    logger.error(traceback.format_exc())
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred. Please try again later."},
    )

# create the route for the rag chain
add_routes(
    app,
    rag_chain,
    path="/promtior-chat",
)

# Health check endpoint
@app.get("/health")
async def health_check():
    try:
        # Simple check to see if the retriever is working
        docs = retriever.invoke("test")
        logger.info(f"Docs: {docs}")
        return {"status": "healthy"}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {"status": "unhealthy", "error": str(e)}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=CONFIG.HOST, port=CONFIG.PORT) 

