import pandas as pd
import numpy as np
import datetime
from datetime import timedelta, datetime

#write the porofolio class to calculate everyday return with rolling asset
class portfolio:

    def __init__(self,signal,init_cap,prices,datelist):
        self.prices=prices
        self.positions = algorithm_signal #dict keys: date
        self.dates = datelist

    def backtest_portfolio(self):
        #iterate through all days for strategy
        portfolio = []
        for idx, val in enumerate(self.datelist):
            names = np.array(['date','prev_holding','pos_diff','chg','return'])
            today_pos = self.positions[idx]
            prev_pos =self.positions[idx-1]
            todaypos_val = [x[2] for x in today_pos]
            prevpos_val = [x[2] for x in prev_pos]
            prev_holding = np.dot(todaypos_val, self.prices.values[idx-1])#everyday holding for all equity
            pos_diff = todaypos_val-prevpos_val
            delta_chg = pos_diff * (self.price.values[idx] - self.price.values[idx-1])
            portfolio.append([val,prev_holding,pos_diff,delta_chg,delta_chg/prev_holding])

        return portfolio