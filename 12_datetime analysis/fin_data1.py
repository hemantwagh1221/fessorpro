import yfinance as yf
data=yf.download('TSLA',interval='1m',period='3d')
print(data.to_csv('data.csv'))