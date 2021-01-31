import json
import pandas as pd
import psycopg2
import csv
import time
start = time.time()


def getvalue(cur, crime, year):
    command = ("SELECT {} FROM crime_table_total WHERE year='{}';""".format(crime, year[0]))
    cur.execute(command)
    ret = cur.fetchall()
    return ret


def calculate_average(cur, crime, year):
    crime_all_records = getvalue(cur, crime, year)
    crime_average = [year[0], crime]
    average = 0
    for r in crime_all_records:
        if r[0] != -999:
            average += r[0]
    wrong_value_list = [x for x in crime_all_records if x == -999]
    average = average / (len(crime_all_records) - len(wrong_value_list))
    crime_average.append(average)

    return crime_average


def years_list(cur):
    command = "SELECT year FROM crime_table_total"
    cur.execute(command)
    statesr = cur.fetchall()
    years = []
    for s in statesr:
        if s not in years:
            years.append(s)
    return years


with open('tables.json') as file:
    tabela = json.load(file)
    insert_command = tabela['inserts_list']['crime_average']

crimes = ["violent_crime", "homicide", "rape_l", "rape_r", "robbery", "assault", "property",
          "burglary", "larceny", "vehicle"]
try:
    conn = psycopg2.connect(
                    host="localhost",
                    database="crime_test",
                    user="postgres",
                    password="1")
    cur = conn.cursor()
    years = years_list(cur)
    for crime in crimes:
        for year in years:
            w = calculate_average(cur, crime, year)
            cur.execute(insert_command, w)
            conn.commit()  # ważne bo sprawia że wykonuje się dana operacja przed zamknięciem cursora
    cur.close()
except (Exception, psycopg2.DatabaseError) as error:
            print(error)
finally:
    if conn is not None:
        conn.close()

print("it took {} seconds to execute script".format(time.time()-start))
