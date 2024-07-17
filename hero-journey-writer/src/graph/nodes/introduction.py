from typing import Dict
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate

introduction_template = """
You are a storyteller crafting the introduction to a hero's journey. 
The hero's name is {hero_name} and their quest is to {quest}.
Write a compelling introduction that sets the scene and introduces the hero and their world.
The introduction should be 2-3 sentences long.
"""

introduction_prompt = ChatPromptTemplate.from_template(introduction_template)

def introduction_node(state: Dict, llm: BaseChatModel) -> Dict:
    # Generate the introduction
    introduction = llm.invoke(introduction_prompt.format_messages(
        hero_name=state["hero_name"],
        quest=state["quest"]
    )).content

    # Update the state
    state["current_stage"] = "introduction"
    state["story"] += f"\n\n{introduction}"
    
    return state
