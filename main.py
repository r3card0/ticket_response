# import libraries
import pandas as pd
import psycopg2 as p2
import os
import datetime
from openpyxl.workbook import workbook
from config import config

# jira number
def ticket_number():
    number = int(input('Enter the number of the ticket: '))
    return number

ticket_number = ticket_number()

# connection
def connectdb():
    params = config()
    connection = p2.connect(**params)
    
    return connection

cur = connectdb().cursor()

connection = connectdb()

# sql select statement
def sql_statement():
    try:
        select = """
        SELECT columns
        FROM table 1  
        JOIN table 2 ON 2.id = 1.id
        ORDER BY 1,2
        """
        return select 

    except TypeError:
        print('There is not sql statement, please paste one')

select = sql_statement()

# create and visualize data frame
df = pd.read_sql_query(select,connection)

# directory to export output
os.chdir(r"/mnt/c/sql/spool")

# choose a format, select 1 to csv format or 2 to excel format
def choose_format():
    menu = int(input("""
    Choose a format option:
    csv format   (1)
    xlsx fortmat (2)

    Choose an option:  """))

    if menu == 1:
        df.to_csv(f'OPSDBE_MINER-{ticket_number}_' + datetime.datetime.now().strftime('%d-%b-%Y') +'.csv', index=False)
    elif menu == 2:
        df.to_excel(f'OPSDBE_MINER-{ticket_number}_' + datetime.datetime.now().strftime('%d-%b-%Y') +'.xlsx', index=False)
    else:
        print('Choose a correct option')

def run():
    choose_format()
    print('Your file is ready!!')

if __name__ == '__main__':
    run()
