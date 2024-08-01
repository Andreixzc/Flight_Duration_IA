import pandas as pd

# Carregar o arquivo flight_schedule.csv
flight_schedule_df = pd.read_csv('Data/flight_schedule.csv', delimiter=';')

# Converter as colunas de data/hora para datetime
flight_schedule_df['DepartureDateTime'] = pd.to_datetime(flight_schedule_df['DepartureDateTime'], format='%d/%m/%Y %H:%M:%S')
flight_schedule_df['ArrivalDateTime'] = pd.to_datetime(flight_schedule_df['ArrivalDateTime'], format='%d/%m/%Y %H:%M:%S')

# Calcular a duração do voo em minutos
flight_schedule_df['FlightDuration'] = (flight_schedule_df['ArrivalDateTime'] - flight_schedule_df['DepartureDateTime']).dt.total_seconds() / 60

# Extrair o dia da semana e a hora de partida
flight_schedule_df['WeekDay'] = flight_schedule_df['DepartureDateTime'].dt.dayofweek + 1  # 1 = Monday, ..., 7 = Sunday
flight_schedule_df['HourDeparture'] = flight_schedule_df['DepartureDateTime'].dt.hour

# Selecionar as colunas relevantes
model_data = flight_schedule_df[[
    'OriginAirportCode', 'DestinationAirportCode', 'WeekDay', 'HourDeparture', 'AircraftModel', 'FlightDuration'
]]

# Renomear as colunas conforme necessário
model_data.columns = ['OriginCode', 'DestinCode', 'WeekDay', 'HourDeparture', 'ModelAircraft', 'FlightDuration']

# Salvar em CSV
model_data.to_csv('Data/flight_duration_model_data.csv', index=False, sep=';')

print("CSV com os dados para treinar o modelo de machine learning gerado com sucesso.")
