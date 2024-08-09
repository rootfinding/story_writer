from intro_writer.agents_def import AgentState

from typing import Dict



def human_response_node(state: AgentState) -> AgentState:
    print(f"\nDesafío del Mago Blanco: {state['desafio']}")
    state['respuesta'] = input("¿Cuál es tu respuesta al desafío del Mago Blanco? ")
    print(f"Tu respuesta: {state['respuesta']}")
    return state



def print_summary(final_state: Dict) -> None:
    """Print the final game summary."""
    print("\n📜 Resumen final:")
    print(f"Historia: {final_state['story'][0]}")
    print(f"Desafíos enfrentados: {final_state['cantidad_desafios']}")
    print(f"Desafíos resueltos: {final_state['desafios_resueltos']}")
    if final_state['desafios_resueltos'] >= 2:
        print("🎊 El héroe ha superado los desafíos del Mago Blanco y continúa su aventura en el bosque mágico.")
    else:
        print("🔁 El héroe no ha superado todos los desafíos del Mago Blanco y debe buscar otro camino en el bosque.")


