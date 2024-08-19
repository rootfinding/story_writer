from intro_writer.agents_def import AgentState
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import StructuredTool
from typing import List
from intro_writer.puzzles_pinnecone import buscar_en_pinecone
import re

PROMPT_MAGO_BLANCO = """
Eres el Mago Blanco, un sabio guardián del bosque mágico. Tu tarea es desafiar al héroe {hero_name} con un {challenge_type}.

Usa estas herramientas:
1. Calculadora: para problemas matemáticos.
2. Buscador de Acertijos: para encontrar acertijos.

Si es un desafío matemático, usa la Calculadora y crea un problema divertido.
Si es un acertijo, usa el Buscador de Acertijos con la palabra "acertijo" y adapta uno al contexto del héroe.

Incluye elementos del escenario ({scenario}) y el dulce favorito del héroe ({favorite_candy}) si es posible.

Presenta tu desafío así:
<desafio>
(Escribe el desafío aquí)
</desafio>

<solucion>
(Escribe la respuesta correcta aquí)
</solucion>
"""

def calculadora(a: int, b: int, operacion: str) -> int:
    operaciones = {
        "suma": lambda x, y: x + y,
        "resta": lambda x, y: x - y,
        "multiplicacion": lambda x, y: x * y,
        "division": lambda x, y: x // y
    }
    return operaciones[operacion](a, b)

calculadora_tool = StructuredTool.from_function(
    func=calculadora,
    name="Calculadora",
    description="Realiza operaciones matemáticas básicas"
)

buscador_acertijos_tool = StructuredTool.from_function(
    func=buscar_en_pinecone,
    name="Buscador de Acertijos",
    description="Busca acertijos en la base de datos"
)

def mago_blanco_node(state: AgentState) -> AgentState:
    model = ChatOpenAI(model_name="gpt-4", temperature=0.7)
    print("\nEl Mago Blanco está preparando un desafío...")
    
    messages = [
        SystemMessage(content=PROMPT_MAGO_BLANCO.format(
            hero_name=state['heroe'],
            favorite_candy=state['caramelo'],
            scenario=state['escenario'],
            challenge_type=state['tipo_desafio']
        )),
        HumanMessage(content=f"Crea un {state['tipo_desafio']} divertido para el héroe.")
    ]
    
    response = model.invoke(messages)
    
    desafio_match = re.search(r'<desafio>(.*?)</desafio>', response.content, re.DOTALL)
    solucion_match = re.search(r'<solucion>(.*?)</solucion>', response.content, re.DOTALL)
    
    if desafio_match and solucion_match:
        state['desafio'] = desafio_match.group(1).strip()
        state['puzzle_solution'] = solucion_match.group(1).strip()
    else:
        print("Error al generar el desafío. Usando uno predeterminado.")
        state['desafio'] = "¿Qué es más grande que tú, pero no pesa nada?"
        state['puzzle_solution'] = "Tu sombra"
    
    print("\nDesafío del Mago Blanco:")
    print(state['desafio'])
    
    state['cantidad_desafios'] = state.get('cantidad_desafios', 0) + 1
    return state

def evaluador_desafio(state: AgentState) -> AgentState:
    model = ChatOpenAI(model_name="gpt-4", temperature=0.2)
    
    prompt = f"""
    Evalúa la respuesta del héroe al siguiente desafío:

    Desafío: {state['desafio']}
    Respuesta correcta: {state['puzzle_solution']}
    Respuesta del héroe: {state['respuesta']}

    Determina si la respuesta del héroe es correcta o está cerca de serlo. 
    Ignora mayúsculas/minúsculas y pequeñas diferencias en la redacción.
    Asigna un puntaje de 0 a 100 basado en qué tan cerca estuvo la respuesta.

    Responde en este formato:
    <evaluacion>
    Puntaje: (número del 0 al 100)
    Comentario: (breve explicación de la evaluación)
    </evaluacion>
    """

    response = model.invoke(prompt)
    
    eval_match = re.search(r'<evaluacion>(.*?)</evaluacion>', response.content, re.DOTALL)
    if eval_match:
        evaluacion = eval_match.group(1).strip()
        puntaje_match = re.search(r'Puntaje:\s*(\d+)', evaluacion)
        comentario_match = re.search(r'Comentario:\s*(.*)', evaluacion)
        
        puntaje = int(puntaje_match.group(1)) if puntaje_match else 0
        comentario = comentario_match.group(1) if comentario_match else "Sin comentario."

        print(f"\nEvaluación del Mago Blanco:")
        print(f"Puntaje: {puntaje}/100")
        print(f"Comentario: {comentario}")

        state['puntaje'] = puntaje
        if puntaje >= 80:
            state['desafio_resuelto'] = True
            state['desafios_resueltos'] = state.get('desafios_resueltos', 0) + 1
            print("¡Has superado el desafío del Mago Blanco!")
        else:
            state['desafio_resuelto'] = False
            print("No has superado completamente el desafío.")
            
        respuesta = input("¿Quieres intentar responder de nuevo? (s/n): ").lower()
        state['reintentar'] = respuesta == 's'
    else:
        print("Error en la evaluación. El desafío se considera no resuelto.")
        state['desafio_resuelto'] = False
        state['reintentar'] = False

    return state