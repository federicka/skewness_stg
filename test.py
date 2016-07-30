#coding: utf-8
#main function
import quandl
import pandas as pd
import numpy as np
import math as m

quandl.ApiConfig.api_key = 'ACKX-sC87Evgmif6miSm'

sp500list = pd.read_csv(r"/Users/mengdantian/Downloads/sp500.csv")
#functions get Close price, log return, skewnss
def get_share_close(x):
    y = quandl.get([x],start_date="2014-06-26",end_date="2016-06-30")
   # y = quandl.get([x])
    y = y[y.keys()[3]]
    return y

#get all data and get skewness stats
sp500stk = []
for x in sp500list['free_code'][:50]:
    stk= get_share_close(x)
    sp500stk.append(stk)

sp500data = pd.concat(sp500stk,ignore_index=False,axis=1)


def daily_ret(x):
    ret = x/x.shift(1)
    return np.log(ret)

def skewness(x):
    t = daily_ret(x)
    meanret =t.mean()
    std = t.std()
    skew = np.mean(np.power((t - meanret),3)) / np.power(std,3)
    return skew

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

#date as key, value is a tuple(sharename, position)

def getsignal(signaltable, date, shares):
    #shares should be a stock name list
    result =[]
    for idx, val in enumerate(shares):
        result.append((val,signaltable.loc[date,val]))

    return result


class portfolio:

    def __init__(self,signal,initial_cap,prices,datelist):
        self.prices=prices
        self.positions = algorithm_signal #dict keys: date
        self.dates = datelist
        self.initial_cap = initial_cap

    def backtest_portfolio(self):
        #iterate through all days for strategy
        portfolio = []
        for idx, val in enumerate(self.dates):
            names = np.array(['date','prev_total','chg','return'])
            today_pos = self.positions[val]#access by keys, which is date
            prev_pos =self.positions[self.dates[idx-1]]
            todaypos_val = [x[1] for x in today_pos]
            prevpos_val = [x[1] for x in prev_pos]
            #data structure of price should be notics
            pos_diff = np.array(todaypos_val) - np.array(prevpos_val)
            A = np.array(self.prices.iloc[idx])
            B = np.array(self.prices.iloc[idx-1])
            A[np.isnan(A)] = 0
            B[np.isnan(B)] = 0
            delta_chg = np.dot(pos_diff,(A-B))
            if idx == 0:
                prev_total = self.initial_cap
            else:
                prev_total = prev_total + delta_chg

            #pos_diff = np.array(todaypos_val)-np.array(prevpos_val)
            #delta_chg = np.dot(pos_diff, (np.array(self.prices.iloc[idx]) - np.array(self.prices.iloc[idx-1])))
            if idx == 0:
                logret = 0
            else:
                logret = m.log(1+delta_chg/prev_total)
            portfolio.append([val,prev_total,delta_chg,logret])

        return portfolio






if __name__ == "__main__":
    window = 6
    stkprice = sp500data
    table = signal_on_rank(sp500data, 0.1, window)
    #shorttable = signal_on_rank(sp500data, "tail", 0.1, window)

    stklist = list(sp500data.columns.values)
    datelist = sp500data.index  # use the sp500data index as the datelist for simplity reason
    algorithm_signal = {k: getsignal(table, k, stklist) for k in datelist}

    backtesting = portfolio(table,10000,stkprice,datelist)
    backtesting.backtest_portfolio()
    print backtesting.backtest_portfolio()


'''
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
'''
