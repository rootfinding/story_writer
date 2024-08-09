import pandas as pd
import random

def generate_scenary():
    """
    Genera un escenario medieval aleatorio. 
    """
    #TODO: incoporar el agente que genera el escenario a partir de imagenes de un mapa
    df_scenarios = pd.DataFrame({
        "scenario": ["Un joven noble se encuentra en un bosque mágico", 
                    "Un aventurero se encuentra en una cueva misteriosa", 
                    "Un aprendiz de mago se encuentra en una torre encantada"]
    })
    row_random = random.randint(0, len(df_scenarios)-1)
    return df_scenarios["scenario"].iloc[row_random]