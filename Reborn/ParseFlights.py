import pandas as pd
from geopy.distance import great_circle

# Função para ler o CSV removendo o BOM e com delimitador correto
def read_csv_without_bom(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        return pd.read_csv(file, delimiter=';')

# Função para encontrar o aeroporto mais próximo
def find_nearest_airport(lat, lon, airports_df):
    airports_df['Distance'] = airports_df.apply(
        lambda row: great_circle((lat, lon), (row['Latitude'], row['Longitude'])).kilometers, axis=1
    )
    nearest_airport = airports_df.loc[airports_df['Distance'].idxmin()]
    return nearest_airport

# Carregar os dados com o delimitador correto e remover o BOM
positions_df = read_csv_without_bom('Data/positions.csv')
airports_df = read_csv_without_bom('Data/airports.csv')

# Garantir que os nomes das colunas estejam corretos e sem espaços extras
positions_df.columns = positions_df.columns.str.strip().str.replace(' ', '')
airports_df.columns = airports_df.columns.str.strip().str.replace(' ', '')

# Converter a coluna 'Time' para datetime
positions_df['Time'] = pd.to_datetime(positions_df['Time'], format='%Y-%m-%d %H:%M:%S.%f')

# Ordenar os dados
positions_df = positions_df.sort_values(by=['idAircraft', 'Time'])

# Identificar voos
def identify_flights(df):
    flights = []
    current_flight = None

    for i in range(len(df)):
        row = df.iloc[i]

        if current_flight is None:
            # Iniciar um novo voo
            current_flight = {
                'IdAircraft': row['idAircraft'],
                'StartTime': row['Time'],
                'StartLat': row['latitude'],
                'StartLon': row['Longitude']
            }
        elif row['idAircraft'] == current_flight['IdAircraft']:
            # Verificar se há uma pausa longa (> X minutos) para finalizar o voo anterior
            if i > 0 and (row['Time'] - df.iloc[i-1]['Time']).total_seconds() / 60 > 60:  # Exemplo: pausa maior que 60 minutos
                # Finalizar o voo atual e iniciar um novo
                current_flight['EndTime'] = df.iloc[i-1]['Time']
                current_flight['EndLat'] = df.iloc[i-1]['latitude']
                current_flight['EndLon'] = df.iloc[i-1]['Longitude']
                flights.append(current_flight)
                current_flight = {
                    'IdAircraft': row['idAircraft'],
                    'StartTime': row['Time'],
                    'StartLat': row['latitude'],
                    'StartLon': row['Longitude']
                }
        else:
            # Finalizar o voo se o avião mudar
            current_flight['EndTime'] = df.iloc[i-1]['Time']
            current_flight['EndLat'] = df.iloc[i-1]['latitude']
            current_flight['EndLon'] = df.iloc[i-1]['Longitude']
            flights.append(current_flight)
            current_flight = {
                'IdAircraft': row['idAircraft'],
                'StartTime': row['Time'],
                'StartLat': row['latitude'],
                'StartLon': row['Longitude']
            }
    
    # Adicionar o último voo
    if current_flight is not None:
        current_flight['EndTime'] = df.iloc[-1]['Time']
        current_flight['EndLat'] = df.iloc[-1]['latitude']
        current_flight['EndLon'] = df.iloc[-1]['Longitude']
        flights.append(current_flight)
    
    return flights

flights = identify_flights(positions_df)

# Obter informações dos aeroportos
flight_info = []
for flight in flights:
    start_airport = find_nearest_airport(flight['StartLat'], flight['StartLon'], airports_df)
    end_airport = find_nearest_airport(flight['EndLat'], flight['EndLon'], airports_df)
    
    flight_info.append({
        'DepartureDateTime': flight['StartTime'].strftime('%d/%m/%Y %H:%M:%S'),
        'OriginAirportCode': start_airport['Code'],
        'OriginAirportName': start_airport['Name'],
        'OriginAirportCity': start_airport['City'],
        'ArrivalDateTime': flight['EndTime'].strftime('%d/%m/%Y %H:%M:%S'),
        'DestinationAirportCode': end_airport['Code'],
        'DestinationAirportName': end_airport['Name'],
        'DestinationAirportCity': end_airport['City'],
        'AircraftId': flight['IdAircraft'],
        'AircraftModel': positions_df.loc[positions_df['idAircraft'] == flight['IdAircraft'], 'ModelAircraft'].iloc[0]
    })

# Converter para DataFrame e ordenar
flight_df = pd.DataFrame(flight_info)
flight_df = flight_df.sort_values(by='DepartureDateTime')

# Salvar em CSV
flight_df.to_csv('Data/flight_schedule.csv', index=False, sep=';')

print("Lista de partidas e chegadas de voos gerada com sucesso.")
