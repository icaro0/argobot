import unittest
import datetime
from argobot import *
import pandas as pd
import time
DEFAULT_TIME_STEPS = (4*24)*7
def create_dataset(X, time_steps=DEFAULT_TIME_STEPS):
    Xs =[]
    for i in range(len(X) - time_steps):
        v = X.iloc[i:(i + time_steps)]
        Xs.append(v)
    return Xs
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
        


def calculateRevenue(revenues):
    if revenues[0].type == 'sell':
        revenues = revenues[1:]
    if revenues[-1].type == 'buy':
        revenues.pop()
    total_revenieu = 0
    for n in list(chunks(revenues, 2)):
        rev = ((n[1].close-n[0].close)/n[0].close)*100
        total_revenieu = total_revenieu + rev
        print('revenue: {}'.format(rev))
    print('total: {}'.format(total_revenieu))

class MyTestCase1(unittest.TestCase):

    def setUp(self):
        """... code to execute in preparation for tests ..."""
        self.bot = Arbobot()
    def tearDown(self) -> None:
        self.bot.trade_wrapper.closeSession()

    # def test_back_testing(self):
    #     start = datetime.datetime.now() - datetime.timedelta(days = 3)
    #     end = datetime.datetime.now()
    #     hslot10 = self.bot.trade_wrapper.getHistory(start = start, end = end)
    #     dataset = create_dataset(self.bot.convertHistoricDataToDataframe(hslot10))
    #     ##iterate over slots of 48 hours
    #     for n in dataset:
    #         self.bot.calculateBuySellSignals(n)

    # def test_back_testing_10_days_sell_retries(self):
    #     start = datetime.datetime.now() - datetime.timedelta(days = 1)
    #     end = datetime.datetime.now()
    #     trade_slot = []
    #     for n in range(1,100):
    #         df = self.bot.convertHistoricDataToDataframe(self.bot.trade_wrapper.getHistory(start = start, end = end))
    #         trade_slot.append(df)
    #         end = start
    #         start = end - datetime.timedelta(days = 1)
    #     df = pd.concat(trade_slot)
    #     df = df.sort_index()
    #     dataset = create_dataset(df)
    #     ##iterate over slots of 48 hours
    #     purchases = []
    #     for n in dataset:
    #         purchases.append(self.bot.calculateBuySellSignals(n))
    #     purchases = [n for n in purchases if n is not None]
    #     last_buy = None
    #     sell_tries = 2
    #     for n in purchases:
    #         if(last_buy is not None and n.type=='sell' and last_buy.close < n.close):
    #             print('{},{},{}'.format(n.time,n.type,n.close))
    #             last_buy = None
    #         if(last_buy is not None and n.type == 'sell'):
    #             if(sell_tries<=0):
    #                 sell_tries = 2
    #                 last_buy = None
    #                 print('{},{},{}'.format(n.time,n.type,n.close))
    #             else:
    #                 sell_tries=sell_tries-1
    #         if(last_buy is None and n.type=='buy'):
    #             print('{},{},{}'.format(n.time,n.type,n.close))
    #             last_buy = n
    #         if(sell_tries<=0):
    #             sell_tries = 2
    #             last_buy = None
    #             print('{},{},{}'.format(n.time,n.type,n.close))
    def test_back_testing_10_days(self):
        start = datetime.datetime.now() - datetime.timedelta(days = 1)
        end = datetime.datetime.now()
        trade_slot = []
        for n in range(1,100):
            df = self.bot.convertHistoricDataToDataframe(self.bot.trade_wrapper.getHistory(start = start, end = end))
            trade_slot.append(df)
            end = start
            start = end - datetime.timedelta(days = 1)
        df = pd.concat(trade_slot)
        df = df.sort_index()
        dataset = create_dataset(df)
        ##iterate over slots of 48 hours
        purchases = []
        for n in dataset:
            purchases.append(self.bot.calculateBuySellSignals(n))
        purchases = [n for n in purchases if n is not None]
        for n in purchases:
            print('{},{},{}'.format(n.time,n.type,n.close))
if __name__ == '__main__':
    unittest.main()