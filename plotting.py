import yfinance as yf
import plotly.graph_objects as go 
import logging


# def compute_ema(price_data)
def plot_stock_price(price_data, ticker_name, buy_sell_data = None, candlestick = True, ema_periods = [13, 26]):
    """
    Plots the price history of a given stock ticker using Yahoo Finance data, 
    with optional trade markers (market/limit buys and sells). Supports both 
    candlestick and line chart modes.

    
    Parameters
    ----------
    ticker_name : str
        The stock ticker symbol (e.g., 'AAPL', 'TSLA') to fetch price data for.

    buy_sell_data : pandas.DataFrame, optional
        A DataFrame containing trade signal metadata to overlay on the price chart.
        If provided, must contain at least the following columns:

            - 'Time' (datetime): Timestamp of each trade signal
            - 'Action' (str): One of the following values (case-sensitive):
                - 'Market buy'
                - 'Market sell'
                - 'Limit buy'
                - 'Limit sell'
            - 'Price / share' (float): Executed or target price of the trade
            - 'Total' (float): Total value of the transaction (used in hover tooltips)

        Additional columns can be included, but only 'Total' is shown in the hover tooltips.

    candlestick : bool, default=True
        Whether to plot the stock as a candlestick chart. If False, a line chart of 
        the closing price will be used instead.

    ema : list of int, default=[13, 26]
        List of EMA periods to calculate and overlay on the chart.
 

        
    Returns
    -------
    None
        Displays an interactive Plotly chart with price data and optional trade markers.

    Notes
    -----
    - This function fetches data using yfinance; an internet connection is required.
    - Any trade rows with times that do not match trading days in the price data 
      will be silently ignored.
    - The 'Total' value is displayed in GBP (£) in the tooltip; adjust hovertemplate 
      if needed for other currencies.
    - Use `candlestick=False` for long-term views or cleaner visuals.
    """
    logging.basicConfig(level=logging.ERROR, format='%(levelname)s: %(message)s', force=True)


    # Plot historical prices with candlestick or linegraph style. 
    if candlestick:
        fig = go.Figure(data=[go.Candlestick(
            x=price_data.index,
            open=price_data['Open'],
            high=price_data['High'],
            low=price_data['Low'],
            close=price_data['Close'],
            name= f'{ticker_name} Price'
        )])
    else:
        fig = go.Figure() 
        fig.add_trace(go.Scatter(
            x=price_data.index,
            y=price_data['Close'],
            mode='lines',
            name=f'{ticker_name} Close Price',
            line=dict(color='blue')
        )) 
    

    # Plot specified EMA'S (if any)
    if ema_periods:
        for span in ema_periods:
            ema_vals = price_data['Close'].ewm(span= span, adjust=False).mean()
            fig.add_trace(go.Scatter(
                x=ema_vals.index,
                y=ema_vals,
                mode='lines',
                name= f'EMA_{span}',
                line=dict(dash='dash')
            ))


    # Plot trading history if available
    if buy_sell_data is not None:
        action_styles = {
            'Market buy': dict(symbol='triangle-up', color='green'),
            'Market sell': dict(symbol='triangle-down', color='red'),
            'Limit buy': dict(symbol='triangle-up', color='green'),
            'Limit sell': dict(symbol='triangle-down', color='red'),
        }
        for action, style in action_styles.items():
            subset = buy_sell_data[buy_sell_data['Action'] == action]
            if not subset.empty:
                fig.add_trace(go.Scatter(
                    x=subset['Time'],
                    y=subset['Price / share'],
                    mode='markers',
                    marker=dict(symbol=style['symbol'], color=style['color'], size=10),
                    name=action,
                    customdata=subset[['Total', 'Result']].values,
                    hovertemplate=
                        'Time: %{x}<br>' +
                        'Price: $%{y:.2f}<br>' +
                        'Value: £%{customdata[0]}<br>' +
                        'Result: £%{customdata[1]}<br>'
                ))

    fig.update_layout(
        title= f'{ticker_name} Chart',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        xaxis_rangeslider_visible=False
    )
    fig.show()

    return
