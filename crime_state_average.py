import json
import pandas as pd
import psycopg2
import csv
import time
start = time.time()


def getvalue(cur, state):
    command = ("SELECT * FROM crime_table_total WHERE state_key='{}';""".format(state))
    cur.execute(command)
    ret = cur.fetchall()
    return ret


def calculate_average(cur, state):
    state_all_records = getvalue(cur, state)
    state_average = list(state_all_records[0])
    if -999 in state_average:
        state_average[state_average.index(-999)] = 0
    for record in state_all_records[1::]:
        for r in [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]:
            if record[r] != -999:
                state_average[r] += record[r]
    for r in [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]:
        state_average[r] = state_average[r] / len(state_all_records)
    return state_average


def state_list(cur):
    command = "SELECT state_key FROM crime_table_total"
    cur.execute(command)
    statesr = cur.fetchall()
    states = []
    for s in statesr:
        if s not in states:
            states.append(s)
    return states


with open('tables.json') as file:
    tabela = json.load(file)
    insert_command = tabela['inserts_list']['crime_state_average']


try:
    conn = psycopg2.connect(
                    host="localhost",
                    database="crime_test",
                    user="postgres",
                    password="1")
    cur = conn.cursor()
    states = state_list(cur)
    print(states)
    for state in states:
        w = calculate_average(cur, state[0])
        #print(w)
        #cur.execute(insert_command, w)
        conn.commit()  # ważne bo sprawia że wykonuje się dana operacja przed zamknięciem cursora
    cur.close()
except (Exception, psycopg2.DatabaseError) as error:
            print(error)
finally:
    if conn is not None:
        conn.close()

print("it took {} seconds to execute script".format(time.time()-start))
