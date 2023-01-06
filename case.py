import pandas as pd
import mysql.connector
from os import getenv
from dotenv import load_dotenv


def query_data(prod_code: int,store_code: int,data: list):
    load_dotenv()
    config = {
        'user':getenv('DB_USER'),
        'password': getenv('PASSWORD'),
        'host': getenv('HOST'),
        'database':getenv('DATABASE')
                                        }

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary=True)

    query = f"""
            SELECT * FROM
            data_product_sales
            WHERE PRODUCT_CODE = {prod_code}
            AND STORE_CODE = {store_code}
            AND DATE BETWEEN '{data[0]}' AND '{data[1]}'

                                                            """

    cursor.execute(query)
    rows = cursor.fetchall()
    return pd.DataFrame(rows)

