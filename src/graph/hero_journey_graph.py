from typing import Dict, List
from langchain_core.language_models import BaseChatModel
from langgraph.graph import StateGraph, END
from src.graph.nodes.introduction import introduction_node
from src.graph.nodes.middle import middle_node
from src.graph.nodes.climax import climax_node
from src.graph.nodes.conclusion import conclusion_node

class HeroJourneyState(Dict):
    """
    Represents the state of the hero's journey.
    """
    story: str
    current_stage: str
    hero_name: str
    quest: str
    allies: List[str]
    enemies: List[str]
    items: List[str]

def create_hero_journey_graph(llm: BaseChatModel) -> StateGraph:
    """
    Creates the hero's journey graph using LangGraph.
    """
    # Initialize the graph
    workflow = StateGraph(HeroJourneyState)

    # Add nodes
    workflow.add_node("introduction", lambda x: introduction_node(x, llm))
    workflow.add_node("middle", lambda x: middle_node(x, llm))
    workflow.add_node("climax", lambda x: climax_node(x, llm))
    workflow.add_node("conclusion", lambda x: conclusion_node(x, llm))

    # Define edges
    workflow.add_edge("introduction", "middle")
    workflow.add_edge("middle", "climax")
    workflow.add_edge("climax", "conclusion")

    # Set the entrypoint
    workflow.set_entry_point("introduction")

    # Define the exit condition
    def should_end(state: HeroJourneyState) -> bool:
        return state["current_stage"] == "conclusion"

    workflow.add_conditional_edges(
        "conclusion",
        should_end,
        {
            True: END,
            False: "middle"  # Loop back to middle if the journey isn't over
        }
    )

    # Compile the graph
    return workflow.compile()
