from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent
from langchain.prompts import StringPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from typing import List
import pinecone

class CalculatorInput(BaseModel):
    expression: str = Field(description="Expresión matemática a calcular")

def calculator_tool(expression: str) -> str:
    try:
        return str(eval(expression))
    except:
        return "Error en la expresión matemática"

def pinecone_query(query: str) -> str:
    index = pinecone.Index("acertijos")
    results = index.query(vector=model.encode(query).tolist(), top_k=1, include_metadata=True)
    if results.matches:
        return results.matches[0].metadata['answer']
    return "No se encontró una respuesta adecuada."

tools = [
    Tool(
        name="Calculadora",
        func=calculator_tool,
        description="Útil para realizar cálculos matemáticos simples"
    ),
    Tool(
        name="Acertijos",
        func=pinecone_query,
        description="Útil para buscar respuestas a acertijos"
    )
]

class MagoBlancoPrintTemplate(StringPromptTemplate):
    template: str
    tools: List[Tool]

    def format(self, **kwargs) -> str:
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        kwargs["agent_scratchpad"] = thoughts
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        return self.template.format(**kwargs)

prompt = MagoBlancoPrintTemplate(
    template="Eres el Mago Blanco, un sabio guardián del bosque mágico. Tu tarea es poner a prueba al héroe con desafíos y acertijos.\n\nHerramientas disponibles:\n{tools}\n\nObjetivo: {input}\n\n{agent_scratchpad}",
    tools=tools,
)

llm = ChatOpenAI(temperature=0)
llm_chain = LLMChain(llm=llm, prompt=prompt)
tool_names = [tool.name for tool in tools]
agent = LLMSingleActionAgent(
    llm_chain=llm_chain,
    output_parser=output_parser,
    stop=["\nObservation:"],
    allowed_tools=tool_names
)

agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)

def mago_blanco_node(state):
    result = agent_executor.run(input=state['input'])
    return {"output": result}