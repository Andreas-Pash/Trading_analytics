import yfinance as yf

import plotly.graph_objects as go 
from plotly.subplots import make_subplots

import logging


# def compute_ema(price_data)
def plot_stock_price(price_data,
                ticker_name,
                buy_sell_data = None,
                candlestick = True,
                ema_periods = [13, 26],
                plot_macd = False,
                fast_macd = None,
                slow_signal = None,
                plot_volume = False

            ):
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
 
    if plot_macd:
        if fast_macd is None or slow_signal is None:
            raise ValueError("If plot_macd=True, both fast_macd and slow_signal must be provided.")       
        
        if plot_volume:
            volume_row = 4
            fig = make_subplots(rows=4, cols=1, shared_xaxes=True,
                row_heights=[0.56, 0.14, 0.14, 0.14 ],
                vertical_spacing= 0.1,
                subplot_titles=(f'{ticker_name} Price', 'MACD', 'MACD Histogram', 'Volume')
            )
            volume_row = 4   
        else:
            fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                    row_heights=[0.6, 0.25, 0.15],
                    vertical_spacing= 0.1,
                    subplot_titles=(f'{ticker_name} Price', 'MACD', 'MACD Histogram')
                )
        
    else:
        if plot_volume:
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                    row_heights=[0.65, 0.35],
                    vertical_spacing= 0.1,
                    subplot_titles=(f'{ticker_name} Price', 'Volume')
                )
            volume_row = 2
        else:
            fig = make_subplots(
                rows=1, cols=1, shared_xaxes=True,
                subplot_titles=(f'{ticker_name} Price',)
            )


    # Plot historical prices with candlestick or linegraph style. 
    if candlestick:
        fig.add_trace(go.Candlestick(
            x=price_data.index,
            open=price_data['Open'],
            high=price_data['High'],
            low=price_data['Low'],
            close=price_data['Close'],
            name= f'{ticker_name} Price'
        ), row=1, col=1)
    else:  
        fig.add_trace(go.Scatter(
            x=price_data.index,
            y=price_data['Close'],
            mode='lines',
            name=f'{ticker_name} Close Price',
            line=dict(color='blue')
        ), row=1, col=1)
    

    # Plot specified EMA'S (if any)
    if ema_periods:
        for span in ema_periods:
            ema_vals = price_data['Close'].ewm(span= span, adjust=False).mean()
            # Todo: Move the above calcualtion to the Techinical indicators module
            
            fig.add_trace(go.Scatter(
                x=ema_vals.index,
                y=ema_vals,
                mode='lines',
                name= f'EMA_{span}',
                line=dict(dash='dash')
            ), row=1, col=1)


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
                ), row=1, col=1)


    # Plot MACD if requested                 
    if plot_macd:
        # Fast MACD line
        fig.add_trace(go.Scatter(
            x=fast_macd.index,
            y=fast_macd,
            mode='lines',
            name='Fast MACD Line',
            line=dict(dash='dash', color='blue', width=2)
        ), row=2, col=1)

        # Slow MACD Signal Line
        fig.add_trace(go.Scatter(
            x=slow_signal.index,
            y=slow_signal,
            mode='lines',
            name='Slow Signal Line',
            line=dict(dash='dot', color='red', width=2)
        ), row=2, col=1)

        # MACD Histogram
        macd_hist = fast_macd - slow_signal
        fig.add_trace(go.Bar(
            x=macd_hist.index,
            y=macd_hist,
            name='MACD Histogram',
            marker_color='black'
        ), row=3, col=1)  


    # Plot Volume if requested  
    if plot_volume:
        fig.add_trace(
            go.Bar(
                x=price_data.index,
                y=price_data['Volume'],
                name='Volume',
                marker_color='red',
                opacity=0.5
            ),
            row= volume_row,
            col=1
        )


    fig.update_layout(
        title= f"{ticker_name} Price {'with MACD' if plot_macd else ''}",
        height=900,
        width=1200,
        xaxis_rangeslider_visible=False,
        xaxis=dict(        # row=1
            tickformat="%Y-%m-%d",
            tickangle=45,
            showgrid=True
        ),
        xaxis2=dict(       # row=2
            showticklabels=False,
            showgrid=True
        ),
        xaxis3=dict(       # row=3
            title='Date',
            tickformat="%Y-%m-%d",
            tickangle=45,
            showgrid=True
        )
    )

    fig.show()
    return
