from typing import Dict
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate

conclusion_template = """
Conclude the hero's journey for {hero_name}, who has completed their quest to {quest}.
Their allies were: {allies}
Their enemies were: {enemies}
Their items were: {items}
Write a satisfying conclusion (3-4 sentences) that wraps up the story and reflects on the hero's growth.
"""

conclusion_prompt = ChatPromptTemplate.from_template(conclusion_template)

def conclusion_node(state: Dict, llm: BaseChatModel) -> Dict:
    # Generate the conclusion
    conclusion_content = llm.invoke(conclusion_prompt.format_messages(
        hero_name=state["hero_name"],
        quest=state["quest"],
        allies=", ".join(state["allies"]),
        enemies=", ".join(state["enemies"]),
        items=", ".join(state["items"])
    )).content

    # Update the state
    state["current_stage"] = "conclusion"
    state["story"] += f"\n\n{conclusion_content}"
    
    return state
