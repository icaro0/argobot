import coinbasepro as cbp
import datetime

class CoinBaseCommunicationsWrapper:
    def __init__(self) -> None:
        self.client = cbp.PublicClient(api_url='https://api-public.sandbox.pro.coinbase.com')
    def getActualPrice(self, product_id='BTC-EUR'):
        return self.client.get_product_ticker(product_id=product_id)
    def getHistory(self, product_id = 'BTC-EUR', start = datetime.datetime.now() - datetime.timedelta(days = 3), end=datetime.datetime.now(), granularity=900):
        return self.client.get_product_historic_rates(product_id=product_id, start= start.isoformat(), stop=end.isoformat(), granularity = granularity)
    def closeSession(self):
        self.client.session.close()

class AuthenticatedCoinBaseCommunicationWrapper(CoinBaseCommunicationsWrapper):
    def __init__(self, key, secret, passphrase) -> None:
        super().__init__()
        self.client = cbp.AuthenticatedClient(key, secret, passphrase, api_url='https://api-public.sandbox.pro.coinbase.com')
    def buy(self, product_id = 'BTC-EUR', size='0.0001'):
        return self.client.place_order(product_id, 'buy', 'market', size=size)
    def sell(self, product_id = 'BTC-EUR', size='0.0001'):
        return self.client.place_order(product_id, 'sell', 'market', size=size)

