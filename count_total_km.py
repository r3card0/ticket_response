# libraries
import pandas as pd
import psycopg2 as p2
import os
import datetime
from openpyxl.workbook import workbook
from config import config



def description():
    program_description = """
    This program calculates the total kms of roads
    non navegables and navegables from a country
    """
    return program_description

# connection
def connectdb():
    params = config()
    connection = p2.connect(**params)
    
    return connection

cur = connectdb().cursor()


def choose_zone():
    zone = input('Ingresa la zona a buscar: ')
    zone = zone.lower()
    return zone

# global variables
connection = connectdb()
zone = choose_zone()

# sql select statement countries
def sql_statement():
    try:
        countries =f"""
        SELECT DISTINCT country
        , country_id
        FROM country_table_{zone}
        ORDER BY 1
        """
        return countries 

    except TypeError:
        print('There is not sql statement, please paste one')

countries = sql_statement()

def country_list():
    df_countries = pd.read_sql_query(countries,connection)
    return df_countries

def select_country():
    print(country_list())
    country_id = input('Select a country, entry country_id: ')
    return country_id

# global variables
country_id = select_country()

def sql_statement():
    try:
        select =f"""
        SELECT distinct country
        , sum((SELECT sum(meters / 1000) FROM road_{zone} WHERE road_nav=1 ')) as km_nav
        , sum((SELECT sum(meters / 1000) FROM road_{zone} WHERE road_nav=0 ')) as km_not_nav
        FROM table_{zone}
        WHERE country_id = {country_id} -- Country
        GROUP BY country
        ORDER BY 1
        """
        return select 

    except TypeError:
        print('There is not sql statement, please paste one')

km = sql_statement()

def dataframe():
    df = pd.read_sql_query(km,connection)
    df.loc[:,'km_total'] = df.sum(axis=1)
    return df

def run():
    print(description())
    #print(connection)
    #print(zone)
    print(dataframe())

if __name__ == "__main__":
    run()


