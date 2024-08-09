import pandas as pd
import random

def generate_scenary():
    try:
        df = pd.read_csv('scenario_generator/single_tile_descriptions_alt_01.csv')
        row_random = random.randint(0, len(df)-1)
        return df["description"].iloc[row_random]
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")
        return "Un aventurero se encuentra en un bosque misterioso"  # Escenario por defecto en caso de error