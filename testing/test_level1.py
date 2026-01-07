import unittest
from calculator import Calculator

class TestOperations(unittest.TestCase):

    def test_sum(self):
        calc = Calculator (8,2)
        answer = calc.get_sum()
        print (f'Test Results: \n The answer was {answer}.')
        self.assertEqual(answer, 10, "The answer wasn't 10.")

    def test_difference(self):
        calc = Calculator (8,2)
        answer = calc.get_difference()
        print (f'Test Results: \n The answer was {answer}.')
        self.assertEqual(answer, 6, "The answer wasn't 6.")

    def test_product(self):
        calc = Calculator (8,2)
        answer = calc.get_product()
        print (f'Test Results: \n The answer was {answer}.')
        self.assertEqual(answer, 16, "The answer wasn't 16.")

    def test_quotient(self):
        calc = Calculator (8,2)
        answer = calc.get_quotient()
        print (f'Test Results: \n The answer was {answer}.')
        self.assertEqual(answer, 4, "The answer wasn't 4.")

if __name__ == "__main__":
    unittest.main()