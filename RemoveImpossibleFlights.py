import sqlite3

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

db_file = 'Database/Flights.db'
remove_identical_flights(db_file)
