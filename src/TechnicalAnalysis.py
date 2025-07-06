import pandas as pd

class TechnicalIndicators:
    def __init__(self, price_data: pd.DataFrame):
        if 'Close' not in price_data.columns:
            raise ValueError("price_data must contain a 'Close' column")
        self.price_data = price_data
        self.macd = None
        self.macd_signal = None

    # TODO:
    def calculate_resistance(price_data, lookback_period=50, tolerance=0.01):
        """
        Identifies a potential resistance level based on recent highs within a lookback period.

        Parameters
        ----------
        price_data : pd.DataFrame
            DataFrame with historical price data. Must include a 'High' column.

        lookback_period : int, default=50
            Number of most recent candles to scan for resistance.

        tolerance : float, default=0.01
            Percentage tolerance to group similar highs (e.g., 0.01 = 1%).

        Returns
        -------
        float
            Estimated resistance level (can be None if not enough data).
        """

        return
    

    def calculate_macd_fast_line(self, short_span=12, long_span=26):
        short_ema = self.price_data['Close'].ewm(span=short_span, adjust=False).mean()
        long_ema = self.price_data['Close'].ewm(span=long_span, adjust=False).mean()
        self.macd = short_ema - long_ema
        return self.macd

    def calculate_macd_ema_slow_signal(self, signal_span=9):
        if self.macd is None:
            raise ValueError("MACD must be calculated before the signal line.")
        self.macd_signal = self.macd.ewm(span=signal_span, adjust=False).mean()
        return self.macd_signal
