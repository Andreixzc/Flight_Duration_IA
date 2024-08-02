import pandas as pd
import sys

def trim_csv_values(file_path):
    # Carregar o CSV em um DataFrame
    df = pd.read_csv(file_path)
    
    # Aplicar o trim em todas as células do DataFrame
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    
    # Salvar o DataFrame modificado de volta no mesmo arquivo CSV
    df.to_csv(file_path, index=False)
    print(f"Trim aplicado e dados salvos em '{file_path}'.")

if __name__ == "__main__":
    trim_csv_values('Dataset/trainingFlightTable.csv')
