from intro_writer.agents_def import AgentState
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
import random
import re

PROMPT_MAGO_BLANCO = """
Eres el Mago Blanco, un sabio guardián del bosque mágico. Tu tarea es poner a prueba al héroe {hero_name} con un {challenge_type}.

Si es un acertijo, crea uno simple y apropiado para niños.
Si es una pregunta matemática, crea una pregunta de aritmética divertida y contextualizada. Usa sumas, restas, multiplicaciones o divisiones simples con números entre 1 y 20. 
Contextualiza la pregunta en situaciones mágicas o de aventura.

Ejemplos de preguntas matemáticas divertidas:
1. "Si un dragón tiene 3 cabezas y cada cabeza tiene 5 dientes, ¿cuántos dientes tiene el dragón en total?"
2. "Un mago tiene 15 pociones y usa 2 en cada hechizo. ¿Cuántos hechizos completos puede lanzar?"
3. "Hay 4 torres en el castillo y cada torre tiene 3 pisos. ¿Cuántos pisos hay en total en el castillo?"

Presenta tu desafío en este formato exacto:
<desafio>
(Escribe aquí el desafío)
</desafio>

<solucion>
Solución: (Escribe aquí la respuesta correcta)
</solucion>

Asegúrate de incluir tanto la etiqueta de desafío como la de solución.
"""

def mago_blanco_node(state: AgentState) -> AgentState:
    model = ChatOpenAI(model_name="gpt-4", temperature=0.7)  # Aumentamos la temperatura para más variedad
    print("\nEl Mago Blanco está preparando un desafío...")
    challenge_type = random.choice(["acertijo", "matemática"])
    
    messages = [
        SystemMessage(content=PROMPT_MAGO_BLANCO.format(hero_name=state['heroe'], challenge_type=challenge_type)),
        HumanMessage(content=f"Crea un {challenge_type} divertido y único para este héroe.")
    ]
    response = model.invoke(messages)
    
    desafio_match = re.search(r'<desafio>(.*?)</desafio>', response.content, re.DOTALL)
    solucion_match = re.search(r'<solucion>(.*?)</solucion>', response.content, re.DOTALL)
    
    if desafio_match and solucion_match:
        state['desafio'] = desafio_match.group(1).strip()
        state['puzzle_solution'] = solucion_match.group(1).strip().split("Solución:")[-1].strip()
    else:
        print("No se pudo generar un desafío específico. Usando un desafío predeterminado.")
        state['desafio'] = "Si tienes 10 manzanas mágicas y regalas 3 a un elfo, ¿cuántas te quedan?"
        state['puzzle_solution'] = "7"
    
    print("\nDesafío del Mago Blanco:")
    print(state['desafio'])
    
    state['cantidad_desafios'] = state.get('cantidad_desafios', 0) + 1
    return state