import pandas as pd
from datetime import timedelta

# Função para encontrar a maior sequência de voos em um período de 2 dias para cada aeronave
def find_max_flights_in_2_days(flight_df):
    max_flights = []

    aircraft_ids = flight_df['AircraftId'].unique()
    
    for aircraft_id in aircraft_ids:
        aircraft_flights = flight_df[flight_df['AircraftId'] == aircraft_id]
        
        max_flights_in_2_days = 0
        max_flight_period = None
        model_aircraft = aircraft_flights['AircraftModel'].iloc[0]
        
        for i in range(len(aircraft_flights)):
            start_time = pd.to_datetime(aircraft_flights.iloc[i]['DepartureDateTime'], format='%d/%m/%Y %H:%M:%S')
            end_time = start_time + timedelta(days=2)
            flights_in_period = aircraft_flights[
                (pd.to_datetime(aircraft_flights['DepartureDateTime'], format='%d/%m/%Y %H:%M:%S') >= start_time) &
                (pd.to_datetime(aircraft_flights['DepartureDateTime'], format='%d/%m/%Y %H:%M:%S') < end_time)
            ]
            
            num_flights_in_period = len(flights_in_period)
            if num_flights_in_period > max_flights_in_2_days:
                max_flights_in_2_days = num_flights_in_period
                max_flight_period = (start_time, end_time)
        
        max_flights.append({
            'PeriodStart': max_flight_period[0].strftime('%d/%m/%Y %H:%M:%S'),
            'PeriodEnd': max_flight_period[1].strftime('%d/%m/%Y %H:%M:%S'),
            'AircraftId': aircraft_id,
            'AircraftModel': model_aircraft,
            'NumFlights': max_flights_in_2_days
        })
    
    return pd.DataFrame(max_flights)

# Carregar o arquivo flight_schedule.csv
flight_schedule_df = pd.read_csv('Data/flight_schedule.csv', delimiter=';')

# Encontrar a maior sequência de voos em um período de 2 dias
max_flights_df = find_max_flights_in_2_days(flight_schedule_df)

# Salvar em CSV
max_flights_df.to_csv('Data/max_flights_in_2_days.csv', index=False, sep=';')

print("Listagem da maior sequência de voos dentro de um período de 2 dias gerada com sucesso.")
