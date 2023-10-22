import psycopg2
from core.dbconf import dbconfig
from core.database import create_tables, populate_tables, perform_undos
from undo.log import get_transaction_list_to_undo

def main():
    conn = None
    try:
        # conectar banco
        params = dbconfig()
        conn = psycopg2.connect(**params);
        cursor = conn.cursor()

        # criar e popular tabelas
        create_tables(cursor)
        populate_tables(cursor)
        
        # undos
        perform_undos(cursor, get_transaction_list_to_undo())
    except:
        print('An exception occurred')

    finally:
        if conn is not None:
            conn.close()