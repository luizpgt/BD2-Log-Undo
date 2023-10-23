import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from core.config import dbconfig
from core.database import create_tables, populate_tables, perform_undos, check_database, print_tables
from undo.log import get_transaction_list_to_undo

def main():
    conn = None
    try:
        #criar banco
        params = dbconfig()

        #criar banco se necessário
        check_database(params.get('user'), params.get('password'), params.get('database'))
        
        # conectar banco        
        conn = psycopg2.connect(**params)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT);

        cursor = conn.cursor()

        # criar e popular tabelas
        create_tables(cursor)
        populate_tables(cursor)
        
        # performar undos
        perform_undos(cursor, get_transaction_list_to_undo())

        # exibir estado final da tabela
        print_tables(cursor)

        cursor.close()
    except(Exception) as err:
        print(err)
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
  main()
