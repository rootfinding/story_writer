from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END

class HeroJourneyState(TypedDict):
    current_stage: str
    context: str
    hero_name: str
    character_insights: list
    inventory: list
    allies: list
    enemies: list
    story_so_far: list

def create_hero_journey_graph():
    workflow = StateGraph(HeroJourneyState)
    
    stages = [
        "call_to_adventure", "refusal_of_call", "supernatural_aid",
        "crossing_threshold", "belly_of_whale", "road_of_trials",
        "meeting_goddess", "temptation", "atonement", "apotheosis",
        "ultimate_boon", "refusal_return", "magic_flight", "rescue",
        "threshold_return", "master_two_worlds", "freedom_to_live"
    ]
    
    for stage in stages:
        workflow.add_node(stage, lambda x, s=stage: {**x, "current_stage": s})
    
    for i in range(len(stages) - 1):
        workflow.add_edge(stages[i], stages[i+1])
    
    workflow.set_entry_point(stages[0])
    workflow.add_edge(stages[-1], END)
    
    return workflow.compile()
