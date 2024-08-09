from intro_writer.agents_def import AgentState

from typing import Literal

def should_continue(state: AgentState) -> Literal["continuar", "terminar"]:
    if state['desafios_resueltos'] >= 2:
        print("\n🎉 ¡Felicidades! Has superado los desafíos del Mago Blanco.")
        return "terminar"
    elif state['cantidad_desafios'] < state['max_desafios']:
        print("\n🔄 El Mago Blanco te dará otro desafío.")
        return "continuar"
    else:
        print("\n⏰ Has agotado tus oportunidades con el Mago Blanco.")
        return "terminar"