import pandas as pd
import numpy as np

csv_file = "files\\sales_dirty.csv"
df = pd.read_csv(csv_file)

df_copy = df.copy()

#VALUE
# clean the value rows and leave the dot and comma only
df_copy['value'] = df_copy['value'].replace(r'[^\w\s\.]','',regex=True)
df_copy['value'] = df_copy['value'].str.replace(',','.')
# change it back to number and if not number change it to NaN
df_copy['value'] = pd.to_numeric(df_copy['value'], errors='coerce')
# drop NaN values
df_copy = df_copy.dropna(subset=['value'])
df_copy = df_copy[df_copy['value'] < 100000]

#EXPENSES
df_copy['expenses'] = df_copy['expenses'].replace(r'[^\w\s\.\,]','',regex=True)
df_copy['expenses'] = df_copy['expenses'].replace(',','.')
df_copy['expenses'] = df_copy['expenses'].replace('-','')
df_copy['expenses'] = pd.to_numeric(df_copy['expenses'], errors='coerce')
df_copy = df_copy.dropna(subset=['expenses'])
df_copy = df_copy[df_copy['expenses'] < 100000]

#PROFIT
df_copy = df_copy.drop(columns='profit')
df_copy['profit'] = df_copy['value'] - df_copy['expenses']
df_copy['profit'] = pd.to_numeric(df_copy['profit'], errors='coerce')
df_copy['profit'] = pd.to_numeric(df_copy['profit']).round(2)

#BOUGHT_BY
df_copy['bought_by'] = df_copy['bought_by'].str.lower()
df_copy['bought_by'] = df_copy['bought_by'].replace(['computer','desktop','pc'],value='Site')
df_copy['bought_by'] = df_copy['bought_by'].replace(['phone','cellphone'],value='App')
df_copy['bought_by'] = df_copy['bought_by'].replace(['buy local','store'],value='OnSite')

#PAYMENT_METHOD
df_copy['payment_method'] = df_copy['payment_method'].str.lower()
df_copy['payment_method'] = df_copy['payment_method'].replace(['credit card'],value='credit')
df_copy['payment_method'] = df_copy['payment_method'].replace(['debit card'],value='debit')
df_copy['payment_method'] = df_copy['payment_method'].replace(['money'],value='cash')

#PURCHASE_DATE
df_copy['purchase_date'] = pd.to_datetime(df_copy['purchase_date'],errors='coerce',dayfirst=False,format='mixed')
df_copy['purchase_date'] = pd.to_datetime(df_copy['purchase_date'], format='%d/%m/%Y')

#PURCHASE_ID
df_copy = df_copy.sort_values(by='purchase_date', ascending=False).drop_duplicates(subset='purchase_id', keep='first')
df_copy = df_copy.dropna(subset='purchase_id')

#new file
df_copy.to_csv(path_or_buf='files/sales_cleaned.csv', index=False)

print(df_copy.info())