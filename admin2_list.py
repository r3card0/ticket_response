# import libraries
import pandas as pd
import psycopg2 as p2
import os
import datetime
from openpyxl.workbook import workbook
from main import connectdb
from country_list import choose_zone, sql_statement

def description():
    program_description = """
    This program extracts the list of admin 2
    from a selected country
    """
    return program_description

# global variables
connection = connectdb()
zone = choose_zone()
country_list = sql_statement()

# get country list
def country_list1():
    df = pd.read_sql_query(country_list,connection)
    return df

print(country_list1())

# Select country id
def select_country():
    country_id = int(input('Type country id: '))
    return country_id

country = select_country()

# Run sql statement
def sql_statement1():
    try:
        select =f"""
        SELECT DISTINCT 
        country, ad_name2, admin2_id
        FROM table_zone{zone}
        WHERE admin1_id = {country}"""
        
        return select 

    except TypeError:
        print('There is not sql statement, please paste one')

admin2 = sql_statement1()

# Get admin2 list
def admin2_list():
    df = pd.read_sql_query(admin2,connection)
    df.dropna()
    pd.options.display.float_format = '{:}'.format # no decimals
    #df.astype(int)
    df = df.sort_values(['country','ad_name2'])
    return df

def run():
    print(description())
    print(admin2_list())

if __name__ == "__main__":
    run()