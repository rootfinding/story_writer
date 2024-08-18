from langchain.tools import BaseTool
import random

class CalculatorTool(BaseTool):
    name = "Calculator"
    description = "Useful for when you need to perform mathematical calculations"

    def _run(self, query: str) -> str:
        try:
            return str(eval(query))
        except:
            return "Error: Invalid mathematical expression"

    async def _arun(self, query: str) -> str:
        return self._run(query)

class PuzzleGeneratorTool(BaseTool):
    name = "PuzzleGenerator"
    description = "Generates a random puzzle or riddle"

    def _run(self, query: str) -> str:
        puzzles = [
            ("¿Qué tiene llaves pero ninguna cerradura, espacio pero ninguna habitación, puedes entrar pero no puedes salir?", "teclado"),
            ("¿Qué sube y baja pero nunca se mueve?", "la temperatura"),
            ("¿Qué es lo que puedes ver con los ojos cerrados?", "sueños"),
        ]
        puzzle, answer = random.choice(puzzles)
        return f"Puzzle: {puzzle}\nAnswer: {answer}"

    async def _arun(self, query: str) -> str:
        return self._run(query)