import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        d = dict()
        print(type(d.get('hello',0)))
        print(d.get('hello', 0))
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
