#imports
from intro_writer.agents_def import AgentState

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
import random
import re
from langchain_openai import ChatOpenAI





PROMPT_MAGO_BLANCO = """
Eres el Mago Blanco, un sabio guardián del bosque mágico. Tu tarea es poner a prueba al héroe {hero_name} con un {challenge_type}.

Si es un acertijo, crea uno simple y apropiado para niños.
Si es una pregunta matemática, crea una pregunta de aritmética simple (suma, resta, multiplicación o división) con números entre 1 y 20.

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
    model = ChatOpenAI(model_name="gpt-4o", temperature=0.5)
    print("\nEl Mago Blanco está preparando un desafío...")
    challenge_type = random.choice(["acertijo", "matemática"])
    
    messages = [
        SystemMessage(content=PROMPT_MAGO_BLANCO.format(hero_name=state['heroe'], challenge_type=challenge_type)),
        HumanMessage(content=f"Crea un {challenge_type} para este héroe.")
    ]
    response = model.invoke(messages)
    
    desafio_match = re.search(r'<desafio>(.*?)</desafio>', response.content, re.DOTALL)
    solucion_match = re.search(r'<solucion>(.*?)</solucion>', response.content, re.DOTALL)
    
    if desafio_match and solucion_match:
        state['desafio'] = desafio_match.group(1).strip()
        state['puzzle_solution'] = solucion_match.group(1).strip().split("Solución:")[-1].strip()

    else:
        print("No se pudo generar un desafío específico. Usando un desafío predeterminado.")
        state['desafio'] = "¿Cuánto es 2 + 2?"
        state['puzzle_solution'] = "4"
    
    print("\nDesafío del Mago Blanco:")
    print(state['desafio'])
    
    state['cantidad_desafios'] = state.get('cantidad_desafios', 0) + 1
    return state