from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from intro_writer.agents_def import AgentState
import random

class Narrador:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4")
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Eres un Narrador místico que describe escenarios fantásticos."),
            ("human", "{input}"),
        ])
        self.agent = create_openai_tools_agent(self.llm, [], self.prompt)
        self.agent_executor = AgentExecutor(agent=self.agent, tools=[], verbose=True)
        self.escenarios = [
            "un bosque misterioso",
            "una caverna oscura",
            "un castillo en ruinas",
            "una montaña nevada"
        ]

    def act(self, state: AgentState) -> AgentState:
        if not state['escenario']:
            state['escenario'] = random.choice(self.escenarios)
            result = self.agent_executor.invoke({"input": f"Describe el escenario: {state['escenario']}"})
            state['story'].append(result['output'])
        return state