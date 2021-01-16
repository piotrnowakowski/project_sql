import psycopg2
import json
import pandas as pd

tables_key_list = ["crime_table_total", "crime_state_average", "crime_average", "income_state_median",
                   "income_state_all_average"]
with open('tables.json', 'r') as file:
    insert_table = json.load(file)
    insert = insert_table['inserts_list']


house_income = pd.read_excel(r'Household Income.xls')


def load_crime_rate(command):
    data_toload = []
    for r in range(1, 52):
        row = house_income.loc[r, :]
        indices = [0, 1, 2]
        for i in range(2, 62, 2):
            indices.append(i)

        data_toload.append([row.iloc[index] for index in indices])
    for i in data_toload:
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="climate",
                user="postgres",
                password="1")
            cur = conn.cursor()
            in_str = command
            cur.execute(in_str, tuple(i))  # tutaj do tupla dodać info które mamy ładować
            conn.commit()  # ważne bo sprawia że wykonuje się dana operacja przed zamknięciem cursora
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

load_crime_rate()
