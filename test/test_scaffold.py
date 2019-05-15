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

    def test_logging(self):
        config = {'logging_level': 'DEBUG'}
        format_logging(config)
        logging.debug("it is debug")
        logging.error("it is error")

        self.assertEqual(True, True)

    def test_get_basic_currency(self):
        self.assertEqual(get_basic_currency('btc'), 'ustd')

    def test_get_value_from_dict(self):
        d = dict()
        d['first'] = dict()
        d['first']['second'] = 'third'
        self.assertEqual(get_value_from_dict(d, 'first', 'second'),'third')



if __name__ == '__main__':
    unittest.main()
