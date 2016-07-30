from pandas import *
import pandas as pd
from yahoo_finance import Share
import datetime
from datetime import timedelta, datetime

dailytrade = pd.read_csv(r"/Users/mengdantian/Downloads/20160512orders-3.csv", names=["Symbol", "triggerPos", "triggerPrice"])
startdate="2016-05-10"
enddate = "2016-05-12"
folder = r"/Users/mengdantian/Dropbox/mengdan/analysis/"


def addToList(list, str_to_add):
    if str_to_add not in list:
        list.append(str_to_add)


class file_reader():

    def __init__(self,folder,startdate,enddate):
        self.folder = folder
        self.startdate = startdate
        self.enddate = enddate

    def get_stklist(self):
        start = datetime.strptime(self.startdate, '%Y-%m-%d')
        end = datetime.strptime(self.enddate, '%Y-%m-%d')
        delta = (end-start).days+1
        print delta
        stk=[]
        folder = self.folder
        for deltatime in range(delta):
            date = start + timedelta(deltatime)
            date = date.strftime("%Y%m%d")
            path = folder+date+'orders.csv'
            new = pd.read_csv(path,names =["Symbol", "triggerPos", "triggerPrice"])
            newstk = list(new['Symbol'])
            for str in newstk:
                addToList(stk, str)
            self.stk = stk
            return self.stk


def get_share(x,startdate,enddate):
    temp = Share(x).get_historical(startdate,enddate)[0]
    return temp['Open'],temp['High'],temp['Low'],temp['Adj_Close']


his = file_reader(folder,startdate,enddate)
stklist = his.get_stklist()
historical_price ={k:get_share(k,startdate,enddate) for k in stklist}
print historical_price[stklist[1]].info()
'''

def dailysingnal(x):
    dailyinfo = historical_price[x]
    #   x['signal'] = np.where(np.logical_or(float(x['triggerPrice'])>float(dailyinfo[2]),float(x['triggerPrice'])<float(dailyinfo[1])),x['triggerPos'],0)
        return x['signal']'''





