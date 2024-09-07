from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import UnstructuredFileLoader
from langchain.embeddings import CacheBackedEmbeddings, OpenAIEmbeddings
from langchain.storage import LocalFileStore
from langchain.vectorstores.faiss import FAISS

import os

def get_retriever(input_file, api_key):
    docs = split_document_into_chunks(input_file)
    cached_embeddings = create_cached_embeddings(input_file, api_key)
    
    vectorstore = FAISS.from_documents(docs, cached_embeddings)
    retriever = vectorstore.as_retriever()
    return retriever



def split_document_into_chunks(input_file):

    file_content = input_file.read()

    file_dir = "./.cache/files"
    os.makedirs(file_dir, exist_ok=True)  # 디렉토리가 없으면 생성

    file_path = f"./.cache/files/{input_file.name}"

    with open(file_path, "wb") as f:
        f.write(file_content)

    splitter = CharacterTextSplitter.from_tiktoken_encoder(
        separator="\n",
        chunk_size=600,
        chunk_overlap=100,
    )
    loader = UnstructuredFileLoader(file_path)
    docs = loader.load_and_split(text_splitter=splitter)
    return docs

def create_cached_embeddings(input_file, api_key):

    embeddings = OpenAIEmbeddings(api_key=api_key)
    cache_dir = LocalFileStore(f"./.cache/embeddings/{input_file.name}")
    cached_embeddings = CacheBackedEmbeddings.from_bytes_store(embeddings, cache_dir)
    return cached_embeddings
