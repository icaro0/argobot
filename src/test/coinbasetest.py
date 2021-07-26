import unittest
from config import *
from exchanges import *

class CoinbaseWrapperTest(unittest.TestCase):

    def setUp(self):
        """... code to execute in preparation for tests ..."""
        self.client = AuthenticatedCoinBaseCommunicationWrapper(coinbase_api_key, coinbase_api_secret, coinbase_api_passphrase)
    def tearDown(self) -> None:
        self.client.closeSession()
    def test_conection(self):
        print(self.client.client.get_accounts())
    def test_getActualPrice(self):
        print(self.client.getActualPrice('BTC-EUR'))
    def test_buy(self):
        print(self.client.buy('BTC-EUR', size=('0.01')))
    def test_sell(self):
        print(self.client.sell('BTC-EUR', size=('0.01')))
if __name__ == '__main__':
    unittest.main()