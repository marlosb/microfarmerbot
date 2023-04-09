import logging
import os
import time

import pyodbc

def input_or_output(code): 
    '''
    Determine if SQL code inputs data (UPDATE, SET, INSERT, DELETE) 
    or outputs data (SELECT, SHOW)
    '''
    code = code.upper()
    if 'INSERT' in code or 'SET' in code or 'DELETE' in code or 'UPDATE' in code:
        return 'input'
    else:
        return 'output'

def parse_query_results(cursor: pyodbc.Cursor) -> list:
    '''
    Parse query results into a list of dictionaries
    '''
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def input_data(conn: pyodbc.Connection, code: str) -> str:
    '''
    Execute SQL code that inputs data into the database
    '''
    cursor = conn.cursor()
    try:
        cursor.execute(code)
        conn.commit()
        response = 'Dados inseridos com sucesso :)'
    except Exception as e:
        logging.info(f'Error executing SQL code: {e}')
        response = 'Erro ao inserir dados :('
    return response

def query_data(conn: pyodbc.Connection, code: str) -> list[dict]:
    '''
    Execute SQL query that outputs data from the database
    '''
    cursor = conn.cursor()
    try:
        cursor.execute(code)
        response = parse_query_results(cursor)
        logging.info('SQL query executed successfully')
    except Exception as e:
        logging.info(f'Error executing SQL query: {e}')
        response = 'Erro ao executar a query :('
    return response

def execute_sql_code(code):
    ''' 
    Connect to SQL Database, using the connection string from the environment variables
    Execute SQL code and return the result

    params:
        code: str = SQL code to be executed

    returns:
        response: str | list[dict] = result of the SQL code execution
    '''
    conn_string = os.environ['SQL_CONNECTION_STRING']
    try:
        logging.info('Trying to connect to SQL Server')
        conn = pyodbc.connect(conn_string)
    except Exception as e:
        logging.info(f'Error connecting to SQL Server: {e}')
        logging.info('Waiting 30 seconds before trying again')
        time.sleep(30)
        conn = pyodbc.connect(conn_string)

    code_type = input_or_output(code)

    if code_type == 'input':
        logging.info('Executing SQL code')
        response_string = input_data(conn, code)
        flag = True
    else:
        logging.info('Executing SQL query')
        response = query_data(conn, code)
        response_string = ''
        if isinstance(response, str):
            return False, response
        for line in response:
            response_string = response_string + f'{line}\n'
        flag = False
    
    conn.close()
    return flag, response_string