from dotenv import load_dotenv
import os
import yfinance as yf

# Load environment variables from .env file
load_dotenv()

# Access the Alpha Vantage API key
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

if ALPHA_VANTAGE_API_KEY:
    print("Alpha Vantage API key loaded successfully!")
else:
    print("Error: Alpha Vantage API key not found. Please check your .env file.")

# Test Yahoo Finance integration
try:
    # Example: Fetch data for a stock (e.g., AAPL)
    stock = yf.Ticker("AAPL")
    stock_info = stock.info  # Retrieve general stock information
    print("Yahoo Finance API is working!")
    print(f"Company Name: {stock_info['longName']}")
except Exception as e:
    print("Error: Unable to fetch data from Yahoo Finance API.")
    print(e)
