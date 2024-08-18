from intro_writer.agents_def import AgentState
from typing import Literal

def should_continue(state: AgentState) -> Literal["continuar", "terminar", "final_infeliz"]:
    if state['desafios_resueltos'] >= 2:
        print("\n🎉 ¡Felicidades! Has superado los desafíos del Mago Blanco.")
        return "terminar"
    elif state['cantidad_desafios'] < state['max_desafios']:
        if state['evaluacion'] == 'incorrecto' and state['desafios_resueltos'] == 0:
            print("\n😔 Has fallado dos veces seguidas. El Mago Blanco te mira con decepción.")
            return "final_infeliz"
        print("\n🔄 El Mago Blanco te dará otro desafío.")
        return "continuar"
    else:
        print("\n⏰ Has agotado tus oportunidades con el Mago Blanco.")
        return "terminar"