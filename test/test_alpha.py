import unittest
import sys
sys.path.append("..")
from resources.alpha import *


class MyTestCase(unittest.TestCase):
    def test_something(self):
        alpha = Alpha('test')
        signals = alpha.moving_average(short_num=5,
                             long_num=30,
                             object='btc',
                             exchange='tushare')
        print(len(signals))
        for i in range(10):
            print(signals[i].desc())
        self.assertGreaterEqual(len(signals), 0)


if __name__ == '__main__':
    unittest.main()
