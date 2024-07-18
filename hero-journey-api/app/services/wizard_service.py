import os
from dotenv import load_dotenv


load_dotenv()

def generate_initial_challenge():
    return "What is your greatest fear?"



def start_journey(db, user_id: str, journey_data: dict):
    # Implementa la lógica para iniciar el viaje aquí
    return {"user_id": user_id, "journey_started": True}

def update_journey(db, user_id: str, stage: str, data: dict):
    from app.models.journey import Journey  # Ensure this import is correct
    journey = db.query(Journey).filter_by(user_id=user_id).first()
    if journey:
        journey.stage = stage
        result = data.get('result', None)  # Define result from data
        journey.result = result
        db.commit()
    else:
        raise ValueError("Journey not found for user_id: {}".format(user_id))
    
    if stage == 'start':
        journey.start_data = data
    elif stage == 'journey':
        journey.journey_data = data
    elif stage == 'challenge':
        journey.challenge_data = data
    elif stage == 'return':
        journey.return_data = data
    else:
        raise ValueError("Invalid stage: {}".format(stage))
    
    db.commit()
    return journey

def evaluate_wizard_response(response: str, stage: str, user_id: str):
    from langchain_anthropic import ChatAnthropic
    api_key = os.getenv("ANTHROPIC_API_KEY")
    llm = ChatAnthropic(model="claude-3-opus-20240229", api_key=api_key)
    prompt = f"Evaluate the following response to a riddle or moral dilemma: {response}"
    evaluation = llm.invoke(prompt).content
    return evaluation