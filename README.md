# Yahoo-Finance-Stock-Scraper
This project is a web scraper designed to collect data on companies listed on Nasdaq. The scraper uses Selenium to navigate and extract company names from the Nasdaq screener. The second part of the project leverages the yfinance library to fetch detailed financial information about these companies, including logos, stock prices, and dividend data.

# NASDAQ Stock Data Parser

This project is a simple web scraper for extracting company data from the NASDAQ website and fetching additional financial information using `yfinance`. The script is divided into two main parts:

1. Parsing the list of companies from the NASDAQ screener.
2. Fetching detailed financial data for each company and saving it into an Excel file.

## Features

- Extracts company names from NASDAQ screener.
- Retrieves financial data such as company name, ticker, ex-dividend date, current stock price, lot size, dividend amount per share, and dividend yield percentage.
- Saves the collected data into an Excel file.

## Requirements

- Python 3.x
- Selenium
- BeautifulSoup4
- yfinance
- pandas
- requests

## Installation

Install the required packages using `pip`:

```sh
pip install -r requirements.txt
