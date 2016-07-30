import pandas as pd
import numpy as np
from yahoo_finance import Share
import datetime
from datetime import timedelta, datetime

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
        result.append(val,signaltable.iloc[date][val])

    return result

datelist = data.index#use the sp500data index as the datelist for simplity reason
algorithm_signal = {k: getsignal(signaltable, k, shares) for k in datelist}





