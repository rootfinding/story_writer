from langgraph.graph import StateGraph
from intro_writer.agents_def import AgentState
from intro_writer.intro_gen import intro_node
from intro_writer.human_interaction import human_response_node,fin_node
from typing import Literal
from intro_writer.mago_blanco import mago_blanco_node,evaluador_desafio
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.base import RunnableSequence
from langgraph.graph import StateGraph, END

def preguntar_tipo_desafio(state: AgentState) -> AgentState:
    print("\n¿Qué tipo de desafío prefieres?")
    print("1. Puzzles")
    print("2. Matemáticas")
    respuesta = input("Elige 1 o 2: ")
    state['tipo_desafio'] = 'puzzles' if respuesta == '1' else 'matematicas'
    return state


def router_continuar(state):
    if state["cantidad_desafios"] >= state["max_desafios"]:
        return "final"
    elif state.get("reintentar", False):
        return "respuesta_humano"
    else:
        return "mago_blanco"
        
def flow_graph():
    builder = StateGraph(AgentState)

    # Agregar nodos
    builder.add_node("presentacion_historia", intro_node)
    builder.add_node("preguntar_tipo_desafio", preguntar_tipo_desafio)
    builder.add_node("mago_blanco", mago_blanco_node)
    builder.add_node("respuesta_humano", human_response_node)
    builder.add_node("evaluador_desafio", evaluador_desafio)
    builder.add_node("final", fin_node)

    # Definir bordes
    builder.add_edge("presentacion_historia", "preguntar_tipo_desafio")
    builder.add_edge("preguntar_tipo_desafio", "mago_blanco")
    builder.add_edge("mago_blanco", "respuesta_humano")
    builder.add_edge("respuesta_humano", "evaluador_desafio")
    
    # Agregar borde condicional para continuar o terminar
    builder.add_conditional_edges(
    "evaluador_desafio",
    router_continuar,
    {
        "mago_blanco": "mago_blanco",
        "respuesta_humano": "respuesta_humano",
        "final": "final"
    }
)   
    builder.add_edge("final", END)
    
    
    # Establecer el punto de entrada
    builder.set_entry_point("presentacion_historia")

    # Compilar el grafo
    return builder.compile()