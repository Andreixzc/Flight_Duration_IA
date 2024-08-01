import sqlite3
import pandas as pd

#Script para criar e popular o banco de dados com as tabelas airports e positions

db_file = 'Database/Flights.db'

conn = sqlite3.connect(db_file)
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS positions')
cursor.execute('DROP TABLE IF EXISTS airports')

cursor.execute('''
CREATE TABLE IF NOT EXISTS positions (
    Time DATETIME,
    Latitude DECIMAL(18,12),
    Longitude DECIMAL(18,12),
    Altitude DECIMAL(28,12),
    GroundSpeed DECIMAL(28,12),
    IdAircraft INTEGER,
    ModelAircraft CHAR(50)
)
''')

# Create the airports table
cursor.execute('''
CREATE TABLE IF NOT EXISTS airports (
    Name CHAR(50),
    Code CHAR(5),
    Latitude DECIMAL(18,12),
    Longitude DECIMAL(18,12),
    Altitude DECIMAL(28,12),
    Country CHAR(50),
    City CHAR(50)
)
''')

# Commit changes
conn.commit()

# Read the CSV files
airports_df = pd.read_csv('Dataset/airports.csv', delimiter=';')
positions_df = pd.read_csv('Dataset/positions.csv', delimiter=';')

# Insert data into airports table
airports_df.to_sql('airports', conn, if_exists='append', index=False)

# Insert data into positions table
positions_df.to_sql('positions', conn, if_exists='append', index=False)

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database and tables created, and data populated successfully.")
