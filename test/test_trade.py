import unittest
import sys
sys.path.append("..")
from resources.trade import *
from resources.account import *
from resources.order import *
from resources.signal import *
from common.scaffold import *
import copy

class MyTestCase(unittest.TestCase):
    def test_case1(self):

        config = parse_config()
        format_logging(config)

        mode = 'allin'
        trade_limit = 'both'
        trade = Trade(mode='test')
        account = Account(mode='test')
        orders = list()
        accounts = list()
        account.get_account('huobi','20190522', get_basic_currency('btc'), 10)
        self.assertEqual(get_value_from_dict(account.spot_account.account, 'huobi', get_basic_currency('btc'), 'value'),10)

        signal1 = SignalMA('huobi', 'btc', 'buy', 1, '20190522', 1, 2 , 2, 1)
        signal2 = SignalMA('huobi', 'btc', 'sell', 2, '20190523', 1, 2, 2, 1)
        signal3 = SignalMA('huobi', 'btc', 'buy', 1, '20190524', 1, 2, 2, 1)
        signal4 = SignalMA('huobi', 'btc', 'sell', 2, '20190525', 1, 2, 2, 1)
        signals = list([signal1, signal2, signal3, signal4])

        for signal in signals:
            order = Order.create_orders(mode=mode,
                                        trade_limit=trade_limit,
                                        account=account,
                                        signal=signal,
                                        fee=0.02)
            orders.extend(order)
            j = 1
            for i in order:
                print('seq : {} ------------------------------------'.format(j))
                j += 1
                transaction, account = trade.trade(i, account, fee=0.02)
                accounts.append(copy.deepcopy(account))
                print('order: \n')
                i.desc()
                print('\n')
                print('transaction: \n')
                transaction.desc()
                print('\n')
                print('account: \n')
                account.desc()
                print('\n')
                print('----------------------------------------------')
                print('\n\n\n')

        if trade_limit == 'both':
            self.assertEqual(len(orders), 7)
            self.assertEqual(len(accounts), 7)
        elif trade_limit == 'buy':
            self.assertEqual(len(orders), 4)
        else:
            self.assertEqual(len(orders), 3)

        if trade_limit == 'both':
            self.assertEqual(orders[0].amount_of_object, 10)
            self.assertEqual(orders[0].object_type, 'spot')
            self.assertEqual(orders[0].price, 1)
            self.assertEqual(orders[0].object_action, 'buy')

            self.assertEqual(orders[1].amount_of_object, 9.8)
            self.assertEqual(orders[1].object_type, 'spot')
            self.assertEqual(orders[1].price, 2)
            self.assertEqual(orders[1].object_action, 'sell')

            self.assertEqual(orders[2].amount_of_object, 9.604)
            self.assertEqual(orders[2].object_type, 'futures')
            self.assertEqual(orders[2].price, 2)
            self.assertEqual(orders[2].object_action, 'buy')
            self.assertEqual(orders[2].futures_action, 'sell')

            self.assertEqual(orders[3].amount_of_object, 9.411919999999999)
            self.assertEqual(orders[3].object_type, 'futures')
            self.assertEqual(orders[3].price, 1)
            self.assertEqual(orders[3].object_action, 'sell')
            self.assertEqual(orders[3].futures_action, 'sell')

            self.assertEqual(orders[4].amount_of_object, 27.671)
            self.assertEqual(orders[4].object_type, 'spot')
            self.assertEqual(orders[4].price, 1)
            self.assertEqual(orders[4].object_action, 'buy')

            self.assertEqual(orders[5].amount_of_object, 27.11758)
            self.assertEqual(orders[5].object_type, 'spot')
            self.assertEqual(orders[5].price, 2)
            self.assertEqual(orders[5].object_action, 'sell')

            self.assertEqual(orders[6].amount_of_object, 26.5752)
            self.assertEqual(orders[6].object_type, 'futures')
            self.assertEqual(orders[6].price, 2)
            self.assertEqual(orders[6].object_action, 'buy')
            self.assertEqual(orders[6].futures_action, 'sell')

            self.assertEqual(accounts[0].spot_account.account['huobi']['ustd']['value'], 0.0)
            self.assertEqual(accounts[0].spot_account.account['huobi']['btc']['value'], 9.8)

            self.assertEqual(accounts[1].spot_account.account['huobi']['ustd']['value'], 19.208000000000002)
            self.assertEqual(accounts[1].spot_account.account['huobi']['btc']['value'], 0.0)

            self.assertEqual(accounts[2].spot_account.account['huobi']['ustd']['value'], 3.552713678800501e-15)
            self.assertEqual(accounts[2].spot_account.account['huobi']['btc']['value'], 0.0)
            self.assertEqual(accounts[2].futures_account.account['huobi']['btc'][0]['value'], 9.411919999999999)

            self.assertEqual(accounts[3].spot_account.account['huobi']['ustd']['value'], 27.671044799999997)
            self.assertEqual(accounts[3].spot_account.account['huobi']['btc']['value'], 0.0)
            self.assertEqual(accounts[3].futures_account.account['huobi']['btc'][0]['value'], 0.0)

            self.assertEqual(accounts[4].spot_account.account['huobi']['ustd']['value'], 4.479999999773554e-05)
            self.assertEqual(accounts[4].spot_account.account['huobi']['btc']['value'],  27.11758)
            self.assertEqual(accounts[4].futures_account.account['huobi']['btc'][0]['value'], 0.0)

            self.assertEqual(accounts[5].spot_account.account['huobi']['ustd']['value'], 53.1505016)
            self.assertEqual(accounts[5].spot_account.account['huobi']['btc']['value'],  0.0)
            self.assertEqual(accounts[5].futures_account.account['huobi']['btc'][0]['value'], 0.0)

            self.assertEqual(accounts[6].spot_account.account['huobi']['ustd']['value'], 0.00010160000000070113)
            self.assertEqual(accounts[6].spot_account.account['huobi']['btc']['value'],  0.0)
            self.assertEqual(accounts[6].futures_account.account['huobi']['btc'][0]['value'], 26.043695999999997)

if __name__ == '__main__':
    unittest.main()
