
import yfinance as yf

# data=yf.download('^NSEI',start='2024-02-01',end='2025-02-01',interval='1h',multi_level_index=False,ignore_tz=True)
# print(data)


# name='NVDA'
# ticker1=yf.Ticker(name)
# # print(ticker1.get_info())

# import pandas as pd
# d=pd.Series(ticker1.get_info())
# d.to_csv('data.csv')

# d1=ticker1.get_info()
# b1=d1.get('beta')
# print(b1)



# ticker_list=['AMZN','TSLA','NVDA','GOOG','JPM']
# list=[]
# for t in ticker_list:
#     t1=yf.Ticker(t)
#     b1=t1.get_info().get('beta')
#     list.append(b1)
# print(list)

# i=list.index(max(list))
# print(ticker_list[i])

name='JPM'
t1=yf.Ticker(name)
d=t1.get_income_stmt()
print(d)


d=t1.get_balance_sheet()
print(d)


d=t1.get_cash_flow()
print(d)

bs1=t1.quarterly_balance_sheet
print(bs1)