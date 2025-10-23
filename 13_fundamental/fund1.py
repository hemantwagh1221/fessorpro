
import pandas as pd
from finvizfinance.quote import finvizfinance

stock = finvizfinance('tsla')
d=stock.ticker_fundament()
# p=d.get('P/E')
# # pd.Series(d).to_csv('tsla.csv')
# print(p)

#news
n=stock.ticker_news()
print(n)


print(stock.ticker_description())




# stocks=['TSLA','GOOG','AMZN','NVDA','JPM']
# list=[]
# for i in stocks:
#     t=finvizfinance(i)
    
#     p=t.ticker_fundament()
#     m=p.get('P/E')
#     list.append(m)
    
# print(list)

# b=list.index(max(list))
# print(stocks[3])