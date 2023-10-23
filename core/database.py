import json
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from core.config import settings

def create_tables(cursor):
    cursor.execute('DROP TABLE IF EXISTS t')
    cursor.execute('''                   
        CREATE TABLE t (
            id integer NOT NULL,
            A integer NOT NULL,
            B integer NOT NULL,
            CONSTRAINT pk_t PRIMARY KEY (id)
        )                   
    ''')

def populate_tables(cursor):
    file = open(str(settings.IN_METADATA_FILE), 'r')

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
        cursor.execute(f'''
            UPDATE t SET {trn.column} = {trn.old_v}
            WHERE id = {trn.tuple_id}
        ''')

def check_database(user, password, dbname):
    conn = None
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
        cursor.close()
    except(Exception) as err:
      print('check_database err -> ' + str(err))
    finally:
      if conn:
        conn.close()

def print_tables(cursor):
    cursor.execute('SELECT id, A, B FROM t ORDER BY id')
    data_dic = {
        "t": {
            "id": [],
            "A": [],
            "B": []
        }
    }
    for record in cursor:
        id, A, B = record
        data_dic['t']['id'].append(id)
        data_dic['t']['A'].append(A)
        data_dic['t']['B'].append(B)
    print(json.dumps(data_dic, indent=4))
