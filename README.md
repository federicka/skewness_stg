# skewness_stg

#strategy based on rolling skewness

#main function: test.py
#data.py -- historical price stored in dataframe noe just for clode price, can change it...
#algo.py -- function that generate skewness ranking and form a dict with keys to be date, value is list of tuple(sharename,signal)
#portfolio.py -- class that enumerate through certain period defined by the historical data date index and then calculate the portflio pnl
