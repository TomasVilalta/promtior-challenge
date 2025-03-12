from typing import List
from langchain.schema import Document
from langchain_community.document_loaders import RecursiveUrlLoader
from bs4 import BeautifulSoup
import re

def bs4_extractor(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    return re.sub(r"\n\n+", "\n\n", soup.text).strip()

class URLLoader:
    def __init__(self, url: str):
        self.url = url

    def load(self) -> List[Document]:
        """Load documents from a list of URLs"""
        if not self.url:
            # Same as the pdf loader, raise an error if no urls are provided
            raise ValueError("No URLs provided")
        loader = RecursiveUrlLoader(self.url, extractor=bs4_extractor)
        raw_documents = loader.load()
        return raw_documents
    
