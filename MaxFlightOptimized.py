import sqlite3
import pandas as pd
from datetime import timedelta
import os

def analyze_flights(db_path):
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Query para obter os dados dos voos
    query = '''
    SELECT dtDeparture, idAircraft, modelAircraft
    FROM flightlist
    ORDER BY idAircraft, dtDeparture
    '''
    
    df = pd.read_sql_query(query, conn, parse_dates=['dtDeparture'])
    
    # Inicializar uma lista vazia para armazenar os resultados
    results = []

    # Processar cada aeronave
    for aircraft_id, aircraft_data in df.groupby('idAircraft'):
        aircraft_data = aircraft_data.sort_values(by='dtDeparture')
        
        max_sequence = 0
        best_start_date = None
        best_end_date = None
        
        start_index = 0
        end_index = 0
        current_flights = 0
        
        # Avaliar todos os períodos de 2 dias usando uma janela deslizante
        while end_index < len(aircraft_data):
            start_date = aircraft_data.iloc[start_index]['dtDeparture']
            end_date = start_date + timedelta(days=2)
            
            # Expandir a janela para a direita
            while end_index < len(aircraft_data) and aircraft_data.iloc[end_index]['dtDeparture'] < end_date:
                current_flights += 1
                end_index += 1
            
            # Atualizar o máximo se necessário
            if current_flights > max_sequence:
                max_sequence = current_flights
                best_start_date = start_date
                best_end_date = end_date
            
            # Mover a janela para a direita
            current_flights -= 1
            start_index += 1

        # Preparar o resultado para esta aeronave
        if max_sequence > 0:
            result = {
                'Period': f"{best_start_date.date()} to {best_end_date.date()}",
                'Aircraft ID': aircraft_id,
                'Model Aircraft': aircraft_data.iloc[0]['modelAircraft'],
                'Number of flights flown': max_sequence
            }
            results.append(result)

    # Converter resultados para DataFrame
    results_df = pd.DataFrame(results)
    
    # Salvar DataFrame em um arquivo CSV
    output_csv_path = 'dataset/longest_flight_sequences.csv'
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    results_df.to_csv(output_csv_path, index=False)
    
    print("Table 'Longest_Flight_Sequences' saved as 'longest_flight_sequences.csv'.")

    # Criar uma nova tabela e inserir resultados
    results_df.to_sql('Longest_Flight_Sequences', conn, if_exists='replace', index=False)
    
    print("Table 'Longest_Flight_Sequences' created successfully.")
    
    # Fechar a conexão
    conn.close()

# Exemplo de uso
db_path = 'Database/Flights.db'
analyze_flights(db_path)
