from app.db_connect import connect
from app import db, app

def get_crypto_class():
    conn = connect()
    with conn.cursor() as cur:
        sql = f'SELECT crypto_class_id, crypto_class_name, crypto_percent from crypto_class'
        cur.execute(sql)
        return cur.fetchall()

def delete_crypto_class(crypto_class_id):
    conn = connect()
    with conn.cursor() as cur:
        sql = f'DELETE from crypto_class WHERE crypto_class_id = {crypto_class_id}'
        cur.execute(sql)
        conn.commit()

def get_cryptos(user_id_):
    conn = connect ()
    with conn.cursor() as cur:
        sql = f'SELECT ' \
              f't.crypto_class_id, t.comp_name, ac.crypto_class_id, ' \
              f'ac.crypto_class_name, t.crypto_price, t.crypto_symbol ' \
              f'FROM crypto t JOIN crypto_class ac ON t.crypto_class_id = ac.crypto_class_id ' \
              f'WHERE t.user_id_ = {user_id_}'
        cur.execute (sql)
        return cur.fetchall()

def insert_crypto_class(crypto_class_name, crypto_percent):
    conn = connect()
    with conn.cursor() as cur:
        sql = f'INSERT INTO crypto_class (crypto_class_name, crypto_percent) ' \
              f'VALUES ("{crypto_class_name}", {crypto_percent})'
        cur.execute(sql)
        conn.commit()

def  update_crypto_class(crypto_class_name, crypto_percent, crypto_class_id):
    conn = connect()
    with conn.cursor() as cur:
        sql = f'UPDATE crypto_class ' \
              f'SET crypto_class_name = "{crypto_class_name}", crypto_percent = {crypto_percent} ' \
              f'WHERE crypto_class_id = {crypto_class_id} '
        cur.execute(sql)
        conn.commit()