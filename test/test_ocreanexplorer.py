import unittest
import os
import sys
sys.path.append("..")
from resources.oceanexplorer import *


class MyTestCase(unittest.TestCase):
    def test_get_btc_pricevol_by_tushare(self):
        file = get_btc_pricevol_by_tushare(start_date='20120101')
        self.assertEqual(file, "E:\\NorthBridge\\data\digital_cash\\btc_history_from_tushare.csv")
        self.assertEqual(os.path.exists(file),True)

if __name__ == '__main__':
    unittest.main()
