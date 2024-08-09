from intro_writer.agents_def import AgentState






def puzzle_evaluator_node(state: AgentState) -> AgentState:
    puzzle_solution = state.get('puzzle_solution', 'N/A').lower()
    user_response = state['respuesta'].lower()

    # Comprobación directa para preguntas matemáticas
    if puzzle_solution.isdigit() and user_response.isdigit():
        is_correct = int(puzzle_solution) == int(user_response)
    else:
        # Para acertijos, usamos una comparación más flexible
        is_correct = any(word in puzzle_solution for word in user_response.split())

    if is_correct:
        explanation = f"¡Correcto! La respuesta '{state['respuesta']}' es acertada."
        state['desafio_resuelto'] = True
        state['desafios_resueltos'] = state.get('desafios_resueltos', 0) + 1
    else:
        explanation = f"Lo siento, la respuesta no es correcta. La solución era: {puzzle_solution}"
        state['desafio_resuelto'] = False

    print(f"\nEl Mago Blanco dice: {explanation}")
    return state