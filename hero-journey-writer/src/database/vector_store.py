import os
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_anthropic import ChatAnthropic
from langchain_openai import OpenAIEmbeddings
import numpy as np

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

llm = ChatAnthropic(model="claude-3-opus-20240229")
embeddings = OpenAIEmbeddings()

class InMemoryVectorStore:
    def __init__(self):
        self.data = {}

    def upsert(self, vectors):
        for id, vector, metadata in vectors:
            self.data[id] = (vector, metadata)

    def query(self, vector, filter, top_k):
        results = []
        for id, (stored_vector, metadata) in self.data.items():
            if filter and not all(metadata.get(k) == v for k, v in filter.items()):
                continue
            similarity = np.dot(vector, stored_vector) / (np.linalg.norm(vector) * np.linalg.norm(stored_vector))
            results.append((id, similarity, metadata))
        results.sort(key=lambda x: x[1], reverse=True)
        return {
            'matches': [{'id': id, 'score': score, 'metadata': metadata} for id, score, metadata in results[:top_k]]
        }

def initialize_vector_store():
    index_name = "memgpt"  # Usa el nombre de tu índice existente
    try:
        return pc.Index(index_name)
    except Exception as e:
        print(f"Failed to initialize Pinecone index: {e}")
        print("Using in-memory vector store instead.")
        return InMemoryVectorStore()

index = initialize_vector_store()

def store_interaction(character, player_name, interaction, stage):
    vector = embeddings.embed_query(interaction)
    index.upsert([(f"{character}_{player_name}_{stage}", vector, {"interaction": interaction, "character": character, "player": player_name})])

def retrieve_interactions(character, player_name, query):
    vector = embeddings.embed_query(query)
    results = index.query(vector=vector, filter={"character": character, "player": player_name}, top_k=5)
    return [r['metadata']['interaction'] for r in results['matches']]

def summarize_character_memory(character, player_name):
    results = index.query(
        vector=[0] * 1536,  # Vector vacío para recuperar todos los resultados, ajustado a la dimensión de OpenAI
        filter={"character": character, "player": player_name},
        top_k=100  # Ajusta según sea necesario
    )
    
    interactions = [r['metadata']['interaction'] for r in results['matches']]
    
    summary_prompt = f"""
    Resume las siguientes interacciones entre el jugador {player_name} y el personaje {character}:
    
    {' '.join(interactions)}
    
    Proporciona un resumen conciso (3-4 oraciones) que capture:
    1. La impresión general que el personaje tiene del jugador
    2. Cualquier promesa o acuerdo importante hecho entre ellos
    3. Cualquier conflicto o tensión notable
    """
    
    return llm.invoke(summary_prompt).content
