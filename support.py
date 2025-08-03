from llama_index.readers.file import PDFReader, CSVReader
from llama_index.readers.json import JSONReader
from llama_index.core import VectorStoreIndex, StorageContext, Document
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
import chromadb
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

json_reader = JSONReader()
pdf_reader = PDFReader()
csv_reader = CSVReader()

data_dir = "data"
all_docs = []

for file in os.listdir(data_dir):
    file_path = os.path.join(data_dir, file)

    if file.endswith(".pdf"):
        docs = pdf_reader.load_data(file=file_path)
        all_docs.extend(docs)
    elif file.endswith(".json"):
        docs = json_reader.load_data(input_file=file_path)
        all_docs.extend(docs)
 

chroma_client = chromadb.PersistentClient(path="./chroma_db")

try:
    chroma_client.delete_collection("support_docs")
except chromadb.errors.NotFoundError:
    pass
support_collection = chroma_client.create_collection("support_docs")
support_vector_store = ChromaVectorStore(chroma_collection=support_collection)
support_storage_context = StorageContext.from_defaults(vector_store=support_vector_store)   
embed_model = OpenAIEmbedding(model_name="text-embedding-3-small")

support_index = VectorStoreIndex.from_documents(
    all_docs, 
    storage_context=support_storage_context,
    embed_model=embed_model
)

support_engine = support_index.as_query_engine()

