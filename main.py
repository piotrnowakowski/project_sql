import pandas as pd
#with pd.read_excel(r'Household Income.xls') as house_income:
house_income = pd.read_excel(r'Household Income.xls')
list_columns = ['State', 'State code']
for i in range(1984, 2015):
    regex = str(i) + "-" + str(i+1) + r".*"
    list_columns.append(regex)

liczba = pd.DataFrame(house_income, index=['Alaska', 'Alabama', 'Arizona', 'Arkansas'])
liczba = liczba.loc['Alaska']
for r in range(1, 52):
    row = house_income.loc[r, :]
    print(row)
    indices = [0, 1, 2]
    for i in range(2, 62, 2):
        indices.append(i)
    #print(indices)
    data_toload = [row.iloc[index] for index in indices]
    print(data_toload)
    #data_insert(data_toload)

