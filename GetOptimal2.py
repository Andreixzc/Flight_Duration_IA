import csv
from geopy.distance import geodesic

# Função para calcular a duração mínima do voo em minutos
def flight_duration(distance, speed_kmh=900):
    return (distance / speed_kmh) * 60  # Converte horas em minutos

# Caminho do arquivo CSV
csv_file_path = 'Dataset/airports.csv'

# Limiar mínimo para a distância (em km)
min_distance_threshold = 200  # Ajuste conforme necessário
distance_tolerance = 100  # Tolerância para agrupar aeroportos próximos (em km)

# Lista para armazenar os dados dos aeroportos
airports = []

# Lê o arquivo CSV e armazena os dados na lista
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        airports.append({
            'Name': row['Name'],
            'Code': row['Code'],
            'Latitude': float(row['Latitude']),
            'Longitude': float(row['Longitude']),
            'Altitude': float(row['Altitude']),
            'Country': row['Country'],
            'City': row['City']
        })

# Calcula a distância de cada aeroporto a partir de um ponto fixo (0, 0) e ordena a lista
origin = (0, 0)
for airport in airports:
    airport['DistanceFromOrigin'] = geodesic(origin, (airport['Latitude'], airport['Longitude'])).kilometers

# Ordena os aeroportos pela distância do ponto fixo
airports.sort(key=lambda x: x['DistanceFromOrigin'])


print("Aeroportos ordenados pela distância do ponto fixo (0, 0):")
for airport in airports:
    print(f"{airport['Name']} ({airport['Code']}): {airport['DistanceFromOrigin']:.2f} km")

# Variáveis para armazenar a distância mínima e a duração mínima do voo
min_distance = float('inf')
min_duration = float('inf')
min_airports_pair = ()
airport_names = ()

# Itera sobre a lista ordenada para comparar apenas aeroportos dentro da tolerância de distância
for i in range(len(airports)):
    airport1 = airports[i]
    for j in range(i + 1, len(airports)):
        airport2 = airports[j]
        distance = geodesic((airport1['Latitude'], airport1['Longitude']),
                            (airport2['Latitude'], airport2['Longitude'])).kilometers
        
        # Print para depuração: distância calculada
       
        
        if distance >= min_distance_threshold:  # Certifica-se de que a distância é maior que o limiar
            duration = flight_duration(distance)
            
            # Print para depuração: duração calculada

            
            if duration < min_duration:
                min_distance = distance
                min_duration = duration
                min_airports_pair = (airport1['Code'], airport2['Code'])
                airport_names = (airport1['Name'], airport2['Name'])

        # Se a diferença de distância já excedeu a tolerância, não faz sentido continuar a comparação
        if airport2['DistanceFromOrigin'] - airport1['DistanceFromOrigin'] > distance_tolerance:
            break

if min_airports_pair:
    print(f"A menor duração de voo é entre os aeroportos {min_airports_pair[0]} ({airport_names[0]}) e {min_airports_pair[1]} ({airport_names[1]})")
    print(f"Distância: {min_distance:.2f} km")
    print(f"Duração mínima do voo: {min_duration:.2f} minutos")
else:
    print("Não foi possível encontrar uma duração mínima de voo válida entre os aeroportos.")
