import os
from dotenv import load_dotenv
from pinecone import Pinecone
from openai import OpenAI
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Cargar variables de entorno
load_dotenv(dotenv_path='.env')

# Verificar si las claves necesarias están presentes
if 'OPENAI_API_KEY' not in os.environ or 'PINECONE_API_KEY' not in os.environ:
    raise ValueError("Las claves OPENAI_API_KEY y PINECONE_API_KEY deben estar definidas en el archivo .env")

# Configurar OpenAI
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Configurar Pinecone
pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
index_name = 'puzzles'
index = pc.Index(index_name)

def get_embedding(text):
    try:
        response = client.embeddings.create(input=[text], model="text-embedding-ada-002")
        return response.data[0].embedding
    except Exception as e:
        logging.error(f"Error al generar embedding: {e}")
        return None

def buscar_en_pinecone(query: str, top_k: int = 3):
    """
    Busca acertijos en Pinecone basados en una consulta.
    
    Args:
    query (str): La consulta de búsqueda.
    top_k (int): Número de resultados a devolver.

    Returns:
    List[Dict]: Una lista de diccionarios con los acertijos encontrados.
    """
    try:
        # Genera el embedding para la consulta
        query_embedding = get_embedding(query)
        if query_embedding is None:
            return []

        # Realiza la búsqueda en Pinecone
        results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)

        # Procesa los resultados
        acertijos = []
        for match in results.matches:
            acertijo = {
                "score": match.score,
                "numero": match.metadata.get("numero", ""),
                "pregunta": match.metadata.get("pregunta", ""),
                "respuesta": match.metadata.get("respuesta", "")
            }
            acertijos.append(acertijo)

        return acertijos
    except Exception as e:
        logging.error(f"Error al buscar en Pinecone: {e}")
        return []