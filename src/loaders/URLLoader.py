from typing import List
from langchain.schema import Document
from langchain_community.document_loaders import RecursiveUrlLoader
from bs4 import BeautifulSoup
import re
import logging
from langchain_community.document_transformers import MarkdownifyTransformer
from bs4 import XMLParsedAsHTMLWarning
import warnings

# Ignore warnings about XMLParsedAsHTMLWarning, this is expected behavior
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

# Maybe move this to utils
def bs4_extractor(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    return re.sub(r"\n\n+", "\n\n", soup.text).strip()


class URLLoader:
    def validate(self, url: str) -> bool:
        """Validate the URL"""
        #could also make a get request to check if the url is valid
        return bool(re.match(r"https?://(?:www\\.)?[ a-zA-Z0-9./]+", url))

    
    def load(self, url: str) -> List[Document]:
        """Load documents from a list of URLs"""
        if not self.validate(url):
            raise ValueError("Invalid URL provided")
        loader = RecursiveUrlLoader(url, extractor=bs4_extractor)
        raw_documents = loader.load()
        # discard description from metadata
        for doc in raw_documents:
            doc.metadata.pop("description", None)

        return raw_documents
    
