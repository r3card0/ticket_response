# libraries
import pandas as pd
import psycopg2 as p2
import os
import datetime
from openpyxl.workbook import workbook
from config import config



def description():
    program_description = """
    This program calculates the total kms of links
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
        SELECT DISTINCT admin_l1_display_name as country
        , admin_l1_rmob_id
        FROM admin_active_ws_{zone}_bw_2201
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
        SELECT distinct a.admin_l1_display_name as country
        , sum((SELECT sum(l.link_length_meters / 1000) FROM link_active_ws_{zone}_bw_2201 l WHERE l.is_navigable=true AND a.admin_rmob_id = l.left_admin_rmob_id AND l.view_start_date between '2022-01-01' AND '2022-08-31')) as km_nav
        , sum((SELECT sum(l.link_length_meters / 1000) FROM link_active_ws_{zone}_bw_2201 l WHERE l.is_navigable=false AND a.admin_rmob_id = l.left_admin_rmob_id AND l.view_start_date between '2022-01-01' AND '2022-08-31')) as km_not_nav
        FROM admin_active_ws_{zone}_bw_2201 a 
        WHERE admin_l1_rmob_id = {country_id} -- Country
        GROUP BY a.admin_l1_display_name
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


