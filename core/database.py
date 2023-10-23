import json
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_tables(cursor):
    cursor.execute('DROP TABLE IF EXISTS t;')

    cursor.execute('''                   
        CREATE TABLE t (
            id integer NOT NULL,
            A integer NOT NULL,
            B integer NOT NULL,
            CONSTRAINT pk_t PRIMARY KEY (id)
        );                   
    ''')

def populate_tables(cursor):
    file = open('input_case/metadata.json', 'r')

    try:        
        data = json.load(file)['table']
        tuples = list( zip(data['id'], data['A'], data['B']) )

        for tuple in tuples:
            tuple = [str(column) for column in tuple]
            values = ', '.join(tuple)
            insert_query = 'INSERT INTO t(id, a, b) VALUES (' + values + ');'
            cursor.execute(insert_query)

    finally:
        file.close()

def perform_undos(cursor, trn_list):
    for trn in trn_list:
        item = str(trn).replace('<', '').replace('>', '').split('|')
        col = item[2]
        value = item[3]
        id = item[1]
        cursor.execute(f'''
            UPDATE t SET {col} = {value}
            WHERE id = {id}
        ''')

def check_database(user, password, dbname):
    try:
        conn = psycopg2.connect(f'user={user} password={password}')
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT);
        cursor = conn.cursor()
        cursor.execute(f'''
            SELECT 'CREATE DATABASE {dbname}'
            WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '{dbname}')        
        ''')   
        db = cursor.fetchone();
        if db:
            cursor.execute(db[0])
    except(Exception) as err:
      print('check_database err -> ' + str(err))
    finally:
      if conn:
        cursor.close()
        conn.close()

    