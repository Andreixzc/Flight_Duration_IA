import csv
from datetime import datetime, timedelta

class Position:
    def __init__(self, time, latitude, longitude, altitude, ground_speed, id_aircraft, model_aircraft):
        self.time = time
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.ground_speed = ground_speed
        self.id_aircraft = id_aircraft
        self.model_aircraft = model_aircraft
    
    def __str__(self):
        return (f"Position(time={self.time}, latitude={self.latitude}, longitude={self.longitude}, "
                f"altitude={self.altitude}, ground_speed={self.ground_speed}, "
                f"id_aircraft={self.id_aircraft}, model_aircraft={self.model_aircraft})")

class Flight:
    def __init__(self, departure, arrival):
        self.departure = departure
        self.arrival = arrival
    
    def __str__(self):
        return f"Flight [departure={self.departure}, arrival={self.arrival}]"

def parse(filename):
    positions = []
    flights = []
    
    # Define the date format
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    
    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header
            
            for row in reader:
                time = row[0]
                latitude = float(row[1])
                longitude = float(row[2])
                altitude = float(row[3])
                ground_speed = float(row[4])
                id_aircraft = row[5]
                model_aircraft = row[6]
                
                positions.append(Position(time, latitude, longitude, altitude, ground_speed, id_aircraft, model_aircraft))
        
        # Process positions to segment flights
        i = 0
        while i < len(positions):
            start = positions[i]
            end = start
            for j in range(i + 1, len(positions)):
                next_position = positions[j]
                if is_interval_greater_than_three_minutes(date_format, end.time, next_position.time):
                    break
                else:
                    end = next_position
            
            if end != start:
                flights.append(Flight(start.time, end.time))
                # Move to the next position after end
                i = positions.index(end) + 1
            else:
                i += 1
    
    except Exception as e:
        print(f"Error reading file: {e}")
    
    print("Segmented Flights:")
    for flight in flights:
        print(flight)

def is_interval_greater_than_three_minutes(date_format, date1, date2):
    try:
        d1 = datetime.strptime(date1, date_format)
        d2 = datetime.strptime(date2, date_format)
        diff_in_minutes = abs((d2 - d1) / timedelta(minutes=1))
        return diff_in_minutes > 5
    except Exception as e:
        print(f"Error comparing dates: {e}")
        return False

if __name__ == "__main__":
    sorted_positions_csv = "E:/Projetos/TesteTecnico/Dataset/PosSorted/11.csv"
    parse(sorted_positions_csv)
