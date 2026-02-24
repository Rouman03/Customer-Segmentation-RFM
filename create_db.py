import pandas as pd
import sqlite3


df = pd.read_excel("data/online_retail_II.xlsx")


df = df.dropna(subset=['Customer ID'])
df = df[~df['Invoice'].astype(str).str.startswith('C')]
df = df[df['Quantity'] > 0]
df['TotalPrice'] = df['Quantity'] * df['Price']
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
conn = sqlite3.connect("database/retail.db")
df.to_sql("transactions", conn, if_exists="replace", index=False)

print("Database created successfully!")
