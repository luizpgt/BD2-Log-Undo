import json
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
    file = open('input_case/metadado.json', 'r')

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

            