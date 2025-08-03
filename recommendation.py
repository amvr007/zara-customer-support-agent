import pandas as pd
from llama_index.core import VectorStoreIndex, StorageContext, Document
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
from llama_index.embeddings.openai import OpenAIEmbedding
from dotenv import load_dotenv

load_dotenv()

df = pd.read_csv("data/zara.csv")  

def textual_rep(row): 
    textual_represensation = f"""
Name: {row['name']},
price: {row['price']},
currency: {row['currency']},
color: {row['color']},
Size: {row['size_list']},
category: {row['category']},
gender: {row['gender']}

description: {row['description']}
"""
    
    return textual_represensation
    

df['textual_representation'] = df.apply(textual_rep, axis=1)


docs = []
for i, rep in enumerate(df["textual_representation"]):
    docs.append(Document(text=rep, doc_id=str(i)))


def build_query_engine():
    chroma_client = chromadb.PersistentClient(path="./chroma_db")

    try:
        chroma_client.delete_collection("recommendation_docs")
    except chromadb.errors.NotFoundError:
        pass
    recommendation_collection = chroma_client.create_collection("recommendation_docs")      

    recomm_vector_store = ChromaVectorStore(chroma_collection=recommendation_collection)
    recomm_storage_context = StorageContext.from_defaults(vector_store=recomm_vector_store)

    embed_model = OpenAIEmbedding(model_name="text-embedding-3-small")

    recomendation_index = VectorStoreIndex.from_documents(
        docs, 
        storage_context=recomm_storage_context,
        embed_model=embed_model
    )

    query_engine = recomendation_index.as_query_engine(similarity_top_k=5)

    return query_engine

recommendation_engine = build_query_engine()

response = recommendation_engine.query("recommend 3 t-shirts under 50 dollars for women")
print(response)

