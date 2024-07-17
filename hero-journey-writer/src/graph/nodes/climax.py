from typing import Dict
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate

climax_template = """
{hero_name} is approaching the climax of their quest to {quest}.
Their allies are: {allies}
Their enemies are: {enemies}
Their items are: {items}
Write a dramatic paragraph (4-5 sentences) describing the ultimate challenge they face.
"""

climax_prompt = ChatPromptTemplate.from_template(climax_template)

def climax_node(state: Dict, llm: BaseChatModel) -> Dict:
    # Generate the climax
    climax_content = llm.invoke(climax_prompt.format_messages(
        hero_name=state["hero_name"],
        quest=state["quest"],
        allies=", ".join(state["allies"]),
        enemies=", ".join(state["enemies"]),
        items=", ".join(state["items"])
    )).content

    # Update the state
    state["current_stage"] = "climax"
    state["story"] += f"\n\n{climax_content}"
    
    return state
