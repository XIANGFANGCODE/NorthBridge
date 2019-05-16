import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        k = [1, 2, 3]
        k.extend([2,3,4])
        f = list()
        k.extend(f)
        print(k)


if __name__ == '__main__':
    unittest.main()
