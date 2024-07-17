# src/utils/character_encounters.py

from ..database.vector_store import store_interaction, retrieve_interactions, summarize_character_memory
from ..models.character import Character
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-3-opus-20240229")

def character_interaction(state, character):
    player_name = state['hero_name']
    current_stage = state['current_stage']
    
    # Recuperar interacciones pasadas relevantes
    past_interactions = retrieve_interactions(character.name, player_name, state['context'])
    
    # Obtener un resumen de la memoria del personaje
    character_memory = summarize_character_memory(character.name, player_name)
    
    prompt = f"""
    El héroe {player_name} se encuentra con {character.name}, un {character.role}.
    Etapa actual del viaje: {current_stage}
    Contexto: {state['context']}
    Debilidad del personaje: {character.weakness}
    Objeto/Información clave: {character.key}
    Disposición actual: {character.get_disposition()}
    
    Resumen de la memoria del personaje sobre el héroe:
    {character_memory}
    
    Interacciones pasadas relevantes:
    {' '.join(past_interactions)}
    
    Genera una breve interacción (3-4 oraciones) entre el héroe y el personaje que:
    1. Refleje la disposición actual del personaje y su memoria sobre el héroe
    2. Proporcione una pista sutil sobre su debilidad o la información clave que posee
    3. Termine con una pregunta o declaración del personaje que el héroe deba responder
    """
    
    interaction = llm.invoke(prompt).content
    
    # Almacenar la nueva interacción
    store_interaction(character.name, player_name, interaction, current_stage)
    
    return interaction

def process_hero_response(state, character, response):
    player_name = state['hero_name']
    current_stage = state['current_stage']
    
    prompt = f"""
    El héroe {player_name} responde a {character.name} con: "{response}"
    Etapa actual: {current_stage}
    Contexto: {state['context']}
    
    Considerando la respuesta del héroe y la historia previa, determina:
    1. Cómo cambia la actitud del personaje (un número entre -20 y +20)
    2. Si el héroe obtiene alguna información o item del personaje
    3. Una breve reacción del personaje (1-2 oraciones)
    
    Formato de respuesta:
    Cambio de actitud: [número]
    Obtención: [información u objeto obtenido, o "Nada"]
    Reacción: [reacción del personaje]
    """
    
    result = llm.invoke(prompt).content
    attitude_change = int(result.split("\n")[0].split(": ")[1])
    obtained = result.split("\n")[1].split(": ")[1]
    reaction = result.split("\n")[2].split(": ")[1]
    
    character.update_attitude(attitude_change)
    if obtained.lower() != "nada":
        state['inventory'].append(obtained)
    
    # Almacenar la respuesta del héroe y la reacción del personaje
    full_interaction = f"Héroe: {response}\n{character.name}: {reaction}"
    store_interaction(character.name, player_name, full_interaction, current_stage)
    
    return reaction, obtained