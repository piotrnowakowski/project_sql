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
    cursor.execute("""SELECT state_key FROM income_state;""")
    #cursor.commit()  # ważne bo sprawia że wykonuje się dana operacja przed zamknięciem cursora
    list =cursor.fetchall()
    for i in list:
        if i not in state_key_list:
            state_key_list.append(i)


def calculate_average(cursor, years):
    get_state_key_list(cursor)
    year_income = []
    for s in state_key_list:
        for i in years:
            cursor.execute("""SELECT income FROM income_state WHERE
                  year=%s AND state_key=%s;""", (str(i), str(s[0])))
            #cursor.commit()  # ważne bo sprawia że wykonuje się dana operacja przed zamknięciem cursora
            output = cursor.fetchall()
            year_income.append(output[0][0])
        all = 0
        for record in year_income:
            all = all + record
        average = all/len(year_income)
        query = "INSERT INTO income_state_all_average (state_key, income) VALUES (%s, %s);"
        cursor.execute(query, [str(s[0]), int(average)])
        conn.commit()
        year_income = []  # zeruje tablice żeby  policzyć kolejny record


yearslist =[]
for i in range(1985, 2015):
    #regex = str(i) + "-" + str(i+1) + r".*"
    yearslist.append(i)
try:
    conn = psycopg2.connect(
        host="localhost",
        database="crime_test",
        user="postgres",
        password="haslo")
    cur = conn.cursor()
    calculate_average(cur, yearslist)
    cur.close()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.close()


