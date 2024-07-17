from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-3-opus-20240229")

def generate_dynamic_event(state):
    prompt = f"""
    Basándote en el estado actual del juego, genera un evento dinámico e inesperado.
    
    Héroe: {state['hero_name']}
    Etapa actual: {state['current_stage']}
    Contexto: {state['context']}
    Inventario: {', '.join(state['inventory'])}
    Aliados: {', '.join(state['allies'])}
    Enemigos: {', '.join(state['enemies'])}
    
    Crea un evento que:
    1. Sea relevante para la etapa actual del viaje del héroe
    2. Incorpore elementos del inventario, aliados o enemigos del héroe
    3. Presente un desafío o dilema inesperado
    4. Ofrezca al menos dos opciones de cómo el héroe puede responder
    
    Formato:
    Evento: [Descripción del evento en 2-3 oraciones]
    Opción 1: [Primera opción de respuesta]
    Opción 2: [Segunda opción de respuesta]
    """
    
    response = llm.invoke(prompt).content
    event, *options = response.split("\n")
    return event.split(": ")[1], [opt.split(": ")[1] for opt in options]

def process_event_choice(state, event, choice):
    prompt = f"""
    El héroe {state['hero_name']} ha elegido: "{choice}" en respuesta al evento:
    {event}
    
    Contexto actual: {state['context']}
    
    Determina las consecuencias de esta elección:
    1. Cómo afecta al estado actual del héroe
    2. Qué cambios ocurren en el inventario, aliados o enemigos
    3. Cómo influye en la dirección general de la historia
    
    Proporciona un breve resumen de las consecuencias en 2-3 oraciones.
    """
    
    consequences = llm.invoke(prompt).content
    
    # Actualizar el estado del juego basado en las consecuencias
    # (Esto es un placeholder, deberías implementar la lógica real aquí)
    state['context'] += f" {consequences}"
    
    return consequences
