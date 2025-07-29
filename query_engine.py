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
 

df = pd.read_csv("data/zara.csv", encoding='utf-8')   

#data preprocessing
for i, item in enumerate(df["brand"]):
    if item == "ZARAHOME": 
      df =  df.drop(index=i)
df = df.reset_index(drop=True)
df = df.drop(["condition", "currency"], axis=1)
df['product_id'] = df.index
new_order = ["product_id", "images", "url", "name", "description", "brand", "color", "size_list", "price"]
df = df[new_order]

# Convert DataFrame to Document objects
product_docs = []
for _, row in df.iterrows():
    doc_text = f"Product ID: {row['product_id']}\nName: {row['name']}\nDescription: {row['description']}\nBrand: {row['brand']}\nColor: {row['color']}\nPrice: {row['price']}\nSize List: {row['size_list']}\nURL: {row['url']}"
    doc = Document(text=doc_text, doc_id=str(row['product_id']))
    product_docs.append(doc)

chroma_client = chromadb.PersistentClient(path="./chroma_db")

support_collection = chroma_client.get_or_create_collection("support_docs")
support_vector_store = ChromaVectorStore(chroma_collection=support_collection)
support_storage_context = StorageContext.from_defaults(vector_store=support_vector_store)


recomm_collection = chroma_client.get_or_create_collection("recomm_docs")
recomm_vector_store = ChromaVectorStore(chroma_collection=recomm_collection)
recomm_storage_context = StorageContext.from_defaults(vector_store=recomm_vector_store)

embed_model = OpenAIEmbedding(model_name="text-embedding-3-small")

support_index = VectorStoreIndex.from_documents(
    all_docs, 
    storage_context=support_storage_context,
    embed_model=embed_model
)

recomendation_index = VectorStoreIndex.from_documents(
    product_docs, 
    storage_context=recomm_storage_context,
    embed_model=embed_model
)

support_engine = support_index.as_query_engine()

recommendation_engine = recomendation_index.as_query_engine()
