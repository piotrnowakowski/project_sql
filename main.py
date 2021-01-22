import pandas as pd
import psycopg2
import csv
import json
import codecs
#with pd.read_excel(r'Household Income.xls') as house_income:
house_income = pd.read_excel(r'Household Income.xls')
list_columns = ['State', 'State code']
with open('tables.json') as file:
    tabela = json.load(file)
    insert_command = tabela['inserts_list']['crime_table_total']

with open('estimated_crimes_1979_2019.csv', "rt") as csv_file:
    #tabela = csv.reader(codecs.iterdecode(csv_file, 'utf-8'), delimiter=',')
    tabela = csv.reader(csv_file, delimiter=',')
    #next(tabela)
    for w in tabela:
        try:
            conn = psycopg2.connect(
                    host="localhost",
                    database="crime_test",
                    user="postgres",
                    password="haslo")

            cur = conn.cursor()
            cur.execute(insert_command, w)  # tutaj do tupla dodać info które mamy ładować
            conn.commit()  # ważne bo sprawia że wykonuje się dana operacja przed zamknięciem cursora
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
