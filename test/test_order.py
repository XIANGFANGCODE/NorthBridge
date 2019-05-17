import unittest
import sys
sys.path.append("..")
from common.scaffold import *
from resources.order import *
from resources.account import *
from resources.signal import *

class MyTestCase(unittest.TestCase):
    def test_case1(self):
        print("----------------------test_case1 begin------------------------")
        mode = 'allin'
        trade_limit = 'sell'
        account = Account('test')
        account.get_account('huobi','20190517', get_basic_currency('btc'), 100000)
        signal = SignalMA(1, 'huobi', 'btc', 'buy', 100, '20190517', 1, 2 , 2, 1)
        orders = Order.create_orders(mode, trade_limit, account, signal)
        for order in orders:
            order.desc()
        self.assertEqual(len(orders), 1)
        print("----------------------test_case1 end------------------------")
        print("")

    def test_case2(self):
        print("----------------------test_case2 begin------------------------")
        mode = 'allin'
        trade_limit = 'buy'
        account = Account('test')
        account.get_account('huobi','20190517', get_basic_currency('btc'), 100000)
        signal = SignalMA(1, 'huobi', 'btc', 'sell', 100, '20190517', 1, 2 , 2, 1)
        orders = Order.create_orders(mode, trade_limit, account, signal)
        for order in orders:
            order.desc()
        self.assertEqual(len(orders), 0)
        print("----------------------test_case2 end------------------------")
        print("")

    def test_case3(self):
        print("----------------------test_case3 begin------------------------")
        mode = 'allin'
        trade_limit = 'both'
        account = Account('test')
        account.get_account('huobi','20190517', get_basic_currency('btc'), 100000)
        signal = SignalMA(1, 'huobi', 'btc', 'sell', 100, '20190517', 1, 2 , 2, 1)
        orders = Order.create_orders(mode, trade_limit, account, signal)
        for order in orders:
            order.desc()
        self.assertEqual(len(orders), 1)
        print("----------------------test_case3 end------------------------")
        print("")

    def test_case4(self):
        print("----------------------test_case4 begin------------------------")
        mode = 'allin'
        trade_limit = 'both'
        account = Account('test')
        account.get_account('huobi','20190517', get_basic_currency('btc'), 100000)
        signal1 = SignalMA(1, 'huobi', 'btc', 'buy', 100, '20190517', 1, 2 , 2, 1)
        signal2 = SignalMA(1, 'huobi', 'btc', 'sell', 200, '20190517', 1, 2, 2, 1)
        signal3 = SignalMA(1, 'huobi', 'btc', 'buy', 100, '20190517', 1, 2, 2, 1)
        signal4 = SignalMA(1, 'huobi', 'btc', 'sell', 200, '20190517', 1, 2, 2, 1)
        signals = list([signal1, signal2, signal3, signal4])
        orders = list()
        for signal in signals:
            ods = Order.create_orders(mode, trade_limit, account, signal)
            orders.extend(ods)
        for order in orders:
            order.desc()
        self.assertEqual(len(orders), 1)
        print("----------------------test_case4 end------------------------")
        print("")


if __name__ == '__main__':
    unittest.main()
