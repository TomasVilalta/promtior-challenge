from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from src.promptTemplates.rag_prompt import rag_prompt

def create_rag_chain(retriever):
    """
    Create a RAG (Retrieval Augmented Generation) chain
    
    Args:
        retriever: The retriever to use for document retrieval
        
    Returns:
        The RAG chain
    """
    # Initialize the model
    model = ChatOpenAI(model="gpt-4o-mini")
    
    # Create the document chain
    document_chain = create_stuff_documents_chain(
        model,
        rag_prompt
    )
    
    # Create and return the RAG chain
    return (
        {"context": retriever, "input": RunnablePassthrough()}
        | document_chain
        | StrOutputParser()
    ) 