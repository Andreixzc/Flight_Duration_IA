import sqlite3
import pandas as pd
#Script que puxa do banco todos os voos de cada aeronave e salva cada um em um arquivo.

# Caminho para o banco de dados
db_file = 'Database/Flights.db'

# Conecta ao banco de dados
conn = sqlite3.connect(db_file)

# Cria um cursor para executar comandos SQL
cursor = conn.cursor()

# Executa a consulta SQL para selecionar todos os dados da tabela positions, ordenando pelo IdAircraft
query = '''
SELECT * FROM positions
ORDER BY IdAircraft
'''

# Usa pandas para ler o resultado da consulta SQL diretamente para um DataFrame
positions_df = pd.read_sql_query(query, conn)

# Fecha a conexão com o banco de dados
conn.close()

# Salva o DataFrame em arquivos CSV separados por IdAircraft
unique_aircraft_ids = positions_df['IdAircraft'].unique()

for aircraft_id in unique_aircraft_ids:
    aircraft_df = positions_df[positions_df['IdAircraft'] == aircraft_id]
    aircraft_df.to_csv(f'Dataset/PosSorted/{aircraft_id}.csv', index=False)

print("Dados foram salvos em arquivos CSV separados por IdAircraft.")
