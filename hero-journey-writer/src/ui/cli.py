import time
from typing import Any, Dict
from langgraph.graph import StateGraph

def print_slowly(text: str, delay: float = 0.03):
    """Print text slowly for a more engaging experience."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def get_user_input(prompt: str) -> str:
    """Get input from the user with a formatted prompt."""
    print_slowly(prompt)
    return input("> ").strip()

def initialize_story() -> Dict[str, Any]:
    """Initialize the story state with user input."""
    print_slowly("Welcome to the Hero's Journey Story Writer!")
    print_slowly("Let's begin by creating your hero and their world.")
    
    hero_name = get_user_input("What is your hero's name?")
    quest = get_user_input("What is the main quest or goal of your hero?")
    
    return {
        "story": "",
        "current_stage": "introduction",
        "hero_name": hero_name,
        "quest": quest,
        "allies": [],
        "enemies": [],
        "items": []
    }

def display_story_progress(state: Dict[str, Any]):
    """Display the current state of the story."""
    print_slowly("\nCurrent Story Progress:")
    print_slowly(state["story"])
    print_slowly(f"\nCurrent Stage: {state['current_stage']}")
    print_slowly(f"Hero: {state['hero_name']}")
    print_slowly(f"Quest: {state['quest']}")
    if state['allies']:
        print_slowly(f"Allies: {', '.join(state['allies'])}")
    if state['enemies']:
        print_slowly(f"Enemies: {', '.join(state['enemies'])}")
    if state['items']:
        print_slowly(f"Items: {', '.join(state['items'])}")

def handle_user_interaction(state: Dict[str, Any]) -> Dict[str, Any]:
    """Handle user interaction based on the current stage."""
    if state["current_stage"] == "introduction":
        ally = get_user_input("Name an ally who will join your hero on their journey:")
        state["allies"].append(ally)
    elif state["current_stage"] == "middle":
        enemy = get_user_input("Name an enemy your hero will face:")
        state["enemies"].append(enemy)
        item = get_user_input("Name an item your hero will acquire:")
        state["items"].append(item)
    elif state["current_stage"] == "climax":
        print_slowly("Your hero faces their greatest challenge!")
        choice = get_user_input("Will they (1) face it head-on or (2) find a clever solution?")
        state["climax_choice"] = choice
    elif state["current_stage"] == "conclusion":
        print_slowly("Your hero's journey is coming to an end.")
        print_slowly("Let's review their adventure...")
    
    return state

def start_cli(graph: StateGraph):
    """Start the command-line interface for the story writing process."""
    state = initialize_story()
    
    while state["current_stage"] != "conclusion":
        display_story_progress(state)
        state = handle_user_interaction(state)
        state = graph.invoke(state)
    
    display_story_progress(state)
    print_slowly("Congratulations! You've completed your hero's journey!")

