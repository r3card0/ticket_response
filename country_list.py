# import libraries
import pandas as pd
import psycopg2 as p2
import os
import datetime
from openpyxl.workbook import workbook
from config import config

## This program extract a list of countries by zones

# connection
def connectdb():
    params = config()
    connection = p2.connect(**params)
    
    return connection

cur = connectdb().cursor()

connection = connectdb()



def choose_zone():
    zone = input('Ingresa la zona a buscar: ')
    zone = zone.lower()
    return zone

zone = choose_zone()

# sql select statement
def sql_statement():
    try:
        select =f"""
        SELECT DISTINCT country, country_id
        FROM country_{zone}
        ORDER BY 1
        """
        return select 

    except TypeError:
        print('There is not sql statement, please paste one')

country_list = sql_statement()

df = pd.read_sql_query(country_list,connection)

def run():
    print(df)

if __name__ == "__main__":
    run()