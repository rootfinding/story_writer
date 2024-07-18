''' QUiero un resumen de todo mi codigo para enteder el workflow completo'''

def resumen_funciones():
    resumen = """
    1. initialize_game_state: Inicializa el estado del juego con el nombre del héroe, contexto inicial, etapa actual, y listas vacías para insights de personajes, inventario, aliados, enemigos y la historia hasta el momento.
    
    2. main_game_loop: Controla el flujo principal del juego. Crea el grafo del viaje del héroe, inicializa el estado del juego, y maneja el bucle principal donde se generan segmentos de historia, eventos dinámicos o encuentros con personajes, y se procesan las decisiones del jugador.
    
    3. handle_dynamic_event: Genera y maneja eventos dinámicos inesperados. Presenta opciones al jugador y procesa las consecuencias de su elección, actualizando la historia del juego.
    
    4. handle_character_encounter: Genera y maneja encuentros con personajes. Presenta la interacción con el personaje, procesa la respuesta del héroe y actualiza el inventario y la historia del juego según la reacción del personaje.
    
    5. evaluate_decision: Evalúa las decisiones del jugador utilizando un modelo de lenguaje (ChatAnthropic). Recupera interacciones relevantes de la base de datos y genera un análisis de la decisión del héroe, identificando rasgos principales, alineación con decisiones anteriores, influencia en futuras interacciones y si acerca al héroe a su objetivo final.
    """
    print(resumen)
