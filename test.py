#coding: utf-8
#main function
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
