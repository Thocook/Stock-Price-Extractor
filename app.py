from flask import Flask, render_template, jsonify
import sqlite3
import os
import time
import yfinance as yf

app = Flask(__name__)

DATABASE = 'stock_prices.db'
TICKERS_FILE = 'tickers.txt'
LONG_NAMES_CACHE = {}

def get_last_download_time():
    log_file = 'stock_price_extractor.log'
    if os.path.exists(log_file):
        return time.ctime(os.path.getmtime(log_file))
    return 'No downloads yet'

def get_stock_data():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    stock_data = {}
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT * FROM '{table_name}' ORDER BY Datetime DESC")
        rows = cursor.fetchall()
        stock_data[table_name] = rows
    conn.close()
    return stock_data

def get_stock_data5(limit=5):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    stock_data = {}
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT * FROM '{table_name}' ORDER BY Datetime DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        stock_data[table_name] = rows
    conn.close()
    return stock_data

def read_tickers_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        tickers = file.read().splitlines()
        print("Tickers read from file:", tickers)  # Debug print statement
    return tickers

def get_ticker_info(ticker):
    if ticker in LONG_NAMES_CACHE:
        return LONG_NAMES_CACHE[ticker]
    stock = yf.Ticker(ticker)
    long_name = stock.info.get('shortName', ticker)
    exchange = stock.info.get('exchange', 'Unknown')
    LONG_NAMES_CACHE[ticker] = {'long_name': long_name, 'exchange': exchange}
    return LONG_NAMES_CACHE[ticker]

def get_table_names_and_long_names():
    tickers = read_tickers_from_file(TICKERS_FILE)
    stock_info = {}
    table_to_long_name = {}
    for ticker in tickers:
        table_name = ticker.replace('.', '_')
        info = get_ticker_info(ticker)
        long_name = info['long_name']
        exchange = info['exchange']
        table_to_long_name[table_name] = long_name
        if exchange not in stock_info:
            stock_info[exchange] = {}
        stock_info[exchange][table_name] = long_name
    return stock_info, table_to_long_name

def get_ticker_data(ticker):
    table_name = ticker.replace('.', '_')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM '{table_name}'")
    rows = cursor.fetchall()
    conn.close()
    return rows

@app.route('/')
def index():
    last_download_time = get_last_download_time()
    stock_data = get_stock_data5()
    stock_info, table_to_long_name = get_table_names_and_long_names()
    return render_template('index.html', last_download_time=last_download_time, 
                           stock_data=stock_data, stock_info=stock_info,  table_to_long_name=table_to_long_name)

@app.route('/api/stock_data')
def stock_data_api():
    stock_data = get_stock_data()
    return jsonify(stock_data)

@app.route('/api/stock_data/<ticker>')
def stock_data_ticker_api(ticker):
    ticker = f'"{ticker}"'
    data = get_ticker_data(ticker)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
