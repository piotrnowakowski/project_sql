import psycopg2
import json
import pandas as pd

tables_key_list = ["crime_table_total", "crime_state_average", "crime_average", "income_state_median",
                   "income_state_all_average"]
with open('tables.json', 'r') as file:
    insert_table = json.load(file)
    insert = insert_table['inserts_list']
