import pandas as pd
import random
import os

def generate_scenary():
    try:
        # Construct the correct path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        path = os.path.join(parent_dir, 'scenario_generator', 'output_csv', 'single_tile_descriptions_1.csv')
        df = pd.read_csv(path)
        row_random = random.randint(0, len(df)-1)
        return df["Description"].iloc[row_random]
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")