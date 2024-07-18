import os
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))

index_name = "hero-journey"

# Asegúrate de que el índice existe
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric='cosine'
    )

index = pc.Index(index_name)

def store_response(user_id: str, stage: str, response: str, embedding: list):
    index.upsert(vectors=[(f"{user_id}_{stage}", embedding, {"response": response, "stage": stage})])

def find_similar_responses(stage: str, embedding: list, top_k: int = 5):
    results = index.query(vector=embedding, filter={"stage": stage}, top_k=top_k)
    return [result.metadata['response'] for result in results.matches]
