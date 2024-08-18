from intro_writer.agents_def import AgentState
from intro_writer.flow_graph import make_graph
from intro_writer.human_interaction import human_response_node
import os
from dotenv import load_dotenv
from langchain.globals import set_debug

print(os.getcwd())

def load_config():
    """Load environment variables and set up configuration."""
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    os.environ["OPENAI_API_KEY"] = openai_api_key
    set_debug(True)

def initialize_state() -> AgentState:
    """Initialize the game state."""
    return AgentState(
        escenario="",
        heroe="Aventurero",
        caramelo="Gominola mágica",
        cantidad_desafios=0,
        max_desafios=5,
        desafio="",
        respuesta="",
        story=[],
        desafios_resueltos=0,
        puzzle_solution="",
        tipo_desafio="",
        evaluacion=""
    )

def print_summary(final_state: AgentState):
    """Print the final game summary."""
    print("\n📜 Resumen final:")
    print(f"Historia: {final_state['story'][0]}")
    print(f"Desafíos enfrentados: {final_state['cantidad_desafios']}")
    print(f"Desafíos resueltos: {final_state['desafios_resueltos']}")
    if final_state['desafios_resueltos'] >= 2:
        print("🎊 El héroe ha superado los desafíos del Mago Blanco y continúa su aventura en el bosque mágico.")
    else:
        print("🔁 El héroe no ha superado todos los desafíos del Mago Blanco y debe buscar otro camino en el bosque.")

def main():
    try:
        load_config()
        state = initialize_state()
        
        print("\n🧙‍♂️ ¡Bienvenido a la aventura en el bosque mágico! 🧙‍♂️")
        graph = make_graph()
        final_state = graph.invoke(state)
        
        print_summary(final_state)
    except Exception as e:
        print(f"Error durante la configuración o ejecución del juego: {e}")
        print("Lo siento, ocurrió un error inesperado. Por favor, intenta de nuevo más tarde.")

if __name__ == "__main__":
    main()