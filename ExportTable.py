import sqlite3
import csv
import argparse

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exporta dados de uma tabela SQLite para um arquivo CSV.")
    parser.add_argument("table_name", help="Nome da tabela a ser exportada.")
    parser.add_argument("--db_file", default='Database/Flights.db', help="Caminho para o arquivo de banco de dados SQLite.")
    parser.add_argument("--output_csv_file", default='Dataset/output.csv', help="Caminho para o arquivo CSV de saída.")

    args = parser.parse_args()
    
    export_table_to_csv(args.db_file, args.table_name, args.output_csv_file)
