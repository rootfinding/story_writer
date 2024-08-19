from typing import TypedDict, List

class AgentState(TypedDict):
    escenario: str
    heroe: str
    caramelo: str
    cantidad_desafios: int
    max_desafios: int
    desafio: str
    respuesta: str
    story: List[str]
    desafios_resueltos: int
    puzzle_solution: str
    tipo_desafio: str



from abc import ABC, abstractmethod

class Agente(ABC):
    def __init__(self, nombre):
        self.nombre = nombre

    @abstractmethod
    def actuar(self, estado):
        pass