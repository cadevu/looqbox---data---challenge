import pandas as pd
import mysql.connector
from datetime import date
from os import getenv
from dotenv import load_dotenv
load_dotenv()
config = {
        'user':getenv('DB_USER'),
        'password': getenv('PASSWORD'),
        'host': getenv('HOST'),
        'database':getenv('DATABASE')
                                        }

cnx = mysql.connector.connect(**config)
query1 = """
SELECT
      STORE_CODE,
      STORE_NAME,
      START_DATE,
      END_DATE,
      BUSINESS_NAME,
      BUSINESS_CODE
FROM data_store_cad
"""
query2 = """
SELECT
        STORE_CODE,
        DATE,
        SALES_VALUE,
        SALES_QTY
FROM data_store_sales
WHERE DATE BETWEEN '2019-01-01' AND '2019-12-31'
"""
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor(dictionary=True)
cursor.execute(query1)

df1 = pd.DataFrame(cursor.fetchall())
cursor.execute(query2)
df2 = pd.DataFrame(cursor.fetchall())
data_filter = [date(2019,10,1),date(2019,12,31)]
mask = (df2['DATE'] >= data_filter[0]) & (df2['DATE'] <= data_filter[1])
df2 = df2.loc[mask]

df1 = df1[['STORE_NAME','BUSINESS_NAME','STORE_CODE']].drop_duplicates()
df2 = df2[['STORE_CODE','SALES_VALUE','SALES_QTY']].groupby('STORE_CODE').sum().reset_index()
df1['TM'] = round ((df2['SALES_VALUE']/df2['SALES_QTY']),2)
df1.drop(columns = 'STORE_CODE',inplace=True)
df1.sort_values(by='STORE_NAME',inplace=True)

df1.rename(columns={"STORE_NAME":"LOJA","BUSINESS_NAME":"CATEGORIA"},inplace=True)
df1.reset_index(drop = True, inplace=True)

print(df1)
