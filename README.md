## Overview
A Dockerized application that automatically extracts stock prices from yfinance every minute, stores them in an SQLite database, and displays them through a Flask-based web interface.

## Features
- Automated 1-minute stock price extraction
- Dockerized environment for consistent deployment
- Scheduled data fetching with cron jobs
- Data storage in SQLite database
- Flask-based back-end for handling HTTP requests
- Simple front-end with HTML and CSS for data display

## Tech Stack
- **Programming Languages**: Python, Bash
- **Database**: SQLite
- **Web Framework**: Flask
- **Containerization**: Docker
- **Scheduling**: Cron
- **Frontend Technologies**: HTML, CSS
  
## Architecture
The project is Dockerized and uses a shell script to initialize the environment. A cron job executes a Python script to fetch stock prices and store them in an SQLite database, ensuring automated updating. Flask handles HTTP requests and interacts with the database, serving a simple front-end built with HTML and CSS.

![image](https://github.com/Thocook/Stock-Price-Extractor/assets/134341575/eaea4528-3c4d-4104-b718-8b2fa4e41a54)


## Usage
- **Port 80**:
  1. Download the repository.
  2. Build the container.
       `docker build -t stock_price_extractor .`
      `docker run -d -p 80:80 stock_price_extractor`
  4. Access the application via a web browser at [http://localhost:80](http://localhost:80).
  5. The stock prices are automatically updated as per the cron job schedule.

## Configuration
- **Cron Job Schedule**: Modify the cron job schedule in the `crontab` file to change the frequency of data fetching.
- **Database**: The SQLite database file is located at `stock_prices.db`.

## Possible Advancements
- Expand the list of tickers to create a bigger database.
- Use a more robust database like PostgreSQL for better scalability.
- Host the container on an online server for consistent availability.

## UI:
![image](https://github.com/Thocook/Stock-Price-Extractor/assets/134341575/5dca5458-e098-4f07-bd6c-9abdd13a0378)
