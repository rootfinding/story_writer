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
    evaluacion: str