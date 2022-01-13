
import pandas
import csv, sqlite3
conn= sqlite3.connect("./Result/Data.db")
df = pandas.read_csv('./Result/Data_Step2(WithHeader).csv')
df.to_sql('Data', conn, if_exists='append', index=False)
print('ok')
