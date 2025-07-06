import pandas as pd

import pytest

from src.TechnicalAnalysis import *
from src.plotting import *


data = pd.DataFrame({'Close': [100, 102, 101, 105, 107, 106, 108, 110]})
def test_macd_calculation():
    """
    Test that MACD is calculated with correct shape and not all NaNs.
    """
    # Sample input
    ti = TechnicalIndicators(data)

    macd = ti.calculate_macd_fast_line(short_span=3, long_span=6)
    assert len(macd) == len(data)  # basic shape check
    assert not macd.isnull().all()  # check it’s not all NaNs


def test_macd_signal_calculation():
    """
    Test that MACD signal line is calculated correctly after MACD.
    """ 
    ti = TechnicalIndicators(data)

    ti.calculate_macd_fast_line(short_span=3, long_span=6)
    signal = ti.calculate_macd_ema_slow_signal(signal_span=2)

    assert len(signal) == len(data)
    assert not signal.isnull().all()


def test_missing_close_column():
    """
    Test that class raises ValueError if 'Close' column is missing.
    """
    with pytest.raises(ValueError, match="must contain a 'Close' column"):
        TechnicalIndicators(pd.DataFrame({'Open': [100, 102]}))


def test_signal_without_macd():
    """
    Test that signal line calculation without MACD raises an error.
    """ 
    ti = TechnicalIndicators(data)

    with pytest.raises(ValueError, match="MACD must be calculated"):
        ti.calculate_macd_ema_slow_signal()


def test_plot_macd_without_signals_raises_error():
    with pytest.raises(ValueError, match="both fast_macd and slow_signal must be provided"):
        plot_stock_price(
            price_data= data,
            ticker_name="AAPL",
            plot_macd=True,
            fast_macd=data
        )
    with pytest.raises(ValueError, match="both fast_macd and slow_signal must be provided"):
        plot_stock_price(
            price_data= data,
            ticker_name="AAPL",
            plot_macd=True, 
            slow_signal=data
        )
    with pytest.raises(ValueError, match="both fast_macd and slow_signal must be provided"):
        plot_stock_price(
            price_data= data,
            ticker_name="AAPL",
            plot_macd=True
        )