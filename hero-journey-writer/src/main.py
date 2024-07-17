import random
from dotenv import load_dotenv
from .graph.hero_journey_graph import create_hero_journey_graph, HeroJourneyState
from .utils.option_generator import generate_options
from .utils.decision_evaluator import evaluate_decision
from .utils.character_encounters import character_interaction, process_hero_response
from .utils.dynamic_events import generate_dynamic_event, process_event_choice
from .utils.story_generator import generate_story_segment
from .models.character import Character
from .database.vector_store import initialize_vector_store

load_dotenv()

def initialize_game_state() -> HeroJourneyState:
    return {
        "hero_name": input("Ingresa el nombre de tu héroe: "),
        "context": "El héroe comienza su viaje en un pequeño pueblo rodeado de montañas misteriosas.",
        "current_stage": "call_to_adventure",
        "character_insights": [],
        "inventory": [],
        "allies": [],
        "enemies": [],
        "story_so_far": []
    }

def main_game_loop():
    graph = create_hero_journey_graph()
    state = initialize_game_state()
    
    print(f"Bienvenido al viaje de {state['hero_name']}!")
    
    while state['current_stage'] != "freedom_to_live":
        state = graph.invoke(state)
        print(f"\n--- Etapa actual: {state['current_stage'].replace('_', ' ').title()} ---")
        
        story_segment = generate_story_segment(state['current_stage'], state['context'])
        print(story_segment)
        
        if random.choice([True, False]):
            handle_dynamic_event(state)
        else:
            handle_character_encounter(state)
        
        handle_player_choice(state)
        
        display_character_insights(state)
        update_context(state)
    
    print("\n¡El viaje del héroe ha concluido!")
    print_final_story(state)

def handle_dynamic_event(state):
    event, event_options = generate_dynamic_event(state)
    print(f"\nEvento inesperado: {event}")
    for i, option in enumerate(event_options, 1):
        print(f"{i}. {option}")
    choice = int(input("\nElige una opción (número): ")) - 1
    consequences = process_event_choice(state, event, event_options[choice])
    print(f"\nConsecuencias: {consequences}")
    state['story_so_far'].append(f"Evento: {event} - Elección: {event_options[choice]}")

def handle_character_encounter(state):
    character = random.choice([
        Character("El Sabio", "mentor", "demasiado críptico", "conocimiento antiguo"),
        Character("La Guerrera", "aliado", "impulsividad", "espada legendaria"),
        Character("El Mercader", "neutral", "codicia", "mapa del tesoro"),
        Character("El Hechicero Oscuro", "enemigo", "arrogancia", "grimorio prohibido")
    ])
    interaction = character_interaction(state, character)
    print(f"\nEncuentro con {character.name}:")
    print(interaction)
    response = input("\nTu respuesta: ")
    reaction, obtained = process_hero_response(state, character, response)
    print(f"\nReacción de {character.name}: {reaction}")
    if obtained != "Nada":
        print(f"Has obtenido: {obtained}")
        state['inventory'].append(obtained)
    state['story_so_far'].append(f"Encuentro con {character.name}")

def handle_player_choice(state):
    options = generate_options(state['current_stage'], state['context'])
    print("\nOpciones para continuar:")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    
    choice = int(input("\nElige una opción (número): ")) - 1
    chosen_option = options[choice]
    evaluation = evaluate_decision(state, chosen_option)
    state['character_insights'].append(evaluation)
    
    process_choice_consequences(state, chosen_option)
    state['story_so_far'].append(chosen_option)

def process_choice_consequences(state, choice):
    lower_choice = choice.lower()
    if "obtiene" in lower_choice:
        item = choice.split("obtiene")[-1].strip()
        state['inventory'].append(item)
        print(f"\n{state['hero_name']} ha obtenido: {item}")
    elif "aliado" in lower_choice:
        ally = choice.split("aliado")[-1].strip()
        state['allies'].append(ally)
        print(f"\n{ally} se ha unido a tu aventura como aliado!")
    elif "enemigo" in lower_choice:
        enemy = choice.split("enemigo")[-1].strip()
        state['enemies'].append(enemy)
        print(f"\n{enemy} se ha convertido en tu enemigo!")

def display_character_insights(state):
    print("\nInsights del personaje:")
    for insight in state['character_insights'][-3:]:
        print(f"- {insight}")

def update_context(state):
    new_context = f"{state['hero_name']} está en la etapa de {state['current_stage'].replace('_', ' ')}. "
    if state['inventory']:
        new_context += f"Tiene en su inventario: {', '.join(state['inventory'])}. "
    if state['allies']:
        new_context += f"Sus aliados son: {', '.join(state['allies'])}. "
    if state['enemies']:
        new_context += f"Sus enemigos son: {', '.join(state['enemies'])}. "
    state['context'] = new_context

def print_final_story(state):
    print("\nResumen del viaje de", state['hero_name'])
    print("===================================")
    for i, event in enumerate(state['story_so_far'], 1):
        print(f"{i}. {event}")
    print("\nInventario final:", ', '.join(state['inventory']))
    print("Aliados finales:", ', '.join(state['allies']))
    print("Enemigos finales:", ', '.join(state['enemies']))
    print("\nÚltimos insights del personaje:")
    for insight in state['character_insights'][-5:]:
        print(f"- {insight}")

if __name__ == "__main__":
    main_game_loop()
