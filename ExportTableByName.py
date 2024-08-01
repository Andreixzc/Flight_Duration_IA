import sqlite3
import csv

def export_table_to_csv(db_file, table_name, output_csv_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    try:
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [column[1] for column in cursor.fetchall()]

        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        with open(output_csv_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(columns)  
            writer.writerows(rows)   

        print(f"Dados da tabela '{table_name}' foram exportados para '{output_csv_file}' com sucesso.")
    except Exception as e:
        print(f"Erro ao exportar a tabela: {e}")
    finally:
        conn.close()


db_file = 'Database/Flights.db'
table_name = 'flightSummary' 
output_csv_file = 'Dataset/flightSummaryNew.csv'  
# table_name = 'Longest_Flight_Sequences'
# output_csv_file = 'Dataset/Longest_Flight_Sequences.csv'
export_table_to_csv(db_file, table_name, output_csv_file)
