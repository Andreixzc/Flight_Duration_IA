import sqlite3
import pandas as pd

# Define the CSV file and SQLite database
csv_file = 'flight_duration_model_data.csv'
db_file = 'flight_data.db'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file, delimiter=';')

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Define the table creation SQL statement
create_table_sql = '''
CREATE TABLE IF NOT EXISTS flight_duration (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    OriginCode TEXT,
    DestinCode TEXT,
    WeekDay TEXT,
    HourDeparture TEXT,
    ModelAircraft TEXT,
    FlightDuration REAL
)
'''

# Execute the table creation SQL statement
cursor.execute(create_table_sql)

# Get column names from DataFrame
columns = df.columns
column_names = ', '.join(columns)
placeholders = ', '.join(['?'] * len(columns))

# Define the insert SQL statement with placeholders
insert_sql = f'INSERT INTO flight_duration ({column_names}) VALUES ({placeholders})'

# Iterate over the rows of the DataFrame and insert them into the table
for row in df.itertuples(index=False, name=None):
    cursor.execute(insert_sql, row)

# Commit the changes and close the connection
conn.commit()
conn.close()

print('Table created and data inserted successfully.')
