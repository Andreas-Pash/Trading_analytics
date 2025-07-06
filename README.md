````markdown
# 📊 Stock Price Visualization & Swing Trading Signal Tool

A Python-based visualization tool for analyzing historical stock price data, overlaying trade signals (Market and Limit orders), and plotting MACD indicators — tailored for swing traders.

---

## 🚀 Features

- Fetch historical stock price data using `yfinance`
- Choose between **candlestick** or **line chart** views
- Overlay **Market Buy/Sell** and **Limit Buy/Sell** trades with hover metadata
- Visualize **MACD** and **Signal Lines** with optional histogram
- Subplot layout optimized for multi-indicator analysis
- Configurable chart sizes and export-ready visuals

---

## 📦 Requirements

Install the dependencies via pip:

```bash
pip install yfinance plotly pandas
````

---

## 🧠 Target User

This tool is designed for **traders** who analyze multi-day to multi-week trends and want to visualize:

* Entry/exit points
* Trade metadata
* MACD-based momentum signals
* Clean price action (excluding pre/post-market noise)

---

## 🛠️ How It Works

```python
plot_stock_price(
    ticker_name='TSLA',
    buy_sell_data=your_trade_dataframe,
    candlestick=True,
    plot_macd=True,
    period='6mo',
    granularity='1d'
)
```

* `ticker_name`: Stock symbol (e.g., `'AAPL'`, `'TSLA'`)
* `buy_sell_data`: DataFrame with trade actions (see format below)
* `candlestick`: Whether to use candlestick (or line) chart
* `plot_macd`: Toggle MACD and MACD Histogram subplots
* `period` / `granularity`: Time range and resolution

---

## 📋 Trade Data Format

To overlay trades, the `buy_sell_data` DataFrame must contain:

| Column          | Type     | Description                                                            |
| --------------- | -------- | ---------------------------------------------------------------------- |
| `Time`          | datetime | Timestamp of the trade                                                 |
| `Action`        | str      | One of: `'Market buy'`, `'Market sell'`, `'Limit buy'`, `'Limit sell'` |
| `Price / share` | float    | Execution or target price                                              |
| `Total`         | float    | Total value (used for hover tooltips)                                  |

🔔 **NOTE:** The above come out of the box from Trading212 export History export

---

## 📈 Chart Output

When `plot_macd=True`, the chart includes:

1. Stock Price (candlestick or line)
2. MACD Line (dashed blue) & Signal Line (dotted red)
3. MACD Histogram (green/red bars)

---

## ✅ Best Practices for Swing Trading Use

* Uses **only regular trading hours** (no pre/post-market noise)
* Recommended interval: `'1d'` or `'1h'`

---

## 📎 TODO / Future Improvements

* Add additional indicators such as RSI and volume
* Support/Resistance levels – for entry/exit zones
* UI for uploading trade logs

---

## 📃 License

MIT License — free to use and modify.
