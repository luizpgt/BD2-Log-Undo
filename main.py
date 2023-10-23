import psycopg2
from core.dbconf import dbconfig
from core.database import create_tables, populate_tables, perform_undos, check_database
from undo.log import get_transaction_list_to_undo

def main():
    conn = None
    try:
        #criar banco
        print('teste')
        params = dbconfig()

        #criar banco se necessário
        check_database(params.get('user'), params.get('password'), params.get('database'))
        
        # conectar banco        
        conn = psycopg2.connect(**params)
        cursor = conn.cursor()

        print('teste2')
        # criar e popular tabelas
        create_tables(cursor)
        populate_tables(cursor)
        
        # undos
        print('teste3')
        perform_undos(cursor, get_transaction_list_to_undo())
    except(Exception) as err:
        print(err)

    finally:
        if conn:
            cursor.close()
            conn.close()

main()