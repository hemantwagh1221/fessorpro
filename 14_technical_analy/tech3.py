
import yfinance as yf
data=yf.download('MGC=F',interval='5m',start='2025-9-23',end='2025-10-24',multi_level_index=False)
print(data)

import pandas_ta as ta

#resample to daily data
d={'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'}
data= data.resample('D').agg(d)
data = data.dropna()
print(data)

def macd(close, fast=None, slow=None, signal=None, talib=None, 
         offset=None, **kwargs):
    """Moving Average Convergence Divergence (MACD)
    
    This indicator attempts to identify trends using the difference between
    two exponential moving averages and a signal line.
    
    Parameters:
    close (Series): close Series
    fast (int): Fast EMA period. Default: 12
    slow (int): Slow EMA period. Default: 26
    signal (int): Signal EMA period. Default: 9
    talib (bool): Ignored (for compatibility). Default: None
    offset (int): Post shift. Default: 0
    
    Other Parameters:
    asmode (bool): Enable AS version of MACD. Default: False
    fillna (value): pd.DataFrame.fillna(value)
    
    Returns:
    DataFrame: 3 columns (MACD, MACDh, MACDs)
    """
    import pandas as pd
    
    # Set defaults
    fast = 12 if fast is None else max(1, int(fast))
    slow = 26 if slow is None else max(1, int(slow))
    signal = 9 if signal is None else max(1, int(signal))
    offset = 0 if offset is None else int(offset)
    as_mode = kwargs.get("asmode", False)
    
    # Ensure slow >= fast
    if slow < fast:
        fast, slow = slow, fast
    
    # Validate input length
    _length = slow + signal - 1
    if len(close) < _length:
        return None
    
    # Helper function: Calculate EMA
    def calculate_ema(series, length):
        """Calculate Exponential Moving Average"""
        alpha = 2.0 / (length + 1)
        ema_values = [None] * len(series)
        
        # Initialize with SMA
        sma = sum(series.iloc[:length]) / length
        ema_values[length - 1] = sma
        
        # Calculate EMA
        for i in range(length, len(series)):
            ema_values[i] = alpha * series.iloc[i] + (1 - alpha) * ema_values[i - 1]
        
        return pd.Series(ema_values, index=series.index)
    
    # Calculate fast and slow EMAs
    fastma = calculate_ema(close, fast)
    slowma = calculate_ema(close, slow)
    
    # Calculate MACD line
    macd_line = fastma - slowma
    
    # Find first valid index (where slowma becomes valid)
    first_valid_idx = slow - 1
    macd_valid = macd_line.iloc[first_valid_idx:]
    
    # Calculate signal line (EMA of MACD)
    # Need to create a properly indexed series for signal calculation
    macd_for_signal = pd.Series([None] * len(close), index=close.index)
    for i in range(first_valid_idx, len(close)):
        macd_for_signal.iloc[i] = macd_line.iloc[i]
    
    # Calculate signal EMA starting from first valid MACD value
    signal_values = [None] * len(close)
    valid_macd_vals = [macd_line.iloc[i] for i in range(first_valid_idx, len(close)) 
                       if macd_line.iloc[i] is not None]
    
    if len(valid_macd_vals) >= signal:
        alpha_signal = 2.0 / (signal + 1)
        # Initialize signal with SMA of first 'signal' MACD values
        signal_sma = sum(valid_macd_vals[:signal]) / signal
        signal_start_idx = first_valid_idx + signal - 1
        signal_values[signal_start_idx] = signal_sma
        
        # Calculate signal EMA
        for i in range(signal_start_idx + 1, len(close)):
            if macd_line.iloc[i] is not None:
                signal_values[i] = (alpha_signal * macd_line.iloc[i] + 
                                   (1 - alpha_signal) * signal_values[i - 1])
    
    signalma = pd.Series(signal_values, index=close.index)
    
    # Calculate histogram
    histogram = macd_line - signalma
    
    # AS Mode calculation
    if as_mode:
        macd_line = macd_line - signalma
        
        # Recalculate signal for AS mode
        first_valid_idx_as = None
        for i in range(len(macd_line)):
            if macd_line.iloc[i] is not None and not pd.isna(macd_line.iloc[i]):
                first_valid_idx_as = i
                break
        
        if first_valid_idx_as is not None:
            valid_macd_as = [macd_line.iloc[i] for i in range(first_valid_idx_as, len(close)) 
                           if not pd.isna(macd_line.iloc[i])]
            
            signal_values_as = [None] * len(close)
            if len(valid_macd_as) >= signal:
                alpha_signal = 2.0 / (signal + 1)
                signal_sma_as = sum(valid_macd_as[:signal]) / signal
                signal_start_idx_as = first_valid_idx_as + signal - 1
                signal_values_as[signal_start_idx_as] = signal_sma_as
                
                for i in range(signal_start_idx_as + 1, len(close)):
                    if not pd.isna(macd_line.iloc[i]):
                        signal_values_as[i] = (alpha_signal * macd_line.iloc[i] + 
                                               (1 - alpha_signal) * signal_values_as[i - 1])
            
            signalma = pd.Series(signal_values_as, index=close.index)
            histogram = macd_line - signalma
    
    # Apply offset
    if offset != 0:
        macd_line = macd_line.shift(offset)
        histogram = histogram.shift(offset)
        signalma = signalma.shift(offset)
    
    # Fill NA values if requested
    if "fillna" in kwargs:
        macd_line = macd_line.fillna(kwargs["fillna"])
        histogram = histogram.fillna(kwargs["fillna"])
        signalma = signalma.fillna(kwargs["fillna"])
    
    # Create column names
    _asmode = "AS" if as_mode else ""
    _props = f"_{fast}_{slow}_{signal}"
    
    # Create DataFrame
    data = {
        f"MACD{_asmode}{_props}": macd_line,
        f"MACD{_asmode}h{_props}": histogram,
        f"MACD{_asmode}s{_props}": signalma
    }
    
    df = pd.DataFrame(data, index=close.index)
    df.name = f"MACD{_asmode}{_props}"
    
    return df


macd1=macd(data['Close'],10,3)
print(super)


import mplfinance as mpf
# a=mpf.make_addplot(macd1['MACD_3_10_9'],color='black',panel=1)
# b=mpf.make_addplot(macd1['MACDs_3_10_9'],color='blue',panel=1)
# c=mpf.make_addplot(macd1['MACDh_3_10_9'],color='red',panel=1,type='bar')
# mpf.plot(data,type='candle',style='yahoo',addplot=[a,b,c])


# adx=ta.adx(data['High'], data['Low'], data['Close'])
# print(adx)

# a=mpf.make_addplot(adx['ADX_14'],color='black',panel=1)
# mpf.plot(data,type='candle',style='yahoo',addplot=[a])

#atr
#rsi

# atr=ta.atr(data['High'], data['Low'], data['Close'])
# print(atr)

# import mplfinance as mpf
# a=mpf.make_addplot(atr,color='black',panel=1)

# mpf.plot(data,type='candle',style='yahoo',addplot=[a])