import unittest
import sys
sys.path.append("..")
from resources.trade import *
from resources.account import *
from resources.order import *
from resources.signal import *
from common.scaffold import *


class MyTestCase(unittest.TestCase):
    def test_something(self):
        print(tranc_float(0.123456,4))


if __name__ == '__main__':
    unittest.main()
