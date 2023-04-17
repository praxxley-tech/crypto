# Crypto Technical Analysis

This Python script performs technical analysis on cryptocurrencies using data from the CoinGecko API. The purpose of the analysis is to identify investment-worthy cryptocurrencies based on specific technical indicators.


## Requirements
- Python 3.8 or higher
- Pandas
- TA-Lib
- Requests
- tqdm

## Usage

```
cd existing_repo
git remote add origin https://github.com/praxxley-tech/crypto.git
git branch -M main
git push -uf origin main
```
Run the script with:
```
python crypto.py
```
The script will analyze all cryptocurrencies listed on CoinGecko and identify the ones that meet the investment criteria based on the following technical indicators:

- Relative Strength Index (RSI)
- Moving Average Convergence Divergence (MACD)
- Bollinger Bands

A cryptocurrency is considered investment-worthy if its RSI is below 30 and its MACD is greater than its MACD signal.

## Output
The script prints the investment-worthy cryptocurrencies and their respective technical indicators:

- RSI
- MACD
- MACD Signal
- Bollinger Lower Band
- Bollinger Upper Band
- The results are also saved to a CSV file named "investment_worthy_crypto.csv" for future reference.

## Functions
The script contains several functions that perform different tasks:

- **get_all_crypto_data()**: Retrieves a list of all cryptocurrencies from the CoinGecko API.
- **save_data_to_csv(data, filename)**: Saves the data to a CSV file.
- **load_data_from_csv(filename)**: Loads data from a CSV file.
- **get_historical_data(coin_id, days=180)**: Retrieves historical price data for a specific cryptocurrency.
- **calculate_technical_indicators(dataframe)**: Calculates various technical indicators using the TA-Lib library.
- **technical_analysis(coin_id)**: Performs technical analysis on a specific cryptocurrency and returns its technical indicators.
- **is_investment_worthy(indicators)**: Determines if a cryptocurrency is investment-worthy based on its technical indicators.

## Progress Bar
The script uses the **tqdm** library to display a progress bar while analyzing the cryptocurrencies. The progress bar provides a visual indication of the script's progress and an estimate of the time remaining.
