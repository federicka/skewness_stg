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

#get all data and get skewness stats
sp500stk = []
for x in sp500list['free_code'][:50]:
    stk= get_share_close(x)
    sp500stk.append(stk)

sp500data = pd.concat(sp500stk,ignore_index=False,axis=1)