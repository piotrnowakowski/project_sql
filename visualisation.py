try:
    conn = psycopg2.connect(
        host="localhost",
        database="climate",
        user="postgres",
        password="1")

    cur = conn.cursor()
    in_str = value
    cur.execute(in_str)
    conn.commit()  # ważne bo sprawia że wykonuje się dana operacja przed zamknięciem cursora
    cur.close()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.close()