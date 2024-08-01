import sqlite3
from datetime import datetime
#Gera dataset de treino, puxando os voos segmentados  na tabela 'flightList' e salvnado na tabela 'flightSummary'.
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

def generate_flight_summary(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flightSummary (
            OriginCode TEXT,
            DestinCode TEXT,
            WeekDay INTEGER,
            HourDeparture INTEGER,
            ModelAircraft TEXT,
            Duration INTEGER
        );
    ''')

    cursor.execute('DELETE FROM flightSummary')
    cursor.execute('''
        INSERT INTO flightSummary (OriginCode, DestinCode, WeekDay, HourDeparture, ModelAircraft, Duration)
        SELECT 
            codeDeparture AS OriginCode,
            codeDestin AS DestinCode,
            strftime('%w', dtDeparture) + 1 AS WeekDay,  -- Adjust for SQLite's strftime output
            strftime('%H', dtDeparture) AS HourDeparture,
            modelAircraft AS ModelAircraft,
            (strftime('%s', dtArrival) - strftime('%s', dtDeparture)) / 60 AS Duration
        FROM flightList
    ''')
    conn.commit()
    conn.close()


db_file = 'Database/Flights.db'
generate_flight_summary(db_file)
