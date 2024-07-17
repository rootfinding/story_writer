from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-3-opus-20240229")

def generate_options(stage, context):
    prompt = f"""
    Genera 3 opciones únicas y específicas para el héroe en la etapa '{stage}' del Viaje del Héroe.
    Contexto actual: {context}
    
    Cada opción debe:
    1. Ser relevante para la etapa actual del viaje.
    2. Presentar un claro curso de acción o decisión.
    3. Tener potenciales consecuencias interesantes.
    4. Ocasionalmente incluir la obtención de un objeto, un nuevo aliado o un nuevo enemigo.
    
    Formato de respuesta:
    1. [Primera opción]
    2. [Segunda opción]
    3. [Tercera opción]
    """
    response = llm.invoke(prompt)
    return [option.split(". ", 1)[1] for option in response.content.split("\n") if option.strip()]
