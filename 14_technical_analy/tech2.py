
import yfinance as yf
data=yf.download('MGC=F',interval='5m',start='2025-10-23',end='2025-10-24',multi_level_index=False)
print(data)

import pandas_ta as ta
super=ta.supertrend(data['High'],data['Low'],data['Close'],10,3)
print(super)


import pandas as pd
import numpy as np


def supertrend(high, low, close, length=None, atr_length=None, 
               multiplier=None, atr_mamode=None, offset=None, **kwargs):
    """Supertrend
    
    This indicator attempts to identify trend direction as well as support and
    resistance levels.
    
    Parameters:
    high (Series): high Series
    low (Series): low Series
    close (Series): close Series
    length (int): The period. Default: 7
    atr_length (int): ATR period. Default: length
    multiplier (float): Coefficient for upper and lower band distance to
                       midrange. Default: 3.0
    atr_mamode (str): MA type to be used for ATR calculation. Default: "rma"
    offset (int): Post shift. Default: 0
    
    Returns:
    DataFrame: 4 columns (SUPERT, SUPERTd, SUPERTl, SUPERTs)
    """
    import pandas as pd
    
    # Set defaults
    length = 7 if length is None else max(1, int(length))
    atr_length = length if atr_length is None else max(1, int(atr_length))
    multiplier = 3.0 if multiplier is None else float(multiplier)
    atr_mamode = "rma" if atr_mamode is None else str(atr_mamode).lower()
    offset = 0 if offset is None else int(offset)
    
    # Validate input
    if len(high) < length + 1 or len(low) < length + 1 or len(close) < length + 1:
        return None
    
    m = len(close)
    
    # Calculate HL2 (midpoint)
    hl2_vals = [(high.iloc[i] + low.iloc[i]) / 2.0 for i in range(m)]
    
    # Calculate True Range
    tr = [0.0] * m
    tr[0] = high.iloc[0] - low.iloc[0]
    for i in range(1, m):
        h_l = high.iloc[i] - low.iloc[i]
        h_pc = abs(high.iloc[i] - close.iloc[i-1])
        l_pc = abs(low.iloc[i] - close.iloc[i-1])
        tr[i] = max(h_l, h_pc, l_pc)
    
    # Calculate ATR based on mamode
    atr_vals = [0.0] * m
    
    if atr_mamode == "rma" or atr_mamode == "ema":
        # RMA (Wilder's smoothing) / EMA
        alpha = 1.0 / atr_length
        atr_vals[atr_length-1] = sum(tr[:atr_length]) / atr_length
        for i in range(atr_length, m):
            atr_vals[i] = alpha * tr[i] + (1 - alpha) * atr_vals[i-1]
    elif atr_mamode == "sma":
        # Simple Moving Average
        for i in range(atr_length-1, m):
            atr_vals[i] = sum(tr[i-atr_length+1:i+1]) / atr_length
    else:
        # Default to RMA
        alpha = 1.0 / atr_length
        atr_vals[atr_length-1] = sum(tr[:atr_length]) / atr_length
        for i in range(atr_length, m):
            atr_vals[i] = alpha * tr[i] + (1 - alpha) * atr_vals[i-1]
    
    # Calculate MATR (multiplier * ATR)
    matr = [multiplier * atr_vals[i] for i in range(m)]
    
    # Calculate lower and upper bands
    lb = [hl2_vals[i] - matr[i] for i in range(m)]
    ub = [hl2_vals[i] + matr[i] for i in range(m)]
    
    # Initialize direction and trend arrays
    dir_ = [1] * m
    trend = [float('nan')] * m
    long = [float('nan')] * m
    short = [float('nan')] * m
    
    # Calculate Supertrend
    for i in range(1, m):
        # Determine direction
        if close.iloc[i] > ub[i - 1]:
            dir_[i] = 1
        elif close.iloc[i] < lb[i - 1]:
            dir_[i] = -1
        else:
            dir_[i] = dir_[i - 1]
        
        # Adjust bands based on direction
        if dir_[i] > 0 and lb[i] < lb[i - 1]:
            lb[i] = lb[i - 1]
        if dir_[i] < 0 and ub[i] > ub[i - 1]:
            ub[i] = ub[i - 1]
        
        # Set trend values
        if dir_[i] > 0:
            trend[i] = lb[i]
            long[i] = lb[i]
        else:
            trend[i] = ub[i]
            short[i] = ub[i]
    
    # Set initial NaN values
    for i in range(length):
        dir_[i] = float('nan')
    
    # Create DataFrame
    _props = f"_{length}_{multiplier}"
    data = {
        f"SUPERT{_props}": trend,
        f"SUPERTd{_props}": dir_,
        f"SUPERTl{_props}": long,
        f"SUPERTs{_props}": short
    }
    
    df = pd.DataFrame(data, index=close.index)
    df.name = f"SUPERT{_props}"
    
    # Apply offset
    if offset != 0:
        df = df.shift(offset)
    
    # Fill NA values if requested
    if "fillna" in kwargs:
        df.fillna(kwargs["fillna"], inplace=True)
    
    return df


super=supertrend(data['High'],data['Low'],data['Close'],10,3)
print(super)

# import mplfinance as mpf
# a=mpf.make_addplot(super['SUPERTl_7_3.0'],color='black')
# b=mpf.make_addplot(super['SUPERTs_7_3.0'],color='blue')

# mpf.plot(data,type='candle',style='yahoo',addplot=[a,b])

#macd
# stochastic osc
# rsi
# adx

#plotly
#tradingview chart


# import pandas as pd
# from lightweight_charts import Chart



# def calculate_sma(df, period: int = 50):
#     return pd.DataFrame({
#         'time': df['Datetime'],
#         f'SMA {period}': df['Close'].rolling(window=period).mean()
#     }).dropna()


# chart = Chart()
# chart.legend(visible=True)

# df = data
# chart.set(df)

# line = chart.create_line('SMA 50')
# sma_data = calculate_sma(df.reset_index(), period=50)
# line.set(sma_data)

# chart.show(block=True)