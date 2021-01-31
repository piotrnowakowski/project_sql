import json
import pandas as pd
import psycopg2
import csv

with open('tables.json') as file:
    tabela = json.load(file)
    insert_command = tabela['inserts_list']['crime_table_total']

with open('estimated_crimes_1979_2019.csv', "rt") as csv_file:
    tabela = csv.reader(csv_file, delimiter=',')
    data = [x for x in tabela]
    try:
        conn = psycopg2.connect(
                    host="localhost",
                    database="crime_test",
                    user="postgres",
                    password="1")
        for w in data[1:]:
                w = [str(-999) if x == '' else x for x in w[:-1]]
                cur = conn.cursor()

                cur.execute(insert_command, w)
                conn.commit()  # ważne bo sprawia że wykonuje się dana operacja przed zamknięciem cursora
                cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    finally:
            if conn is not None:
                conn.close()
