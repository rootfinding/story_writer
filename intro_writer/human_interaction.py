from intro_writer.agents_def import AgentState

from typing import Dict



def human_response_node(state: AgentState) -> AgentState:
    print(f"\nDesafío del Mago Blanco: {state['desafio']}")
    state['respuesta'] = input("¿Cuál es tu respuesta al desafío del Mago Blanco? ")
    print(f"Tu respuesta: {state['respuesta']}")
    return state






from langchain_openai import ChatOpenAI

def fin_node(state: AgentState) -> AgentState:
    """Generate a final summary using OpenAI and print it."""
    chat = ChatOpenAI(model_name="gpt-3.5-turbo")
    
    prompt = f"""
    Genera un resumen final de la aventura del héroe en el bosque mágico. Usa la siguiente información:
    - Historia inicial: {state['story'][0]}
    - Héroe: {state['heroe']}
    - Escenario: {state['escenario']}
    - Desafíos enfrentados: {state['cantidad_desafios']}
    - Desafíos resueltos: {state['desafios_resueltos']}
    - Tipo de desafío: {state['tipo_desafio']}
    - Caramelo favorito: {state['caramelo']}

    El resumen debe ser breve y emocionante, concluyendo la aventura de manera apropiada.
    Personaliza la narración según el escenario específico y los desafíos resueltos.
    Incluye referencias al tipo de desafío (puzzles o matemáticas) y al caramelo favorito del héroe para darle un toque personal.
    """
    
    response = chat.invoke(prompt)
    summary = response.content
    
    print("\n📜 Resumen final de la aventura:")
    print(summary)
    
    if state['desafios_resueltos'] >= 2:
        print(f"\n🎊 ¡Felicidades, {state['heroe']}! Has superado los desafíos del Mago Blanco y demostrado tu valía en el bosque mágico.")
        print(f"Tu ingenio en {state['tipo_desafio']} y tu amor por los {state['caramelo']} te han llevado lejos.")
        print("Tu aventura continúa, ¿qué nuevos misterios te esperan?")
    else:
        print(f"\n🔁 {state['heroe']}, aunque no has superado todos los desafíos del Mago Blanco, tu journey no termina aquí.")
        print(f"Tus habilidades en {state['tipo_desafio']} han mejorado, y tu pasión por los {state['caramelo']} sigue intacta.")
        print("El bosque mágico guarda muchos secretos aún. ¿Qué nuevo camino tomarás?")
    
    return state