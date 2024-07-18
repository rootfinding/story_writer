from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.journey import JourneyStart
from pydantic import BaseModel
from app.services.wizard_service import generate_initial_challenge, evaluate_wizard_response, start_journey, update_journey

router = APIRouter(prefix="/wizard", tags=["wizard"])

@router.post("/start")
async def start_journey_route(journey: JourneyStart, db: Session = Depends(get_db)):
    user_id = "test_user"  # En una aplicación real, obtendrías esto de la autenticación
    new_journey = start_journey(db, user_id, journey.dict())
    challenge = generate_initial_challenge()
    return {"message": "Journey started", "challenge": challenge}



class EvaluationRequest(BaseModel):
    response: str
    stage: str

@router.post("/evaluate")
async def evaluate_response(request: EvaluationRequest, db: Session = Depends(get_db)):
    user_id = "test_user"  # En una aplicación real, obtendrías esto de la autenticación
    result = evaluate_wizard_response(request.response, request.stage, user_id)
    if not isinstance(result, dict):
        result = {"result": result}  # Convert to dict if necessary
    update_journey(db, user_id, request.stage, result)
    next_challenge = generate_next_challenge(request.stage)
    return {"message": "Response evaluated", "result": result, "next_challenge": next_challenge}

def generate_next_challenge(stage):
    challenges = {
        'start': "You've faced your fear. Now, what's your next step on this journey?",
        'journey': "You've embarked on your journey. What obstacle do you encounter?",
        'challenge': "You've reached the ultimate challenge. How do you overcome it?",
        'return': "You're nearing the end of your journey. What have you learned?"
    }
    return challenges.get(stage, "Your journey continues. What happens next?")