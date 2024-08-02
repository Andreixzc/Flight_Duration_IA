import sqlite3
import pandas as pd
#Script que puxa do banco todos os voos de cada aeronave e salva cada um em um arquivo.


db_file = 'Database/Flights.db'

conn = sqlite3.connect(db_file)

cursor = conn.cursor()

# Executa a consulta SQL para selecionar todos os dados da tabela positions, ordenando pelo IdAircraft
query = '''
SELECT * FROM positions
ORDER BY IdAircraft
'''

positions_df = pd.read_sql_query(query, conn)

conn.close()

#DataFrame em arquivos CSV separados por IdAircraft
unique_aircraft_ids = positions_df['IdAircraft'].unique()

for aircraft_id in unique_aircraft_ids:
    aircraft_df = positions_df[positions_df['IdAircraft'] == aircraft_id]
    aircraft_df.to_csv(f'Dataset/PosSorted/{aircraft_id}.csv', index=False)

print("Dados foram salvos em arquivos CSV separados por IdAircraft.")
