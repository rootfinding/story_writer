import os
from typing import Dict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from sqlalchemy import create_engine
from intro_writer.scenary import generate_scenary
from intro_writer.agents_def import AgentState
from intro_writer.flow_graph import flow_graph
from langchain_core.runnables import RunnableConfig
import logging


print(os.getcwd())

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_config() -> None:
    """Load environment variables and set up configuration."""
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    os.environ["OPENAI_API_KEY"] = openai_api_key



def initialize_state() -> Dict:
    """Initialize the game state."""
    return {
        "max_desafios": 2,
        "cantidad_desafios": 0,
        "desafios_resueltos": 0,
        "story": [],
        "puzzle_solution": "N/A"
    }

def get_user_input() -> Dict[str, str]:
    """Get user input for hero name and favorite candy."""
    return {
        "heroe": input("¿Cuál es el nombre de tu héroe? "),
        "caramelo": input("¿Cuál es tu dulce favorito? ")
    }

def setup_database():
    """Set up database connection."""
    db_url = os.getenv("DATABASE_URL", "postgresql://user:password@langgraph-postgres/dbname")
    try:
        engine = create_engine(db_url)
        # Puedes agregar aquí lógica adicional para verificar la conexión si lo deseas
        logger.info("Database connection established successfully")
        return engine
    except Exception as e:
        logger.error(f"Error connecting to database: {e}")
        raise



def main() -> None:
    """Main function to run the game."""
    try:
        load_config()
        engine = setup_database()
        state = initialize_state()
        state['escenario'] = generate_scenary()
        state.update(get_user_input())

        print("\n ¡Bienvenido a la aventura!")
        final_state = flow_graph().invoke(state)
    except Exception as e:
        logger.error(f"Error during game setup or execution: {e}")
        print("Lo siento, ocurrió un error inesperado. Por favor, intenta de nuevo más tarde.")

if __name__ == "__main__":
    main()
    
    
    
