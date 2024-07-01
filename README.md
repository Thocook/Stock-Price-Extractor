Overview
A Dockerized application that automatically extracts stock prices every minute, stores them in an SQLite database, and displays them through a Flask-based web interface.

Features
Automated 1-minute stock price extraction
Dockerized environment for consistent deployment
Scheduled data fetching with cron jobs
Data storage in SQLite database
Flask-based back-end for handling HTTP requests
Simple front-end with HTML and CSS for data display
Technologies Used
Python
SQLite
Docker
Bash
HTML
CSS
Architecture
The project is Dockerized and uses a shell script to initialize the environment. A cron job executes a Python script to fetch stock prices and store them in an SQLite database, ensuring automated updating. Flask handles HTTP requests and interacts with the database, serving a simple front-end built with HTML and CSS.
![image](https://github.com/Thocook/Stock-Price-Extractor/assets/134341575/eaea4528-3c4d-4104-b718-8b2fa4e41a54)

Usage
Port 80:
Download the repository.
Build the container.
Access the application via a web browser at http://localhost:80.
The stock prices are automatically updated as per the cron job schedule.
Configuration
Cron Job Schedule: Modify the cron job schedule in the crontab file to change the frequency of data fetching.
Database: The SQLite database file is located at stock_prices.db.
Ways to Improve
Expand the list of tickers to create a bigger database.
Use a more robust database like PostgreSQL for better scalability.
Host the container on an online server for consistent availability.
