from langgraph.graph import StateGraph
from intro_writer.agents_def import AgentState
from intro_writer.narrador import Narrador
from intro_writer.mago_blanco import MagoBlanco
from intro_writer.human_interaction import human_response_node
from intro_writer.evaluator import puzzle_evaluator_node
from intro_writer.conditional_edge import should_continue

def make_graph():
    builder = StateGraph(AgentState)

    # Agregar nodos
    builder.add_node("Narrador", Narrador().act)
    builder.add_node("MagoBlanco", MagoBlanco().act)
    builder.add_node("HumanInteraction", human_response_node)
    builder.add_node("Evaluador", puzzle_evaluator_node)

    # Definir bordes
    builder.add_edge("Narrador", "MagoBlanco")
    builder.add_edge("MagoBlanco", "HumanInteraction")
    builder.add_edge("HumanInteraction", "Evaluador")
    
    builder.add_conditional_edges(
        "Evaluador",
        should_continue,
        {
            "continuar": "MagoBlanco",
            "terminar": "END",
            "final_infeliz": "END"
        }
    )

    # Establecer el punto de entrada
    builder.set_entry_point("Narrador")

    # Compilar el grafo
    return builder.compile()