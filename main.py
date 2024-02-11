import psycopg2
from psycopg2.sql import SQL, Identifier
def create_db(conn):
    with conn.cursor() as cur:
        cur.execute('DROP TABLE phones;'
                    'DROP TABLE clients;')
        cur.execute('CREATE TABLE IF NOT EXISTS clients('
                    'id SERIAL PRIMARY KEY,'
                    'first_name VARCHAR(60) NOT NULL,'
                    'last_name VARCHAR(60) NOT NULL,'
                    'email VARCHAR(60) NOT NULL);')
        cur.execute('CREATE TABLE IF NOT EXISTS phones('
                    'id SERIAL PRIMARY KEY,'
                    'client_id INTEGER REFERENCES clients(id),'
                    'phone_number VARCHAR(12));')
        conn.commit()
def add_client(conn, first_name, last_name, email, phones=None):
    with conn.cursor() as cur:
        cur.execute('INSERT INTO clients (first_name, last_name, email)'
                    'VALUES (%s, %s, %s)'
                    'RETURNING id, first_name, last_name, email;', (first_name, last_name, email))
        print(cur.fetchone())
def add_phone(conn, client_id, phone_number):
    with conn.cursor() as cur:
        cur.execute('INSERT INTO phones (phone_number)'
                    'VALUES (%s)'
                    'RETURNING id, phone_number, client_id;', (phone_number,))
        print(cur.fetchone())
def change_client(conn, id, first_name=None, last_name=None, email=None):
    with conn.cursor() as cur:
        if first_name != None:
            cur.execute('UPDATE clients '
                        'SET first_name=%s '
                        'WHERE id=%s'
                        'RETURNING first_name, last_name, email;', (first_name, id))
        if last_name != None:
            cur.execute('UPDATE clients '
                        'SET last_name=%s '
                        'WHERE id=%s'
                        'RETURNING first_name, last_name, email;', (last_name, id))
        if email != None:
            cur.execute('UPDATE clients '
                        'SET email=%s '
                        'WHERE id=%s'
                        'RETURNING first_name, last_name, email;', (email, id))
            return cur.fetchone()
def delete_phone(conn, client_id, phone_number):
    with conn.cursor() as cur:
        cur.execute('DELETE FROM phones WHERE phone_number=%s;', (phone_number,))
        conn.commit()
def delete_client(conn, id):
    with conn.cursor() as cur:
        cur.execute('DELETE FROM phones WHERE client_id=%s;', (id,))
        cur.execute('DELETE FROM clients WHERE id=%s;', (id,))
        conn.commit()
def find_client(conn, first_name=None, last_name=None, email=None, phone_number=None):
    with conn.cursor() as cur:
        if first_name != None:
            cur.execute('SELECT clients.first_name, clients.last_name, clients.email, phones.phone_number From clients '
                        'LEFT JOIN phones ON clients.id = phones.id '
                        'WHERE clients.first_name=%s;',
                        (first_name, ))
            return cur.fetchone()
        if last_name != None:
            cur.execute('SELECT clients.first_name, clients.last_name, clients.email, phones.phone_number From clients '
                        'LEFT JOIN phones ON clients.id = phones.id '
                        'WHERE clients.last_name=%s;',
                        (last_name, ))
            return cur.fetchone()
        if email != None:
            cur.execute('SELECT clients.first_name, clients.last_name, clients.email, phones.phone_number From clients '
                        'LEFT JOIN phones ON clients.id = phones.id '
                        'WHERE clients.email=%s;',
                        (email, ))
            return cur.fetchone()
        if phone_number != None:
            cur.execute('SELECT clients.first_name, clients.last_name, clients.email, phones.phone_number From clients '
                        'LEFT JOIN phones ON clients.id = phones.id '
                        'WHERE phones.phone_number=%s;',
                        (phone_number, ))
            return cur.fetchone()

if __name__ == '__main__':
    with psycopg2.connect(database='clients_db', user='postgres', password='djokerdjek') as conn:
        print(create_db(conn))
        print(add_client(conn, 'Иван', 'Иванов', 'ivanov@mail.ru'))
        print(add_client(conn, 'Петр', 'Петров', 'petrov@gmail.com'))
        print(add_client(conn, 'Вася', 'Ложкин', 'vasia@gmail.com'))
        print(add_phone(conn, '1', '+79685784532'))
        print(add_phone(conn, '2', '+79685784534'))
        print(add_phone(conn, '3', '+79685784536'))
        print(delete_phone(conn, '3', '+79685784536'))
        print(change_client(conn,'3','Сидр', 'Сидоров', 'sidor_sidorov@mail.ru'))
        print(change_client(conn, '3', 'Кадр', None,'mail@mail.ru'))
        print(find_client(conn, 'Не-Иван', 'Иванов', 'ivanov@mail.ru'))
        print(find_client(conn, 'Петр', None, None))
        print(find_client(conn, None, 'Петров', None))
        print(find_client(conn, None, None, 'ivanov@mail.ru'))



