from app.db_connect import connect
import yfinance as yf
# note that yf is an alias

# get the crypto from the crypto table
def get_crypto():
    conn = connect()
    with conn.cursor() as cur:
        cur.execute("SELECT crypto_symbol FROM crypto")
        return cur.fetchall()

def get_stock_price(symbol):
   crypto_yahoo = yf.Ticker(symbol.replace('$', ''))
   data = crypto_yahoo.history()
   print(data.tail(1)['Close'])
   last_quote = (data.tail(1)['Close'].iloc[0])
   return last_quote

def update_price(price, symbol):
    conn = connect()
    cur = conn.cursor()
    sql = f"UPDATE crypto SET crypto_price = {price} WHERE crypto_symbol LIKE '{symbol}'"
    try:
        cur.execute(sql)
        conn.commit()
    except:
        print("Didn't work")

def post_crypto_prices():
    crypto = get_crypto()
    for crypto in crypto:
        symbol = crypto['crypto_symbol']
        price = get_stock_price(crypto['crypto_symbol'])

        update_price(price, symbol)