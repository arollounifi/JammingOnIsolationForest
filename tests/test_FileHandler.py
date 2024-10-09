import unittest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from io import StringIO
from FileHandler import FileHandler


class TestFileHandler(unittest.TestCase):

    @patch('pandas.read_csv')
    def test_readFile_success(self, mock_read_csv):
        # Mocking the return value of pd.read_csv
        mock_data = pd.DataFrame({'rssi': [-50, -45, -60]})
        mock_read_csv.return_value = mock_data

        # Call the method and check results
        result = FileHandler._readFile('dummy.csv', 3)
        pd.testing.assert_frame_equal(result, mock_data)

    @patch('pandas.read_csv')
    def test_readFile_empty_file(self, mock_read_csv):
        # Simulate an empty dataframe being returned by read_csv
        mock_read_csv.return_value = pd.DataFrame(columns=['rssi'])

        # Check that FileNotFoundError is raised
        with self.assertRaises(FileNotFoundError):
            FileHandler._readFile('empty.csv', 3)

    def test_parseData_success(self):
        # Input data simulates RSSI values
        input_data = pd.Series([-50, -45, -60])

        # Expected result is a NumPy array with the adjustment of -95
        expected_output = np.array([[-50], [-45], [-60]]) - 95

        # Call the method
        result = FileHandler._parseData(pd.DataFrame({'rssi': input_data}))

        # Check if result matches the expected output
        np.testing.assert_array_equal(result, expected_output)

    @patch('pandas.read_csv')
    def test_readAndParseFile_integration(self, mock_read_csv):
        # Mocking read_csv for integration test
        mock_data = pd.DataFrame({'rssi': [-50, -45, -60]})
        mock_read_csv.return_value = mock_data

        # Expected parsed output
        expected_output = np.array([[-50], [-45], [-60]])

        # Call the integrated method
        result = FileHandler.readAndParseFile('dummy.csv', 3)

        # Check the final result matches the expected parsed data
        np.testing.assert_array_equal(result, expected_output)


if __name__ == '__main__':
    unittest.main()
