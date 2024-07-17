# src/utils/decision_evaluator.py

from langchain_anthropic import ChatAnthropic
from database.vector_store import retrieve_interactions

llm = ChatAnthropic(model="claude-3-opus-20240229")

def evaluate_decision(state, decision):
    player_name = state['hero_name']
    current_stage = state['current_stage']
    
    # Recuperar interacciones relevantes
    relevant_interactions = []
    for character in state['encountered_characters']:
        interactions = retrieve_interactions(character.name, player_name, state['context'], top_k=1)
        relevant_interactions.extend(interactions)
    
    prompt = f"""
    Evalúa la siguiente decisión del héroe {player_name}: '{decision}'.
    
    Etapa actual: {current_stage}
    Contexto: {state['context']}
    Inventario: {', '.join(state['inventory'])}
    Aliados: {', '.join(state['allies'])}
    Enemigos: {', '.join(state['enemies'])}
    
    Interacciones recientes relevantes:
    {' '.join(relevant_interactions)}
    
    Historial de insights previos:
    {' '.join(state['character_insights'][-5:])}  # Últimos 5 insights
    
    Proporciona un análisis (3-4 oraciones) que:
    1. Identifique el rasgo principal demostrado (valentía, cobardía, astucia, compasión, etc.).
    2. Explique cómo esta decisión se alinea o contrasta con decisiones anteriores.
    3. Sugiera cómo esta elección podría influir en futuras interacciones o eventos.
    4. Evalúe si esta decisión acerca al héroe a su objetivo final o lo desvía.
    
    Comienza tu respuesta con el rasgo principal identificado en mayúsculas.
    """
    
    return llm.invoke(prompt).content