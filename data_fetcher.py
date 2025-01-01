# Purpose:
# Fetches updated figures from APIs.

class data_fetcher:

    # Attributes
    api_key : str # Stores the API key for accessing financial data
    base_url : str # The base URL of the financial data provider
    headers : dict # Optional API headers (HTTP)
    rate_limit : int # Tracking the number of API calls made to avoid exceeding any limits
    supported_providers : list # List of supported financial data providers

    # Methods

    def __init__(self, provider, api_key):
        # Initializes the data fetcher with the providers details and API key

    def fetch_stock_data(selfself, ticker: str, data_type: str) -> dict:
        # Makes an API call to fetch the requested data for the given ticker
        # ticker = stock ticker symbol
        # data_type = The type of data to fetch, such as "price", "fundamentals", "dividends")
        # Returns a dictionary containing the fetched data

    def fetch_historical_prices(self, ticker: str, start_date: str, end_date: str) -> dict:
        # Fetches historical price data for the given ticker within the specified date range
        # ticker = stock ticker symbol
        # start_date: start date for the historical data (YYYY-MM-DD)
        # end_date: end date for historical data (YYYY-MM-DD)
        # Returns a dictionary with historical price data (date, open, high, low, close, volume)

    def fetch_dividend_data(self, ticker:str) -> dict:
        # Retrieves dividend payout history for any given stock
        # ticker = stock ticker symbol
        # Returns a dictionary containing dividend history (dates and amounts).

    def store_to_database(self, data: dict, table_name: str):
        # Stores the fetched data into the Database class
        # data = a dictionary of data fetched from the API
        # table_name = the name of the database table to store teh data

    def validate_ticker(self, ticker:str) -> bool:
        # Checks the format and existence of a ticker symbol using the providers API
        # ticker = stock ticker symbol
        # Returns TRUE if the ticker is valid, FALSE otherwise

    def handle_rate_limit(self):
        # Checks if the rate limit has been reached

    def switch_provider(self, provider: str, api_key: str):
        # Allows switching to a different financial data provider if needed
        # provider = the new provider to switch to
        # api_key = the API key of the new provider

    def fetch_sentiment_data(self, ticker: str) -> dict:
        # Scrapes or uses APIs to fetch sentiment data related to the ticker
        # ticker = the stock ticker symbol
        # Returns a dictionary of sentiment data (positive, negative, neutral) derived from news or social media.

