import psycopg2
import json
import pandas as pd

tables_key_list = ["crime_table_total", "crime_state_average", "crime_average", "income_state_median",
                   "income_state_all_average"]
with open('tables.json', 'r') as file:
    insert_table = json.load(file)
    insert = insert_table['inserts_list']
    for i in tables_key_list:
        print(insert[i])

house_income = pd.read_excel(r'Household Income.xls')


def load_crime_rate():
    for r in range(1, 52):
        row = house_income.loc[r, :]
        indices = [0, 1, 2]
        for i in range(2, 62, 2):
            indices.append(i)
        data_toload = [row.iloc[index] for index in indices]
        print(data_toload)


