#coding: utf-8
import quandl
import pandas as pd
import numpy as np
import math as m

quandl.ApiConfig.api_key = 'ACKX-sC87Evgmif6miSm'

sp500list = pd.read_csv(r"/Users/mengdantian/Downloads/sp500.csv")
#functions get Close price, log return, skewnss
def get_share_close(x):
    y = quandl.get([x],start_date="2015-06-26",end_date="2016-06-30")
   # y = quandl.get([x])
    y = y[y.keys()[3]]
    return y

def daily_ret(x):
    ret = x/x.shift(1)
    return np.log(ret)

def skewness(x):
    t = daily_ret(x)
    meanret =t.mean()
    std = t.std()
    skew = np.mean(np.power((t - meanret),3)) / np.power(std,3)
    return skew

#get all data and get skewness stats
sp500stk = []
for x in sp500list['free_code'][:10]:
    stk= get_share_close(x)
    sp500stk.append(stk)

sp500data = pd.concat(sp500stk,ignore_index=False,axis=1)
#headers = sp500data.dtypes.index
#skewnesstable = sp500data.apply(skewness,axis=0)
#result = skewnesstable.sort_values()
#print skewnesstable[result.index[:2]] #get the first two ranking record

#generate signal based on the ranking table, since it is rolling, rolling ranking
def signal_on_rank(data,selectionptg,window):
    days = window * 22
    stklist = list(data.columns.values)
    a = np.zeros(shape=(data.shape[0], len(stklist)))
    signals = pd.DataFrame(a,index=data.index,columns = stklist)

    for row in range(days,data.shape[0]):

        rank = data[(row-days):row].apply(skewness,axis = 0)
        ranksort = rank.sort_values()

        id1 = rank[ranksort.index[:m.ceil(rank.shape[0]*selectionptg)]].index.tolist()
        id2 = rank[ranksort.index[rank.shape[0]-m.floor(rank.shape[0] * selectionptg):rank.shape[0]]].index.tolist()
        #signals.loc[data.index[row]] = np.zeros(data.shape[1]) #initial the array
        for col in range(len(stklist)-1):

            if stklist[col] in id1:
                signals.loc[data.index[row],stklist[col]] = 1
            elif stklist[col] in id2:
                signals.loc[data.index[row],stklist[col]] = -1

    return signals
signaltable = signal_on_rank(sp500data,0.1,3)
print signaltable

class portfolio:

    def __init__(self,signal,init_cap,prices):
        self.initial_capital = init_cap * np.ones(len(prices))
        self.prices=prices
        self.positions = signal #row by row.... (date)

    def backtest_portfolio(self):
        portfolio = pd.DataFrame(index=self.prices.index)
        pos_diff = self.positions.diff()
        # Create a ‘holdings’ Series that totals all open position market values
        # and a ‘cash’ column that stores remaining cash in account
        portfolio['holdings'] = np.multiply(self.positions.values, self.prices.values)
        #here issue, .sum() cannot work
        #check again...
        #M = np.multiply(np.asarray(pos_diff),np.asarray(self.prices))
        portfolio['cost'] = np.multiply(pos_diff.values,self.prices.values)
       # portfolio['cost2']= portfolio['cost'].sum(axis=0)
        portfolio['cost2']=portfolio['cost'].cumsum(axis=0)
        portfolio['cash2'] = self.initial_capital - portfolio['cost2']
        # Sum up the cash and holdings to create full account ‘equity’, then create the percentage returns
        portfolio['total'] = portfolio['cash2'] + portfolio['holdings']
        portfolio['returns'] = portfolio['total'].pct_change()
        return portfolio

if __name__ == "__main__":
    window = 6
    stkprice = sp500data
    table = signal_on_rank(sp500data, 0.1, window)
    #shorttable = signal_on_rank(sp500data, "tail", 0.1, window)

    stklist = list(sp500data.columns.values)
    pnl = pd.DataFrame(index=stklist)
    for col in range(len(stklist)-1):
        stklist[col]
        skewnessport = portfolio(table[stklist[col]],100,stkprice[stklist[col]])
        skewnessport.backtest_portfolio()
        #skewnessport2 = portfolio(shorttable[stklist[col]], 100, stkprice[stklist[col]])
        #skewnessport2.backtest_portfolio()
        print skewnessport.backtest_portfolio()
