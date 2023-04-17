import requests
import pandas as pd
from ta import add_all_ta_features
from ta.utils import dropna
from datetime import datetime
import os
from tqdm import tqdm

def get_script_directory():
    return os.path.dirname(os.path.abspath(__file__))

def get_csv_path(filename):
    return os.path.join(get_script_directory(), filename)

def save_data_to_csv(data, filename):
    data.to_csv(filename, index=False)

def load_data_from_csv(filename):
    return pd.read_csv(filename)

csv_path = get_csv_path("investment_worthy_crypto.csv")
if os.path.exists(csv_path):
    investment_worthy_crypto = load_data_from_csv(csv_path).to_dict("records")
else:
    investment_worthy_crypto = []

def get_all_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/list"
    response = requests.get(url)
    data = response.json()

    crypto_data = []
    for item in data:
        try:
            crypto_data.append({
                "id": item["id"],
                "symbol": item["symbol"],
                "name": item["name"],
            })
        except TypeError:
            continue

    return crypto_data

def get_historical_data(coin_id, days=180):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days={days}&interval=daily"
    response = requests.get(url)
    data = response.json()

    if "prices" not in data:
        return None

    prices = data["prices"]
    timestamps, price_data = zip(*prices)

    df = pd.DataFrame({"timestamp": timestamps, "price": price_data})
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df

def calculate_technical_indicators(dataframe):
    dataframe["low"] = dataframe["price"]
    dataframe["high"] = dataframe["price"]
    dataframe["close"] = dataframe["price"]
    dataframe["volume"] = 0
    dataframe = dropna(dataframe)
    
    if len(dataframe) < 2:
        return None

    dataframe = add_all_ta_features(dataframe, "timestamp", "high", "low", "close", "volume")
    return dataframe

def technical_analysis(coin_id):
    historical_data = get_historical_data(coin_id)
    
    if historical_data is None:
        return None

    historical_data = calculate_technical_indicators(historical_data)
    
    if historical_data is None:
        return None

    latest_data = historical_data.iloc[-1]

    rsi = latest_data["momentum_rsi"]
    macd = latest_data["trend_macd"]
    macd_signal = latest_data["trend_macd_signal"]
    bollinger_lband = latest_data["volatility_bbl"]
    bollinger_hband = latest_data["volatility_bbh"]
    stochastic_k = latest_data["momentum_stoch"]
    stochastic_d = latest_data["momentum_stoch_signal"]
    bollinger_bandwidth = latest_data["volatility_bbw"]

    return {
        "rsi": rsi,
        "macd": macd,
        "macd_signal": macd_signal,
        "bollinger_lband": bollinger_lband,
        "bollinger_hband": bollinger_hband,
        "stochastic_k": stochastic_k,
        "stochastic_d": stochastic_d,
        "bollinger_bandwidth": bollinger_bandwidth
    }

def get_indicators_score(indicators):
    rsi_score = max(0, 100 - indicators["rsi"]) / 100
    macd_score = max(0, (indicators["macd"] - indicators["macd_signal"]) / indicators["macd_signal"]) if indicators["macd_signal"] != 0 else 0
    stochastic_score = max(0, (indicators["stochastic_k"] - indicators["stochastic_d"]) / indicators["stochastic_d"]) if indicators["stochastic_d"] != 0 else 0
    bollinger_score = max(0, (indicators["bollinger_hband"] - indicators["price"]) / (indicators["bollinger_hband"] - indicators["bollinger_lband"])) if (indicators["bollinger_hband"] - indicators["bollinger_lband"]) != 0 else 0

    total_score = rsi_score + macd_score + stochastic_score + bollinger_score
    return total_score

all_crypto = get_all_crypto_data()
crypto_strengths = []

for i, crypto in enumerate(tqdm(all_crypto, desc="Analyzing cryptocurrencies")):
    print(f"Processing crypto {i + 1}/{len(all_crypto)}: {crypto['name']} ({crypto['symbol']})")
    indicators = technical_analysis(crypto["id"])
    if indicators is not None:
        indicators["price"] = get_historical_data(crypto["id"]).iloc[-1]["price"]
        total_score = get_indicators_score(indicators)
        crypto_strengths.append({
            "name": crypto["name"],
            "symbol": crypto["symbol"],
            "indicators": indicators,
            "total_score": total_score
        })

def calculate_moving_averages(dataframe):
    dataframe["sma_50"] = dataframe["price"].rolling(window=50).mean()
    dataframe["sma_200"] = dataframe["price"].rolling(window=200).mean()
    return dataframe

def moving_average_analysis(coin_id):
    historical_data = get_historical_data(coin_id)
    
    if historical_data is None:
        return None

    historical_data = calculate_moving_averages(historical_data)
    latest_data = historical_data.iloc[-1]

    sma_50 = latest_data["sma_50"]
    sma_200 = latest_data["sma_200"]

    return {
        "sma_50": sma_50,
        "sma_200": sma_200,
    }

all_crypto = get_all_crypto_data()
crypto_strengths = []

for crypto in tqdm(all_crypto, desc="Analyzing cryptocurrencies"):
    indicators = technical_analysis(crypto["id"])
    if indicators is not None:
        indicators["price"] = get_historical_data(crypto["id"]).iloc[-1]["price"]
        total_score = get_indicators_score(indicators)
        moving_averages = moving_average_analysis(crypto["id"])
        if moving_averages is not None:
            future_trend = "Positive" if moving_averages["sma_50"] > moving_averages["sma_200"] else "Negative"
        else:
            future_trend = "Unknown"
        crypto_strengths.append({
            "name": crypto["name"],
            "symbol": crypto["symbol"],
            "indicators": indicators,
            "total_score": total_score,
            "moving_averages": moving_averages,
            "future_trend": future_trend
        })

crypto_strengths = sorted(crypto_strengths, key=lambda x: x["total_score"], reverse=True)

top_5_crypto = crypto_strengths[:5]

print("Top 5 investment-worthy cryptocurrencies:")
for i, crypto in enumerate(top_5_crypto, 1):
    print(f"{i}. {crypto['name']} ({crypto['symbol']}):")
    print(f"  Total Score: {crypto['total_score']:.2f}")
    print(f"  RSI: {crypto['indicators']['rsi']:.2f}")
    print(f"  MACD: {crypto['indicators']['macd']:.2f}")
    print(f"  MACD Signal: {crypto['indicators']['macd_signal']:.2f}")
    print(f"  Bollinger Lower Band: {crypto['indicators']['bollinger_lband']:.2f}")
    print(f"  Bollinger Upper Band: {crypto['indicators']['bollinger_hband']:.2f}")
    print(f"  Stochastic %K: {crypto['indicators']['stochastic_k']:.2f}")
    print(f"  Stochastic %D: {crypto['indicators']['stochastic_d']:.2f}")
    print(f"  Bollinger Bandwidth: {crypto['indicators']['bollinger_bandwidth']:.2f}")
    print(f"  Future Trend: {crypto['future_trend']}")
    print()
