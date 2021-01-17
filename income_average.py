import psycopg2
import json

global state_key_list
state_key_list = []
global insert_order

with open('tables.json', 'r') as file:
    insert_table = json.load(file)
    insert = insert_table['inserts_list']
    insert_order = insert["income_state_all_average"]


def get_state_key_list(cursor):
    cursor.execute("""SELECT state_key::float FROM income_state_median;""")
    cursor.commit()  # ważne bo sprawia że wykonuje się dana operacja przed zamknięciem cursora
    list =cursor.fetchall()
    for i in list:
        if i not in state_key_list:
            state_key_list.append(i)


def calculate_average(cursor, years):
    get_state_key_list()
    year_income = []
    for s in state_key_list:
        for i in years:
            cursor.execute("""SELECT income::float FROM income_state_median WHERE
                  year = %s AND state = %s;""", (i, s))
            cursor.commit()  # ważne bo sprawia że wykonuje się dana operacja przed zamknięciem cursora
            output = cursor.fetchall()
            year_income.append(output)
        all = 0
        for record in year_income:
            all = all + record
        average = all/len(year_income)
        cursor.execute(insert_order, (s, i, average))
        cursor.commit()
        year_income = []  # zeruje tablice żeby  policzyć kolejny record
# INSERT INTO income_state_all_average (id, state_key, year, income) VALUES (%s, %s, %s, %s, %s)"


yearslist =[]
for i in range(1984, 2015):
    regex = str(i) + "-" + str(i+1) + r".*"
    yearslist.append(regex)
try:
    conn = psycopg2.connect(
        host="localhost",
        database="climate",
        user="postgres",
        password="1")
    cur = conn.cursor()
    calculate_average(cur, yearslist)
    cur.close()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.close()


