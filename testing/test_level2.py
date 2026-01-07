import unittest
from calculator import Calculator

class TestOperations(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator(8,2)

    def test_sum(self):
        sum = self.calc.get_sum()      
        print (f'Test Results: \n The answer was {sum}.')
        self.assertEqual(sum, 10, 'The Answer was not 10')

    #test difference
    def test_diff(self):
        diff = self.calc.get_difference()
        print (f'Test Results: \n  The answer was {diff}.')
        self.assertEqual(diff, 6, 'The Answer was not 6')


if __name__ == '__main__':
    unittest.main()