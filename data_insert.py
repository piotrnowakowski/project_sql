import psycopg2
import json
import pandas as pd
import time
start = time.time()
tables_key_list = ["crime_table_total", "crime_state_average", "crime_average", "income_state_median",
                   "income_state_all_average"]
with open('tables.json', 'r') as file:
    insert_table = json.load(file)
    insert = insert_table['inserts_list']
    command = insert['income_state']  # Here you cand define command variable to get a command you want to use by
                                      # choosing a key from tables_key_list right now it stores insert command I use

house_income = pd.read_excel(r'Household Income.xls')


def load_crime_rate(command):
    data_toload = []
    for r in range(1, 52):
        row = house_income.loc[r, :]
        indices = [0, 1]
        for j in range(2, 62, 2):
            indices.append(j)

        data_toload.append([row.iloc[index] for index in indices])
    for i in data_toload:
        year_max = 2014
        for r in range(0, 30):
            data = []
            data.append(i[0])
            data.append(i[1])
            data.append(year_max)
            data.append(i[r+2])
            year_max -= 1
            try:
                conn = psycopg2.connect(
                    host="localhost",
                    database="crime_test",
                    user="postgres",
                    password="1")
                cur = conn.cursor()
                in_str = command
                cur.execute(in_str, tuple(data))  # tutaj do tupla dodać info które mamy ładować
                conn.commit()  # ważne bo sprawia że wykonuje się dana operacja przed zamknięciem cursora
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()


load_crime_rate(command)
print ("it took {} seconds to execute script".format(time.time()-start))