import unittest
import sys
sys.path.append("..")
from resources.order import *


class MyTestCase(unittest.TestCase):
    def test_something(self):
        orders = Order.create_orders('no', 'both', 'account', 'signal')
        for i in orders:
            i.desc()
        self.assertEqual(len(orders), 2)

if __name__ == '__main__':
    unittest.main()
