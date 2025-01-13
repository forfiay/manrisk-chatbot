from langchain_chroma import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain.schema import Document
from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.utils import filter_complex_metadata
import shutil
import os

DIRECTORY = "file"

def load_docs(file_path):
    document_loader = PyPDFDirectoryLoader(file_path)
    return document_loader.load()

documents = load_docs(DIRECTORY)

def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=500,
        length_function=len,
        add_start_index=True,
    )

    chunks = text_splitter.split_documents(documents)
    chunks = filter_complex_metadata(chunks)
    return chunks

chunks = split_text(documents)

CHROMA_PATH = "chroma"
embeddings = FastEmbedEmbeddings()

def save_to_chroma(chunks: list[Document]):
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
    vector_store = Chroma.from_documents(chunks, embeddings, persist_directory=CHROMA_PATH)
    
save_to_chroma(chunks)
