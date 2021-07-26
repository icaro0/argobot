from time import sleep
import datetime
import numpy as np
import pandas as pd
import talib
from decimal import *
from communications import Mail
from config import *
from exchanges import *
from entities import Signal

class Arbobot:
    def __init__(self, product_id='BTC-EUR', default_buy_size='0.00001', default_sell_size='0.00001', interval=900, trade_wrapper=None, communication_wrapper=None, automatic_orders = False) -> None:
        self.interval = interval
        if(trade_wrapper is not None):
            self.trade_wrapper = trade_wrapper
        else:
            self.trade_wrapper = CoinBaseCommunicationsWrapper()
        if(communication_wrapper is not None):
            self.communication_wrapper = communication_wrapper
        else:
            self.communication_wrapper = Mail(username, password)
        self.automatic_orders = automatic_orders
        self.product_id = product_id
        self.default_buy_size = default_buy_size
        self.default_sell_size = default_sell_size
    def sell(self, signal):
        msg = 'day {} sell signal detected: {}'.format(signal.time, signal.close)
        self.communication_wrapper(username, username, msg, msg)
        if(self.automatic_orders):
            results = self.trade_wrapper.sell(self.product_id, size=self.default_sell_size)
            print(results)
            return results
        return None
        
    def buy(self, signal):
        msg = 'day {} buy signal detected: {}'.format(signal.time, signal.close)
        self.communication_wrapper(username, username, msg, msg)
        if(self.automatic_orders):
            results = self.trade_wrapper.buy(self.product_id, size=self.default_buy_size)
            print(results)
            return results
        return None
        
    def convertHistoricDataToDataframe(self, history):
        df = pd.DataFrame({'Date':[n['time'] for n in history], 'Close':[float(n['close']) for n in history]})
        df['Date'] = pd.to_datetime(df['Date'], unit='s')
        df.set_index('Date',inplace=True)
        dti = df.index.tz_localize("UTC")
        df.index = dti.tz_convert("Europe/Madrid")
        df = df.sort_index()
        return df
    #calculamos las señales de compra
    def implement_macd_strategy(self, prices, data):    
        buy_price = []
        sell_price = []
        macd_signal = []
        signal = 0
        for i in range(len(data)):
            if (data['macd'][i] > data['signal'][i]):
                if signal != 1:
                    buy_price.append(prices[i])
                    sell_price.append(np.nan)
                    signal = 1
                    macd_signal.append(signal)
                else:
                    buy_price.append(np.nan)
                    sell_price.append(np.nan)
                    macd_signal.append(0)
            elif (data['macd'][i] < data['signal'][i]):
                if signal != -1:
                    buy_price.append(np.nan)
                    sell_price.append(prices[i])
                    signal = -1
                    macd_signal.append(signal)
                else:
                    buy_price.append(np.nan)
                    sell_price.append(np.nan)
                    macd_signal.append(0)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                macd_signal.append(0)
                
        return buy_price, sell_price, macd_signal

    def calculateMACD(self,df):
        macd, signal, hist = talib.MACD(df['Close'], 
                                    fastperiod=9, slowperiod=12, signalperiod=24)
        df['macd'] = macd
        df['signal'] = signal
        return df
    def calculateIndicators(self,df):
        df = self.calculateMACD(df)
        buy_price, sell_price, macd_signal = self.implement_macd_strategy(df['Close'], df)
        df['buy'] = buy_price
        df['sell'] = sell_price
        return df
    def calculateBuySellSignals(self,n):
        n = self.calculateIndicators(n)
        ele = n.tail(1)
        if(ele['sell'][0] >0):
            #print('day {} sell signal detected: {}'.format(ele.index.to_pydatetime()[0].isoformat(),ele['sell'][0]))
            return Signal('sell', ele['sell'][0], ele.index.to_pydatetime()[0].isoformat())
        if(ele['buy'][0] >0):
            #print('day {} buy signal detected: {}'.format(ele.index.to_pydatetime()[0].isoformat(),ele['buy'][0]))
            return Signal('buy', ele['buy'][0], ele.index.to_pydatetime()[0].isoformat())
        return None
    
    def start(self)-> None:
        while True:
            start = datetime.datetime.now() - datetime.timedelta(days = 3)
            end = datetime.datetime.now()
            history = self.trade_wrapper.getHistory(start = start, end = end)
            print("trading calculation...")
            df = self.convertHistoricDataToDataframe(history)
            signal = self.calculateBuySellSignals(df)
            if(signal is not None and signal.type=='sell'):
                self.sell(signal)
            elif(signal is not None and signal.type=='buy'):
                self.buy(signal)
            else:
                print('No signal detected')
            sleep(self.interval)

if __name__=='__main__':
    bot = Arbobot()
    #bot = Arbobot(trade_wrapper=AuthenticatedCoinBaseCommunicationWrapper(coinbase_api_key, coinbase_api_secret, coinbase_api_passphrase), automatic_orders=True)
    bot.start()