# import libraries
import pandas as pd
import psycopg2 as p2
import os
import datetime
from openpyxl.workbook import workbook
from config import config
from country_list import choose_zone,run

# connection
def connectdb():
    params = config()
    connection = p2.connect(**params)
    
    return connection

cur = connectdb().cursor()

# global variables
connection = connectdb()
zone = choose_zone()

# print country list
print(run())

def choose_country():
    country_id = int(input('Type country_id: '))
    return country_id

country = choose_country()

# sql select statement
def sql_statement():
    try:
        select =f"""
        SELECT DISTINCT 
        country, admin1_id
        , ad_name2, admin2_id
        , ad_name3, admin3_id --....
        FROM table_zone{zone}
        WHERE admin1_id = {country}"""
        return select 

    except TypeError:
        print('There is not sql statement, please paste one')

admin_path = sql_statement()

df = pd.read_sql_query(admin_path,connection)

def sort_df():
    df_sorted = df.sort_values(['country','ad_name2','ad_name3'])
    return df_sorted

def run():
    print(sort_df())

if __name__ == "__main__":
    run()