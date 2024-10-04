import os
import unittest
import pandas as pd
import numpy as np

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)

from src.data_validation import compare_numeric_cols, compare_categorical_cols, compare_shapes 

class TestComparisonFunctions(unittest.TestCase):

    def setUp(self):
        # sample numeric data
        self.df_numeric_1 = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [5, 6, 7, 8, 9]
        })
        self.df_numeric_2 = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [5, 6, 7, 8, 10]
        })

        # Sample categorical data
        self.df_categorical_1 = pd.DataFrame({
            'C': ['a', 'b', 'a', 'c', 'b'],
            'D': ['x', 'y', 'x', 'x', 'y']
        })
        self.df_categorical_2 = pd.DataFrame({
            'C': ['a', 'b', 'b', 'c', 'c'],
            'D': ['x', 'y', 'y', 'x', 'x']
        })

    def test_compare_numeric_cols(self):
        result = compare_numeric_cols(self.df_numeric_1, self.df_numeric_2)
        expected_columns = ['count_1', 'count_2', 'mean_1', 'mean_2', 'min_1', 'min_2', 'max_1', 'max_2']
        self.assertTrue(all(col in result.columns for col in expected_columns))

        # test mean 
        self.assertEqual(result.loc['A', 'mean_1'], 3.0)
        self.assertEqual(result.loc['B', 'mean_2'], 7.2)

        # test count
        self.assertEqual(result.loc['A', 'count_1'],  result.loc['B', 'count_2'])

        # test min
        self.assertEqual(result.loc['A', 'min_1'], 1.0)
        self.assertEqual(result.loc['B', 'min_2'], 5.0)

        # test max
        self.assertEqual(result.loc['A', 'max_1'], 5.0)
        self.assertEqual(result.loc['B', 'max_2'], 10.0)

    def test_compare_categorical_cols(self):
        avg_freq_ratio, freq_diff = compare_categorical_cols(self.df_categorical_1, self.df_categorical_2)
        
        self.assertAlmostEqual(avg_freq_ratio['C'], 1.1667, places=4)  # average frequency ratio
        self.assertIn('C', freq_diff)
        self.assertIn('D', freq_diff)
    
        # assert dtype of freq_diff
        self.assertEqual(type(freq_diff), dict)

        # assert dtype of value within freq_diff
        self.assertEqual(type(freq_diff['C']), pd.DataFrame)

    def test_compare_shapes(self):
        # print output
        from io import StringIO
        import sys

        captured_output = StringIO()
        sys.stdout = captured_output  # redirect stdout
        compare_shapes(self.df_numeric_1, self.df_numeric_2)
        sys.stdout = sys.__stdout__  # reset redirect

        output = captured_output.getvalue()
        self.assertIn('PROD: (5, 2)', output)
        self.assertIn('DEV: (5, 2)', output)

if __name__ == '__main__':
    unittest.main()
