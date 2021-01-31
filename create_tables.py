import psycopg2


def create_tables():
    import psycopg2
    import json

    tables_key_list = ["crime_table_total", "crime_state_average", "crime_average", "income_state",
                       "income_state_all_average"]
    with open('tables.json', 'r') as file:
        insert_table = json.load(file)
        insert = insert_table['create_tables']
        for i in tables_key_list:
            print(insert[i])
            try:
                conn = psycopg2.connect(
                    host="localhost",
                    database="crime_test",
                    user="postgres",
                    password="1")

                cur = conn.cursor()
                in_str = insert[i]
                cur.execute(in_str)  # tutaj do tupla dodać info które mamy ładować
                conn.commit()  # ważne bo sprawia że wykonuje się dana operacja przed zamknięciem cursora
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()

                    
create_tables()