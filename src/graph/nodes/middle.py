from typing import Dict
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate

middle_template = """
Continue the hero's journey for {hero_name}, who is on a quest to {quest}.
They are now in the middle of their journey, facing challenges and meeting new allies or enemies.
Their current allies are: {allies}
Their current enemies are: {enemies}
Their current items are: {items}
Write a paragraph (3-4 sentences) describing a new challenge or encounter they face.
"""

middle_prompt = ChatPromptTemplate.from_template(middle_template)

def middle_node(state: Dict, llm: BaseChatModel) -> Dict:
    # Generate the middle part
    middle_content = llm.invoke(middle_prompt.format_messages(
        hero_name=state["hero_name"],
        quest=state["quest"],
        allies=", ".join(state["allies"]),
        enemies=", ".join(state["enemies"]),
        items=", ".join(state["items"])
    )).content

    # Update the state
    state["current_stage"] = "middle"
    state["story"] += f"\n\n{middle_content}"
    
    return state
