from langchain_core.prompts import ChatPromptTemplate

promptTemplate = ChatPromptTemplate.from_template(
    """
    You are a helpful assistant that can answer questions solely based on the following text:
    {context}
    Question: {input}
    Answer:
    """
)