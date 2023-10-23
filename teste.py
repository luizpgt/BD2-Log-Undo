import psycopg2
user = 'postgres'
password = 'postgres'
conn = psycopg2.connect(f'user={user} password={password}')
cursor = conn.cursor()
cursor.execute('''
    SELECT 'CREATE DATABASE undolog_db'
    WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'undolog_db')        
''')    

