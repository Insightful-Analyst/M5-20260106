import unittest
import pandas as pd
from app_refactored import enrich_dateDuration

class TestOperations(unittest.TestCase):
    def setUp(self):
        self.test_df = pd.DataFrame({
            'checkout_date': pd.to_datetime(['15/12/2025', '01/01/2026', '10/01/2026'], dayfirst=True),
            'return_date': pd.to_datetime(['07/01/2026', '05/01/2026', '08/01/2026'], dayfirst=True)
        })

    # Test that date_delta is calculated correctly
    def test_date_delta_calc(self):
        result = enrich_dateDuration('checkout_date', 'return_date', self.test_df)

        #first row
        print ('First row enrich_dateDuration calculated correctly')
        self.assertEqual(result.loc[0,'date_delta'], 23)
        #second row
        print ('Second row enrich_dateDuration calculated correctly')
        self.assertEqual(result.loc[1,'date_delta'], 4)

    def test_valid_loan_flag_true(self):
        result = enrich_dateDuration('checkout_date', 'return_date', self.test_df)
        
        #first row
        print ('First row valid loan flag True calculated correctly')
        self.assertTrue(result.loc[0,'valid_loan_flag'])
        #second row
        print ('First row valid loan flag True calculated correctly')
        self.assertTrue(result.loc[1,'valid_loan_flag'])

    def test_valid_loan_flag_false(self):
        invalid_df = pd.DataFrame({
            'checkout_date':pd.to_datetime(['15/12/2025'], dayfirst=True),
            'return_date':pd.to_datetime(['01/12/2025'], dayfirst=True)
        })
        
        result = enrich_dateDuration('checkout_date', 'return_date', invalid_df)

        print('Valid loan flag False calculated correctly')
        self.assertFalse(result.loc[0, 'valid_loan_flag'])
        print('Negative date_delta calculated correctly')
        self.assertTrue(result.loc[0,'date_delta'] < 0)

if __name__ == '__main__':
    unittest.main()

