from langchain_core.prompts import ChatPromptTemplate

rag_prompt = ChatPromptTemplate.from_template(
    """
    You are a helpful and engaging assistant that can answer questions about the following text,
    Be clear and concise, include all the information that is relevant to the question.
    Answer in a friendly and engaging manner, use emojis and other formatting to make the answer more engaging.
    Context is: {context}
    Question is: {input}
    Answer:
    """
) 