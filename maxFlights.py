import sqlite3
import pandas as pd
from datetime import timedelta

#Query que extrai os voos máximos por aeronave no periodo de 2 dias e salva na tabela 'Longest_Flight_Sequences'.

def analyze_flights(db_path):
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Query to get the flight data
    query = '''
    SELECT dtDeparture, idAircraft, modelAircraft
    FROM flightlist
    ORDER BY idAircraft, dtDeparture
    '''
    
    df = pd.read_sql_query(query, conn, parse_dates=['dtDeparture'])
    
    # Initialize an empty list to hold results
    results = []

    # Process each aircraft
    for aircraft_id, aircraft_data in df.groupby('idAircraft'):
        aircraft_data = aircraft_data.sort_values(by='dtDeparture')
        
        max_sequence = 0
        best_start_date = None
        best_end_date = None
        
        # Evaluate all 2-day periods
        for i in range(len(aircraft_data)):
            start_date = aircraft_data.iloc[i]['dtDeparture']
            end_date = start_date + timedelta(days=2)
            flights_in_period = aircraft_data[(aircraft_data['dtDeparture'] >= start_date) & (aircraft_data['dtDeparture'] < end_date)]

            if len(flights_in_period) > max_sequence:
                max_sequence = len(flights_in_period)
                best_start_date = start_date
                best_end_date = end_date

        # Prepare result for this aircraft
        if max_sequence > 0:
            result = {
                'Period': f"{best_start_date.date()} to {best_end_date.date()}",
                'Aircraft': f"{aircraft_id} - {aircraft_data.iloc[0]['modelAircraft']}",
                'Number of flights flown': max_sequence
            }
            results.append(result)

    # Convert results to DataFrame
    results_df = pd.DataFrame(results)
    
    # Create a new table and insert results
    results_df.to_sql('Longest_Flight_Sequences', conn, if_exists='replace', index=False)
    
    print("Table 'Longest_Flight_Sequences' created successfully.")
    
    # Close the connection
    conn.close()

# Example usage
db_path = 'Database/Flights.db'
analyze_flights(db_path)
