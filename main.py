import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from models.Table import Table
from core.config import dbconfig
from undo.log import get_transaction_list_to_undo
from core.database import create_tables, populate_tables, perform_undos, check_database, print_tables, get_table_metadata


def main():
    conn = None
    try:


        # pegar estrutura da tabela no banco

        #criar banco
        params = dbconfig()

        #criar banco se necessário
        check_database(params.get('user'), params.get('password'), params.get('database'))
        
        # conectar banco        
        conn = psycopg2.connect(**params)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT);

        cursor = conn.cursor()

        # capturar estrutura da tabela com base no json de entrada 
        table_metadata = Table(*get_table_metadata())

        # criar e popular tabelas
        create_tables(cursor, table_metadata)
        populate_tables(cursor, table_metadata)
        
        # performar undos
        perform_undos(cursor, get_transaction_list_to_undo(), table_metadata)

        # exibir estado final da tabela
        print_tables(cursor, table_metadata)

        cursor.close()
    except(Exception) as err:
        print(err)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    main()
