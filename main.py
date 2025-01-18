# Purpose:
# Entry point to tie everything together.

from data_fetcher import data_fetcher

fetcher = data_fetcher("Alpha Vantage", "your_alpha_vantage_api_key")

# Fetch stock data
print("Fetching stock data...")
print(fetcher.fetch_stock_data("AAPL", "price"))

# Fetch historical prices
print("\nFetching historical prices...")
print(fetcher.fetch_historical_prices("AAPL", "2023-01-01", "2023-12-31"))

# Fetch dividend data
print("\nFetching dividend data...")
print(fetcher.fetch_dividend_data("AAPL"))

# Validate ticker
print("\nValidating ticker...")
print(fetcher.validate_ticker("AAPL"))

# Handle rate limit
print("\nHandling rate limit (simulation)...")
fetcher.handle_rate_limit()

# Switch provider to Yahoo Finance
print("\nSwitching provider to Yahoo Finance...")
fetcher.switch_provider("Yahoo Finance", "")
print("Switched to provider: Yahoo Finance")

# Fetch sentiment data
print("\nFetching sentiment data...")
print(fetcher.fetch_sentiment_data("AAPL"))
