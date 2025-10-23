
import yfinance as yf
data=yf.download('NVDA',interval='1m',start='2025-10-21',end='2025-10-23',multi_level_index=False)
print(data)

import pandas as pd

# import talib
# import pandas_ta

import pandas_ta as ta
data['sma']=ta.sma(data['Close'],length=10)
data


# import talib as ta
# data['sma2']=ta.SMA(data['Close'],10)
# print(data)


# data['ema']=ta.ema(data['Close'],10)
# print(data)

def bbands(close, length=5, lower_std=2.0, upper_std=2.0, ddof=1):
    """
    Bollinger Bands - Pure Python Implementation
    Returns a pandas DataFrame like the original function
    
    Parameters:
        close (list or pandas Series): List/Series of closing prices
        length (int): The period for moving average. Default: 5
        lower_std (float): Lower standard deviation multiplier. Default: 2.0
        upper_std (float): Upper standard deviation multiplier. Default: 2.0
        ddof (int): Degrees of Freedom (0 or 1). Default: 1
    
    Returns:
        pandas DataFrame: DataFrame with columns 'BBL_X_Y_Z', 'BBM_X_Y_Z', 'BBU_X_Y_Z', 
                         'BBB_X_Y_Z', 'BBP_X_Y_Z' where X=length, Y=lower_std, Z=upper_std
    """
    import pandas as pd
    
    # Convert to list for processing
    if hasattr(close, 'tolist'):
        close_list = close.tolist()
    elif hasattr(close, 'values'):
        close_list = close.values.tolist()
    else:
        close_list = list(close)
    
    # Get the index from the original Series
    if hasattr(close, 'index'):
        index = close.index
    else:
        index = range(len(close_list))
    
    if not close_list or len(close_list) < length:
        return None
    
    n = len(close_list)
    
    # Initialize output lists with None for the first (length-1) values
    lower = [None] * (length - 1)
    mid = [None] * (length - 1)
    upper = [None] * (length - 1)
    bandwidth = [None] * (length - 1)
    percent = [None] * (length - 1)
    
    # Calculate for each valid window
    for i in range(length - 1, n):
        # Get window of data
        window = close_list[i - length + 1:i + 1]
        
        # Calculate Simple Moving Average (SMA)
        sma = sum(window) / length
        
        # Calculate Standard Deviation
        variance = sum((x - sma) ** 2 for x in window) / (length - ddof)
        std_dev = variance ** 0.5
        
        # Calculate bands
        lower_band = sma - (lower_std * std_dev)
        upper_band = sma + (upper_std * std_dev)
        
        # Calculate bandwidth (percentage)
        band_range = upper_band - lower_band
        bw = 100 * band_range / sma if sma != 0 else 0
        
        # Calculate percent B (position within bands)
        if band_range != 0:
            pct = (close_list[i] - lower_band) / band_range
        else:
            pct = 0.5
        
        # Append results
        lower.append(lower_band)
        mid.append(sma)
        upper.append(upper_band)
        bandwidth.append(bw)
        percent.append(pct)
    
    # Create column names like the original function
    _props = f"_{length}_{lower_std}_{upper_std}"
    
    # Create DataFrame
    df = pd.DataFrame({
        f'BBL{_props}': lower,
        f'BBM{_props}': mid,
        f'BBU{_props}': upper,
        f'BBB{_props}': bandwidth,
        f'BBP{_props}': percent
    }, index=index)
    
    df.name = f"BBANDS{_props}"
    df.category = "volatility"
    
    return df


# Example usage
if __name__ == "__main__":
    import pandas as pd
    
    # Sample closing prices
    prices = [100, 102, 101, 103, 105, 104, 106, 108, 107, 109, 111, 110, 112]
    
    # Create a pandas Series
    close_series = pd.Series(prices)
    
    # Calculate Bollinger Bands
    result = bbands(close_series, length=5, lower_std=2.0, upper_std=2.0)
    
    print("Bollinger Bands Results:")
    print(result)



d=bbands(data['Close'], 30)
print(d)



import mplfinance as mpf
# a=mpf.make_addplot(d['BBL_30_2.0_2.0'],color='black')
# b=mpf.make_addplot(d['BBM_30_2.0_2.0'],color='blue')
# c=mpf.make_addplot(d['BBU_30_2.0_2.0'],color='green')
# mpf.plot(data,type='candle',style='yahoo',addplot=[a,b,c])

#atr

def atr(high, low, close, length=None, mamode=None, talib=None, drift=None, offset=None, **kwargs):
    # Validate arguments
    length = int(length) if length is not None and length > 0 else 14
    mamode = mamode.lower() if mamode and isinstance(mamode, str) else "rma"
    drift = int(drift) if drift is not None and drift >= 1 else 1
    offset = int(offset) if offset is not None and offset != 0 else 0
    
    # If any of the series is None, return None
    if high is None or low is None or close is None:
        return None
    
    # Calculate True Range (TR)
    prev_close = close.shift(drift)
    tr0 = high - low
    tr1 = (high - prev_close).abs()
    tr2 = (low - prev_close).abs()
    tr = pd.concat([tr0, tr1, tr2], axis=1).max(axis=1)
    
    # Calculate ATR based on the specified moving average mode
    if mamode == 'sma':
        atr_series = tr.rolling(window=length).mean()
    elif mamode == 'ema':
        atr_series = tr.ewm(span=length, adjust=False).mean()
    elif mamode == 'wma':
        def wma(series, window):
            weights = np.arange(1, window + 1)
            def calc(x):
                return np.dot(x, weights) / weights.sum()
            return series.rolling(window=window).apply(calc, raw=True)
        atr_series = wma(tr, length)
    else:  # Default to RMA (Wilder's MA)
        atr_series = tr.ewm(alpha=1.0/length, adjust=False).mean()
    
    # Convert to percentage if requested
    if kwargs.get("percent", False):
        atr_series = atr_series * 100 / close
    
    # Apply offset
    if offset != 0:
        atr_series = atr_series.shift(offset)
    
    # Handle fills
    fillna = kwargs.get('fillna', None)
    if fillna is not None:
        atr_series.fillna(fillna, inplace=True)
    
    fill_method = kwargs.get('fill_method', None)
    if fill_method is not None:
        atr_series.fillna(method=fill_method, inplace=True)
    
    # Name the series
    mamode_prefix = mamode[0] if mamode else 'r'
    percent_suffix = 'p' if kwargs.get("percent", False) else ''
    atr_series.name = f"ATR{mamode_prefix}_{length}{percent_suffix}"
    
    return atr_series




        
atr1=atr(data['High'],data['Low'],data['Close'],10)
print(atr1)

a=mpf.make_addplot(d['BBL_30_2.0_2.0'],color='black')
b=mpf.make_addplot(d['BBM_30_2.0_2.0'],color='blue')
c=mpf.make_addplot(d['BBU_30_2.0_2.0'],color='green')
d=mpf.make_addplot(atr1,color='red',panel=1)
mpf.plot(data,type='candle',style='yahoo',addplot=[a,b,c,d])