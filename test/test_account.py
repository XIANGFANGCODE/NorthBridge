import unittest
import sys
sys.path.append("..")
from resources.account import *


class MyTestCase(unittest.TestCase):
    def test_something(self):
        account = Account('test')
        account.get_account(exchange='tushare', object='ustd', datetime='20190501', start_account=100000)
        account.desc()
        self.assertEqual(account.spot_account.account['tushare']['ustd'], 100000)


if __name__ == '__main__':
    unittest.main()
