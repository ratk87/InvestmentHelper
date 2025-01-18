# Purpose:
# Fetches updated figures from APIs.

import requests  # For making HTTP requests
import json      # For handling API responses
from datetime import datetime  # For handling date-related operations

class data_fetcher:

    # Attributes
    api_key : str # Stores the API key for accessing financial data
    base_url : str # The base URL of the financial data provider
    headers : dict # Optional API headers (HTTP)
    rate_limit : int # Tracking the number of API calls made to avoid exceeding any limits
    supported_providers : list # List of supported financial data providers

    # Attributes

    def __init__(self, provider, api_key):
        """
               Initializes the DataFetcher with the provider's details and API key.

               :param provider: The name of the data provider (e.g., "Alpha Vantage").
               :param api_key: The API key for authentication.
               """
        self.provider = provider
        self.api_key = api_key
        self.base_url = self.get_base_url(provider)
        self.headers = {"Content-Type": "application/json"}
        self.rate_limit = 0
        self.supported_providers = ["Alpha Vantage", "Yahoo Finance"]

    def get_base_url(self, provider: str) -> str:
        """
        Returns the base URL for the specified provider.

        :param provider: The name of the data provider.
        :return: Base URL for the API.
        """
        if provider == "Alpha Vantage":
            return "https://www.alphavantage.co/query"
        elif provider == "Yahoo Finance":
            return "https://query1.finance.yahoo.com/v8/finance/chart"
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    # Methods

    def fetch_stock_data(self, ticker: str, data_type: str) -> dict:
        """
                Fetches current stock data, such as price, fundamentals, or dividends.

                :param ticker: Stock ticker symbol (e.g., "AAPL").
                :param data_type: The type of data to fetch (e.g., "price", "fundamentals").
                :return: A dictionary containing the fetched data.
                """
        try:
            if self.provider == "Alpha Vantage":
                function = "TIME_SERIES_INTRADAY" if data_type == "price" else "OVERVIEW"
                params = {
                    "function": function,
                    "symbol": ticker,
                    "apikey": self.api_key,
                    "interval": "5min" if data_type == "price" else None,
                }
                response = requests.get(self.base_url, params=params)
                response.raise_for_status()
                data = response.json()

                # Extract latest stock price if data_type is "price"
                if data_type == "price":
                    time_series = data.get("Time Series (5min)", {})
                    latest_timestamp = max(time_series.keys())
                    latest_data = time_series[latest_timestamp]
                    return {
                        "timestamp": latest_timestamp,
                        "open": latest_data["1. open"],
                        "high": latest_data["2. high"],
                        "low": latest_data["3. low"],
                        "close": latest_data["4. close"],
                        "volume": latest_data["5. volume"],
                    }

                return data
            else:
                raise ValueError("Unsupported provider for fetch_stock_data")
        except Exception as e:
            print(f"Error in fetch_stock_data: {e}")
            return {}

    def fetch_historical_prices(self, ticker: str, start_date: str, end_date: str) -> dict:
        """
        Fetches historical price data for a given stock ticker within a specified date range.

        :param ticker: Stock ticker symbol (e.g., "AAPL").
        :param start_date: Start date for historical data (YYYY-MM-DD).
        :param end_date: End date for historical data (YYYY-MM-DD).
        :return: A dictionary with historical price data (date, open, high, low, close, volume).
        """

        def fetch_historical_prices(self, ticker: str, start_date: str, end_date: str) -> dict:
            try:
                if self.provider == "Yahoo Finance":
                    start_timestamp = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())
                    end_timestamp = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp())
                    url = f"{self.base_url}/{ticker}"
                    params = {
                        "symbol": ticker,
                        "period1": start_timestamp,
                        "period2": end_timestamp,
                        "interval": "1d",
                    }
                    response = requests.get(url, params=params)
                    response.raise_for_status()
                    data = response.json()

                    # Process the Yahoo Finance data
                    chart_data = data.get("chart", {}).get("result", [])[0]
                    if not chart_data:
                        raise ValueError("No historical data available for the given ticker and date range.")

                    historical_prices = chart_data.get("indicators", {}).get("quote", [{}])[0]
                    dates = chart_data.get("timestamp", [])
                    result = {}
                    for i, timestamp in enumerate(dates):
                        date_str = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")
                        result[date_str] = {
                            "open": historical_prices.get("open", [])[i],
                            "high": historical_prices.get("high", [])[i],
                            "low": historical_prices.get("low", [])[i],
                            "close": historical_prices.get("close", [])[i],
                            "volume": historical_prices.get("volume", [])[i],
                        }

                    return result
                else:
                    raise ValueError("Unsupported provider for fetch_historical_prices")
            except Exception as e:
                print(f"Error in fetch_historical_prices: {e}")
                return {}

    def fetch_dividend_data(self, ticker: str) -> dict:
        """
        Retrieves dividend payout history for a given stock ticker.

        :param ticker: Stock ticker symbol (e.g., "AAPL").
        :return: A dictionary containing dividend history (dates and amounts).
        """

        def fetch_dividend_data(self, ticker: str) -> dict:
            try:
                if self.provider == "Alpha Vantage":
                    params = {
                        "function": "TIME_SERIES_MONTHLY_ADJUSTED",
                        "symbol": ticker,
                        "apikey": self.api_key,
                    }
                    response = requests.get(self.base_url, params=params)
                    response.raise_for_status()
                    data = response.json()

                    # Extract dividend history
                    monthly_adjusted = data.get("Monthly Adjusted Time Series", {})
                    dividends = {
                        date: details["7. dividend amount"]
                        for date, details in monthly_adjusted.items()
                        if float(details["7. dividend amount"]) > 0
                    }

                    return dividends
                else:
                    raise ValueError("Unsupported provider for fetch_dividend_data")
            except Exception as e:
                print(f"Error in fetch_dividend_data: {e}")
                return {}

    def store_to_database(self, data: dict, table_name: str):
        """
        Stores the fetched data into the database.

        :param data: A dictionary of data fetched from the API.
        :param table_name: The name of the database table to store the data.
        """
        try:
            if hasattr(self, "database"):
                self.database.insert(table_name, data)
                print(f"Data successfully stored in table '{table_name}'.")
            else:
                print("Database instance not found. Please initialize it.")
        except Exception as e:
            print(f"Error storing data to database: {e}")

    def validate_ticker(self, ticker: str) -> bool:
        """
        Validates the format and existence of a ticker symbol using the provider's API.

        :param ticker: Stock ticker symbol (e.g., "AAPL").
        :return: True if the ticker is valid, False otherwise.
        """
        try:
            if self.provider == "Alpha Vantage":
                params = {
                    "function": "SYMBOL_SEARCH",
                    "keywords": ticker,
                    "apikey": self.api_key,
                }
                response = requests.get(self.base_url, params=params)
                response.raise_for_status()
                data = response.json()
                matches = data.get("bestMatches", [])
                return any(match["1. symbol"] == ticker for match in matches)
            elif self.provider == "Yahoo Finance":
                url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
                response = requests.get(url)
                return response.status_code == 200
            else:
                raise ValueError("Unsupported provider for validate_ticker")
        except Exception as e:
            print(f"Error validating ticker: {e}")
            return False

    def handle_rate_limit(self):
        """
        Handles rate limiting by introducing delays when the limit is reached.
        """
        self.rate_limit += 1
        if self.rate_limit >= 5:  # Example: Limit of 5 API calls
            print("Rate limit reached. Sleeping for 60 seconds...")
            import time
            time.sleep(60)
            self.rate_limit = 0

    def switch_provider(self, provider: str, api_key: str):
        """
        Switches to a different financial data provider.

        :param provider: The new provider to switch to.
        :param api_key: The API key for the new provider.
        """
        if provider in self.supported_providers:
            self.provider = provider
            self.api_key = api_key
            self.base_url = self.get_base_url(provider)
            self.rate_limit = 0
            print(f"Switched to provider: {provider}")
        else:
            print(f"Provider '{provider}' is not supported.")

    def fetch_sentiment_data(self, ticker: str) -> dict:
        """
        Fetches sentiment data related to a stock ticker.

        :param ticker: Stock ticker symbol (e.g., "AAPL").
        :return: A dictionary of sentiment data (positive, negative, neutral).
        """
        # For simplicity, this returns dummy data.
        try:
            # Dummy data - Replace this with actual scraping or API integration
            sentiment_data = {
                "positive": 70,
                "negative": 20,
                "neutral": 10,
            }
            return sentiment_data
        except Exception as e:
            print(f"Error fetching sentiment data: {e}")
            return {}


