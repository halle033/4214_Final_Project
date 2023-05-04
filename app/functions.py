from app.db_connect import connect
from app import db, app

def get_asset_class():
    conn = connect()
    with conn.cursor() as cur:
        sql = f'SELECT asset_class_id, asset_class_name, allocation_percent from asset_class'
        cur.execute(sql)
        return cur.fetchall()

def delete_asset_class(asset_class_id):
    conn = connect()
    with conn.cursor() as cur:
        sql = f'DELETE from asset_class WHERE asset_class_id = {asset_class_id}'
        cur.execute(sql)
        conn.commit()

def get_tickers(user_id):
    conn = connect ()
    with conn.cursor() as cur:
        sql = f'SELECT ' \
              f't.ticker_id, t.company_name, ac.asset_class_id, ' \
              f'ac.asset_class_name, t.current_price, t.ticker_symbol ' \
              f'FROM ticker t JOIN asset_class ac ON t.asset_class_id = ac.asset_class_id ' \
              f'WHERE t.user_id = {user_id}'
        cur.execute (sql)
        return cur.fetchall()

def insert_asset_class(asset_class_name, allocation_percent):
    conn = connect()
    with conn.cursor() as cur:
        sql = f'INSERT INTO asset_class (asset_class_name, allocation_percent) ' \
              f'VALUES ("{asset_class_name}", {allocation_percent})'
        cur.execute(sql)
        conn.commit()

def  update_asset_class(asset_class_name, allocation_percent, asset_class_id):
    conn = connect()
    with conn.cursor() as cur:
        sql = f'UPDATE asset_class ' \
              f'SET asset_class_name = "{asset_class_name}", allocation_percent = {allocation_percent} ' \
              f'WHERE asset_class_id = {asset_class_id} '
        cur.execute(sql)
        conn.commit()