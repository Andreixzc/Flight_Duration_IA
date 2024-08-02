import csv
import os
from datetime import datetime, timedelta
import sqlite3

#Script que segmenta os voos baseado na diferença de tempo entre as posições entre os registros, e puxa 
# os aeroportos da origem e destino pelas coordenadas das mesmas.


class Position:
    def __init__(self, time, latitude, longitude, altitude, ground_speed, id_aircraft, model_aircraft):
        self.time = time
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.altitude = float(altitude)
        self.ground_speed = float(ground_speed)
        self.id_aircraft = id_aircraft
        self.model_aircraft = model_aircraft

class Flight:
    def __init__(self, departure, arrival, lat_s, lon_s, lat_e, lon_e, id_aircraft, model_aircraft):
        self.departure = departure
        self.arrival = arrival
        self.lat_s = lat_s
        self.lon_s = lon_s
        self.lat_e = lat_e
        self.lon_e = lon_e
        self.id_aircraft = id_aircraft
        self.model_aircraft = model_aircraft

def is_interval_greater_than_three_minutes(date_format, date1, date2):
    try:
        d1 = datetime.strptime(date1, date_format)
        d2 = datetime.strptime(date2, date_format)
        diff_in_minutes = abs((d2 - d1) / timedelta(minutes=1))
        return diff_in_minutes >= 30
    except Exception as e:
        print(f"Error comparing dates: {e}")
        return False

def get_closest_airport(lat, lon, airports):
    min_dist = float('inf')
    closest_airport = None
    for airport in airports:
        dist = ((airport['Latitude'] - lat) ** 2 + (airport['Longitude'] - lon) ** 2) ** 0.5
        if dist < min_dist:
            min_dist = dist
            closest_airport = airport
    return closest_airport

def remove_bom(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        content = file.read()
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def parse_file(file_path, date_format, airports):
    positions = []
    flights = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            
            for row in reader:
                if len(row) == 7:
                    time, latitude, longitude, altitude, ground_speed, id_aircraft, model_aircraft = row
                    positions.append(Position(time, latitude, longitude, altitude, ground_speed, id_aircraft, model_aircraft))
                else:
                    print(f"Skipping row with incorrect number of fields: {row}")
        
        i = 0
        while i < len(positions):
            start = positions[i]
            end = start
            j = i + 1

            while j < len(positions):
                next_position = positions[j]
                if is_interval_greater_than_three_minutes(date_format, end.time, next_position.time):
                    break
                else:
                    end = next_position
                j += 1

            if end != start:
                departure_airport = get_closest_airport(start.latitude, start.longitude, airports)
                arrival_airport = get_closest_airport(end.latitude, end.longitude, airports)

                flight = {
                    'dtDeparture': start.time,
                    'codeDeparture': departure_airport['Code'] if departure_airport else '',
                    'NameDeparture': departure_airport['Name'] if departure_airport else '',
                    'CityDeparture': departure_airport['City'] if departure_airport else '',
                    'dtArrival': end.time,
                    'codeDestin': arrival_airport['Code'] if arrival_airport else '',
                    'NameDestin': arrival_airport['Name'] if arrival_airport else '',
                    'cityDestin': arrival_airport['City'] if arrival_airport else '',
                    'idAircraft': start.id_aircraft,
                    'modelAircraft': start.model_aircraft
                }
                flights.append(flight)
                i = positions.index(end) + 1
            else:
                i += 1

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

    return flights

def parse_directory(directory, airport_file, output_file):
    remove_bom(airport_file)  # Remove BOM if present

    airports = []
    try:
        with open(airport_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                airport = {
                    'Name': row['Name'],
                    'Code': row['Code'],
                    'Latitude': float(row['Latitude']),
                    'Longitude': float(row['Longitude']),
                    'City': row['City']
                }
                airports.append(airport)
    except Exception as e:
        print(f"Error reading airport file: {e}")
        return

    all_flights = []
    date_format = "%Y-%m-%d %H:%M:%S.%f"

    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)
            flights = parse_file(file_path, date_format, airports)
            all_flights.extend(flights)

    # Write results to output CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['dtDeparture', 'codeDeparture', 'NameDeparture', 'CityDeparture', 'dtArrival', 'codeDestin', 'NameDestin', 'cityDestin', 'idAircraft', 'modelAircraft']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        
        for flight in all_flights:
            writer.writerow(flight)

    print(f"Data written to {output_file}")

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS flightList (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dtDeparture TEXT NOT NULL,
        codeDeparture TEXT,
        NameDeparture TEXT,
        CityDeparture TEXT,
        dtArrival TEXT NOT NULL,
        codeDestin TEXT,
        NameDestin TEXT,
        cityDestin TEXT,
        idAircraft TEXT NOT NULL,
        modelAircraft TEXT
    )
    ''')
    conn.commit()

def insert_data(conn, csv_file):
    cursor = conn.cursor()
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute('''
            INSERT INTO flightList (
                dtDeparture, codeDeparture, NameDeparture, CityDeparture,
                dtArrival, codeDestin, NameDestin, cityDestin, idAircraft, modelAircraft
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['dtDeparture'], row['codeDeparture'], row['NameDeparture'], row['CityDeparture'],
                row['dtArrival'], row['codeDestin'], row['NameDestin'], row['cityDestin'],
                row['idAircraft'], row['modelAircraft']
            ))
    conn.commit()


def remove_identical_flights(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Remove registros onde origem e destino são iguais
    cursor.execute('''
        DELETE FROM flightList
        WHERE (codeDeparture = codeDestin AND cityDeparture = cityDestin)
    ''')

    conn.commit()
    conn.close()


# Example usage
directory = "E:/Projetos/TesteTecnico/Dataset/PosSorted/"
airport_file = "E:/Projetos/TesteTecnico/Dataset/airports.csv"
output_file = "E:/Projetos/TesteTecnico/Dataset/combined_flightsNew.csv"
parse_directory(directory, airport_file, output_file)


db_file = 'Database/Flights.db'
csv_file = 'E:/Projetos/TesteTecnico/Dataset/combined_flightsNew.csv'
    
conn = sqlite3.connect(db_file)
create_table(conn)
insert_data(conn, csv_file)
print('Data inserted successfully.')
conn.close()

remove_identical_flights(db_file)
print('Identical flights removed successfully.')



