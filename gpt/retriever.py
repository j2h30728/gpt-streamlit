from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import UnstructuredFileLoader
from langchain.embeddings import CacheBackedEmbeddings, OpenAIEmbeddings
from langchain.storage import LocalFileStore
from langchain.vectorstores.faiss import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import SitemapLoader


import os

def get_document_retriever(input_file, api_key):
    docs = _split_document_into_chunks(input_file)
    cached_embeddings = _create_cached_embeddings(input_file.name, api_key)
    
    vector_store = FAISS.from_documents(docs, cached_embeddings)
    retriever = vector_store.as_retriever()
    return retriever

def get_website_retriever(url,api_key):
    docs = _split_website_into_chunk(url)
    cached_embeddings = _create_cached_embeddings(url, api_key)

    vector_store = FAISS.from_documents(docs, cached_embeddings)
    retriever = vector_store.as_retriever()
    return retriever


def _split_document_into_chunks(input_file):

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

def _create_cached_embeddings(cache_name, api_key):

    embeddings = OpenAIEmbeddings(api_key=api_key)
    cache_dir = LocalFileStore(f"./.cache/embeddings/{cache_name}")
    cached_embeddings = CacheBackedEmbeddings.from_bytes_store(embeddings, cache_dir)
    return cached_embeddings


def _split_website_into_chunk(url):
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=1000,
    chunk_overlap=200,
    )
    loader = SitemapLoader(
        url,
        filter_urls=[
            r"^(.*\/ai-gateway  \/).*",
            r"^(.*\/vectorize\/).*",
            r"^(.*\/workers-ai\/).*",
        ],
        parsing_function=_parse_page,
    )
    loader.requests_per_second = 2
    docs = loader.load_and_split(text_splitter=splitter)
    return docs




def _parse_page(soup):
    header = soup.find("header")
    footer = soup.find("footer")
    if header:
        header.decompose()
    if footer:
        footer.decompose()
    return (
        str(soup.get_text())
        .replace("\n", " ")
        .replace("\xa0", " ")
    )
