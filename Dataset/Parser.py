import csv
from datetime import datetime

class Position:
    def __init__(self, time, latitude, longitude, altitude, groundSpeed, idAircraft, modelAircraft):
        self.time = time
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.groundSpeed = groundSpeed
        self.idAircraft = idAircraft
        self.modelAircraft = modelAircraft

    def __str__(self):
        return f"Position{{time='{self.time}', latitude={self.latitude}, longitude={self.longitude}, altitude={self.altitude}, groundSpeed={self.groundSpeed}, idAircraft='{self.idAircraft}', modelAircraft='{self.modelAircraft}'}}"

class Flight:
    def __init__(self, saida, chegada):
        self.saida = saida
        self.chegada = chegada

    def __str__(self):
        return f"Flight [saida={self.saida}, chegada={self.chegada}]"

def is_interval_greater_than_three_minutes(time1, time2):
    try:
        date1 = datetime.strptime(time1, '%Y-%m-%d %H:%M:%S.%f')
        date2 = datetime.strptime(time2, '%Y-%m-%d %H:%M:%S.%f')
        diff_in_minutes = abs((date2 - date1).total_seconds() / 60)
        return diff_in_minutes > 3
    except Exception as e:
        print(f"Erro ao comparar datas: {e}")
        return False

def parse(filename):
    positions = []
    voos = []

    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Ler e descartar o cabeçalho

            for row in reader:
                current_position = Position(
                    time=row[0],
                    latitude=float(row[1]),
                    longitude=float(row[2]),
                    altitude=float(row[3]),
                    groundSpeed=float(row[4]),
                    idAircraft=row[5],
                    modelAircraft=row[6]
                )
                positions.append(current_position)

        # Processar as posições para segmentar voos
        i = 0
        while i < len(positions):
            start = positions[i]
            end = start
            j = i + 1
            while j < len(positions):
                next_pos = positions[j]
                if is_interval_greater_than_three_minutes(end.time, next_pos.time):
                    break
                end = next_pos
                j += 1
            if end != start:
                flight = Flight(saida=start.time, chegada=end.time)
                voos.append(flight)
                i = j  # Avançar o ponteiro para o próximo segmento de voo
            else:
                i += 1

    except Exception as e:
        print(e)

    print("Voos segmentados:")
    for voo in voos:
        print(voo)

if __name__ == "__main__":
    sorted_positions_csv = "E:/Projetos/TesteTecnico/Dataset/PosSorted/11.csv"
    parse(sorted_positions_csv)
