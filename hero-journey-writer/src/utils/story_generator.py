from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-3-opus-20240229")

def generate_story_segment(stage, context):
    prompt = f"""
    Genera un breve segmento de historia para la etapa '{stage}' del Viaje del Héroe.
    Contexto actual: {context}
    El segmento debe ser evocativo y establecer el tono para las decisiones que el héroe deberá tomar.
    Limita la respuesta a 3-4 oraciones.
    """
    return llm.invoke(prompt).content
