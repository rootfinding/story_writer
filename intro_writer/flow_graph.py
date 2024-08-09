# Creación del grafo
from langgraph.graph import StateGraph
from intro_writer.agents_def import AgentState
from intro_writer.intro_gen import intro_node
from intro_writer.mago_blanco import mago_blanco_node
from intro_writer.human_interaction import human_response_node
from intro_writer.evaluator import puzzle_evaluator_node



def flow_graph():

    builder = StateGraph(AgentState)

    # Agregar nodos
    builder.add_node("presentacion_historia", intro_node)
    builder.add_node("mago_blanco", mago_blanco_node)
    builder.add_node("respuesta_humano", human_response_node)
    builder.add_node("evaluador_desafio", puzzle_evaluator_node)

    # Definir bordes
    builder.add_edge("presentacion_historia", "mago_blanco")
    builder.add_edge("mago_blanco", "respuesta_humano")
    builder.add_edge("respuesta_humano", "evaluador_desafio")
    # Establecer el punto de entrada
    builder.set_entry_point("presentacion_historia")

    # Compilar el grafo
    return builder.compile()