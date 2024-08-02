import sqlite3
import pandas as pd
from datetime import datetime
import os

# Gera dataset de treino, puxando os voos segmentados na tabela 'flightList' e salvando na tabela 'trainingFlightTable'.

def get_weekday(date_str):
    date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    return date.weekday() + 1

def get_hour(date_str):
    date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    return date.hour

def calculate_duration(start_time, end_time):
    start = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    end = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    return int((end - start).total_seconds() // 60)

def generate_trainingFlightTable(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Criar tabela trainingFlightTable se não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trainingFlightTable (
            OriginCode TEXT,
            DestinCode TEXT,
            WeekDay INTEGER,
            HourDeparture INTEGER,
            ModelAircraft TEXT,
            Duration INTEGER
        );
    ''')

    # Limpar a tabela existente
    cursor.execute('DELETE FROM trainingFlightTable')

    # Inserir dados na tabela trainingFlightTable
    cursor.execute('''
        INSERT INTO trainingFlightTable (OriginCode, DestinCode, WeekDay, HourDeparture, ModelAircraft, Duration)
        SELECT 
            codeDeparture AS OriginCode,
            codeDestin AS DestinCode,
            strftime('%w', dtDeparture) + 1 AS WeekDay,  -- Ajustar para a saída do strftime do SQLite
            strftime('%H', dtDeparture) AS HourDeparture,
            modelAircraft AS ModelAircraft,
            (strftime('%s', dtArrival) - strftime('%s', dtDeparture)) / 60 AS Duration
        FROM flightList
    ''')
    conn.commit()

    # Exportar a tabela trainingFlightTable para um arquivo CSV
    df = pd.read_sql_query('SELECT * FROM trainingFlightTable', conn)
    
    output_csv_path = 'dataset/trainingFlightTable.csv'
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    df.to_csv(output_csv_path, index=False)
    
    print(f"Table 'trainingFlightTable' saved as 'trainingFlightTable.csv'.")

    # Fechar a conexão
    conn.close()

# Exemplo de uso
db_file = 'Database/Flights.db'
generate_trainingFlightTable(db_file)
