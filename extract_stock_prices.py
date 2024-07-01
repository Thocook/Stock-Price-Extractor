import yfinance as yf
import pandas as pd
from datetime import datetime
import logging
import sqlite3
import os
from time import sleep

# Set up logging
logging.basicConfig(filename='stock_price_extractor.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def read_tickers(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        tickers = file.read().splitlines()
        print("Tickers read from file:", tickers)  # Debug print statement
    return tickers

def fetch_stock_data(symbol, retries=3):
    for attempt in range(retries):
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period="5d", interval="1m")
            if hist.empty:
                raise ValueError(f"No historical data found for {symbol}")
            return hist
        except Exception as e:
            logging.error(f"Attempt {attempt+1} failed for {symbol}: {e}")
            sleep(2)  # Wait for a bit before retrying
    raise ValueError(f"Failed to fetch data for {symbol} after {retries} attempts")

def extract_and_store_stock_prices(stock_symbols, db_name):
    try:
        conn = sqlite3.connect(db_name)
        for symbol in stock_symbols:
            try:
                print(symbol)
                hist = fetch_stock_data(symbol)
                hist.reset_index(inplace=True)
                hist['Datetime'] = hist['Datetime'].astype(str)  # Convert datetime to string for SQLite compatibility
                print(hist.head())

                # Escape table name
                table_name = f'"{symbol.replace(".", "_")}"'  # Replace dot in symbol for SQLite table name compatibility

                # Check if table exists
                cursor = conn.cursor()
                cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name={table_name};")
                if cursor.fetchone():
                    # Append new data
                    existing_data = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
                    new_data = hist[~hist['Datetime'].isin(existing_data['Datetime'])]
                    combined_data = pd.concat([existing_data, new_data]).reset_index(drop=True)
                    combined_data.to_sql(table_name, conn, if_exists='replace', index=False)
                else:
                    # Create new table
                    hist.to_sql(table_name, conn, if_exists='replace', index=False)

                logging.info(f"Data for {symbol} extracted and saved to database table {table_name}.")
                print(f"Data for {symbol} extracted and saved to database table {table_name}.")
            except Exception as e:
                logging.error(f"Failed to process {symbol}: {e}")
        
        conn.close()
        logging.info("All data extracted and saved successfully.")
    except Exception as e:
        logging.error(f"Failed to extract stock prices: {str(e)}")

if __name__ == "__main__":
    print("Extracting stock prices...")
    ticker_file = 'tickers.txt'
    db_name = 'stock_prices.db'
    stock_symbols = read_tickers(ticker_file)
    extract_and_store_stock_prices(stock_symbols, db_name)
