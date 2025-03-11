from typing import List
from langchain.schema import Document
from langchain_community.document_loaders import WebBaseLoader

class URLLoader:
    def __init__(self, urls: List[str]):
        self.urls = urls

    def load(self) -> List[Document]:
        """Load documents from a list of URLs"""
        if not self.urls:
            # Same as the pdf loader, raise an error if no urls are provided
            raise ValueError("No URLs provided")
        loader = WebBaseLoader(self.urls)
        raw_documents = loader.load()
        return raw_documents
    

    

