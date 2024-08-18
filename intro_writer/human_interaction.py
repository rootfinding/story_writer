from intro_writer.agents_def import AgentState

def human_response_node(state: AgentState) -> AgentState:
    print(f"\nDesafío del Mago Blanco: {state['desafio']}")
    state['respuesta'] = input("¿Cuál es tu respuesta al desafío del Mago Blanco? ")
    print(f"Tu respuesta: {state['respuesta']}")
    return state