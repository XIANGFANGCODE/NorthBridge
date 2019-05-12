import unittest
import sys
sys.path.append("..")
from common.scaffold import *


class MyTestCase(unittest.TestCase):
    def test_something(self):
        config = parse_config()
        for key in config:
            print('key : {}, value : {}'.format(key, config[key]))
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
