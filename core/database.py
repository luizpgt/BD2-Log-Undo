import json
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from core.config import settings

def is_list_of_int(item_list):
    for item in item_list:
        if isinstance(item, int):
            return True
    return False


def get_table_metadata():

    file = open(str(settings.IN_METADATA_FILE), 'r')
    data = json.load(file)['table']

    keys = list()
    key_types = list()
    values = list()

    for key, value in data.items():
        keys.append(str(key))
        key_types.append("integer" if is_list_of_int(value) else "varchar(500)")
        values.append(value)

    return keys, key_types, values


def create_tables(cursor, table_metadata):

    keys = table_metadata.keys
    key_types = table_metadata.key_types
    values = table_metadata.values

    sql_create = 'CREATE TABLE t ('

    for i in range(len(keys)):
        sql_create += f'{keys[i]} {key_types[i]} null,'

    sql_create += f'CONSTRAINT pk_t PRIMARY KEY ({keys[0]}));'

    cursor.execute('DROP TABLE IF EXISTS t')
    cursor.execute(sql_create)


def populate_tables(cursor, table_metadata):

    sql_insert_query = f'insert into t({",".join(table_metadata.keys)}) values '
        
    bigger_values_list = (len(max(table_metadata.values, key=len)))

    for i in range(bigger_values_list):
        sql_insert_query += '('
        for j in range(len(table_metadata.values)):
            if len(table_metadata.values[j]) < i + 1 or table_metadata.values[j][i] == None:
                sql_insert_query += f'null,'
            else:
                if table_metadata.key_types[j] == 'integer':
                    sql_insert_query += f'{table_metadata.values[j][i]},'
                else:
                    sql_insert_query += f'\'{table_metadata.values[j][i]}\','
        sql_insert_query = sql_insert_query[:-1] + '),'
    sql_insert_query = sql_insert_query[:-1] + ';'

    cursor.execute(sql_insert_query)


def perform_undos(cursor, trn_list, table_metadata):
    for trn in trn_list:
        cursor.execute(f'''
            UPDATE t SET {trn.column} = {trn.old_v}
            WHERE {table_metadata.keys[0]} = {trn.tuple_id}
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


def print_tables(cursor, table_metadata):
    sql_select = f'SELECT {",".join(table_metadata.keys)} FROM t ORDER BY {table_metadata.keys[0]}'
    cursor.execute(sql_select)

    data_dic = {"t":{}}
    for key in table_metadata.keys:
        data_dic['t'][key] = []

    for record in cursor:
        for i in range(len(table_metadata.keys)):
            data_dic['t'][table_metadata.keys[i]].append(record[i])

    print(json.dumps(data_dic, indent=4))
