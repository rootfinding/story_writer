# src/characters/wizard.py
from langchain_anthropic import ChatAnthropic
from src.database.vector_store import store_interaction, retrieve_interactions

class Wizard:
    def __init__(self):
        self.llm = ChatAnthropic(model="claude-3-opus-20240229")
    
    def generate_riddle(self):
        prompt = "Generate a challenging riddle related to a hero's journey."
        return self.llm.invoke(prompt).content
    
    def generate_moral_dilemma(self):
        prompt = "Create a moral dilemma that a hero might face on their journey."
        return self.llm.invoke(prompt).content
    
    def evaluate_response(self, player_name, response, context):
        prompt = f"Evaluate the following response to a riddle or moral dilemma: {response}"
        evaluation = self.llm.invoke(prompt).content
        store_interaction(player_name, "wizard", response, context)
        return evaluation
    
    def recall_player_history(self, player_name):
        return retrieve_interactions("wizard", player_name, "player history")

# Usage example
wizard = Wizard()
riddle = wizard.generate_riddle()
print(riddle)
player_response = input("Your answer: ")
evaluation = wizard.evaluate_response("Player1", player_response, "initial_encounter")
print(evaluation)