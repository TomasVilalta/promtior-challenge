from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from src.promptTemplates.rag_prompt import rag_prompt
from src.config.config import CONFIG

def create_rag_chain(retriever):
    """
    Create a RAG (Retrieval Augmented Generation) chain
    
    Args:
        retriever: The retriever to use for document retrieval
        
    Returns:
        The RAG chain
    """

    model = ChatOpenAI(model=CONFIG.OPENAI_MODEL_NAME)
    
    document_chain = create_stuff_documents_chain(
        model,
        rag_prompt
    )
    
    return (
        {"context": retriever, "input": RunnablePassthrough()}
        | document_chain
        | StrOutputParser()
    ) 