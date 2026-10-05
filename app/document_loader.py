from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_pdf(pdf_path: str):
    """
    Load a PDF and return its pages as LangChain Document objects.

    Each document contains:
    - page text
    - source filename
    - page number
    """

    loader = PyPDFLoader(pdf_path)

    documents = loader.load()

    return documents


def split_documents(documents):
    """
    Split PDF pages into smaller chunks suitable for
    LLM processing and retrieval.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
    )

    chunks = splitter.split_documents(documents)

    return chunks