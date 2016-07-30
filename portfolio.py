import pandas as pd
import numpy as np
import datetime
from datetime import timedelta, datetime

#write the porofolio class to calculate everyday return with rolling asset
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

