from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from intro_writer.agents_def import AgentState
from openai import OpenAI
from dotenv import load_dotenv
import os
import platform
import subprocess
from intro_writer.text_to_speech import generate_speech, play_speech
load_dotenv()

GENERADOR_INTRO_PROMPT = """
Eres un narrador creativo. Crea una introducción cautivadora para una historia que incorpore:
1. Nombre del héroe: {hero_name}
2. Dulce favorito del héroe: {favorite_candy}
3. Escenario aleatorio: {random_scenario}

Tu introducción debe tener 3-5 oraciones, presentar al héroe, incorporar el dulce y establecer el escenario. 
Usa un lenguaje sencillo y amigable, apropiado para niños. Puedes usar emojis para hacer la historia más divertida.
"""


def intro_node(state: AgentState) -> AgentState:
    model = ChatOpenAI(model_name="gpt-4", temperature=0.5)
    formatted_prompt = GENERADOR_INTRO_PROMPT.format(
        hero_name=state['heroe'],
        favorite_candy=state['caramelo'],
        random_scenario=state['escenario']
    )
    
    messages = [
        SystemMessage(content=formatted_prompt),
        HumanMessage(content="Genera la introducción de la historia.")
    ]
    response = model.invoke(messages)
    state['story'].append(response.content)
    
    print("\nHistoria generada:")
    print(state['story'][0])
    
    # Generar y reproducir el audio
    output_file = generate_speech(response.content)
    play_speech(output_file)
    
    return state


