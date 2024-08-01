import sqlite3
import csv

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

def main():
    db_file = 'Database/Flights.db'
    csv_file = 'E:/Projetos/TesteTecnico/Dataset/combined_flightsNew.csv'
    
    conn = sqlite3.connect(db_file)
    
    # Criar a tabela
    create_table(conn)
    
    # Inserir dados
    insert_data(conn, csv_file)
    
    # Fechar a conexão
    conn.close()

if __name__ == '__main__':
    main()
