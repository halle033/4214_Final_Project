from app.db_connect import connect
import yfinance as yf
# note that yf is an alias

# get the tickers from the ticker table
def get_tickers():
    conn = connect()
    with conn.cursor() as cur:
        cur.execute("SELECT ticker_symbol FROM ticker")
        return cur.fetchall()

def get_stock_price(symbol):
   ticker_yahoo = yf.Ticker(symbol)
   data = ticker_yahoo.history()
   last_quote = (data.tail(1)['Close'].iloc[0])
   return last_quote

def update_price(price, symbol):
    conn = connect()
    cur = conn.cursor()
    sql = f"UPDATE ticker SET current_price = {price} WHERE ticker_symbol LIKE '{symbol}'"
    try:
        cur.execute(sql)
        conn.commit()
    except:
        print("Didn't work")

def post_ticker_prices():
    tickers = get_tickers()
    for ticker in tickers:
        symbol = ticker['ticker_symbol']
        price = get_stock_price(ticker['ticker_symbol'])

        update_price(price, symbol)