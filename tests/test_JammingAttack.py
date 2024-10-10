import unittest
from unittest.mock import patch
import numpy as np
import matplotlib.pyplot as plt

# Import the necessary classes and modules
from JammingAttack import JammingAttack
from Parameters import Parameters
from Constructor import Constructor

class TestJammingAttack(unittest.TestCase):

    def setUp(self):
        self.size = 2000
        self.jamming_attack = JammingAttack(self.size)

    # Test that the JammingAttack object initializes correctly.
    def test_initialization(self):
        self.assertEqual(self.jamming_attack.size, self.size)
        self.assertEqual(self.jamming_attack.jammingStructure, [])

    def test_selectStart_jammingTypes_invalid_low(self):
        with self.assertRaises(Exception) as context:
            self.jamming_attack.selectStart(0)  # Invalid jammingTypes
        self.assertIn("The jamming type is not valid", str(context.exception))

    def test_selectStart_jammingTypes_invalid_high(self):
        with self.assertRaises(Exception) as context:
            self.jamming_attack.selectStart(4)  # Invalid jammingTypes
        self.assertIn("The jamming type is not valid", str(context.exception))

    # Test that selectStart returns Parameters.NORMAL_TRAFFIC when NormalorJamming == 0.
    @patch('random.randint')
    def test_selectStart_returns_NORMAL_TRAFFIC(self, mock_randint):
        # Mock random.randint to return 0 for NormalorJamming
        mock_randint.side_effect = [0]  # First call returns 0
        result = self.jamming_attack.selectStart(2)  # jammingTypes can be any valid value
        self.assertEqual(result, Parameters.NORMAL_TRAFFIC)
        # Verify that random.randint was called with (0, 1)
        mock_randint.assert_called_with(0, 1)

    # Test that selectStart returns a jamming type when NormalorJamming == 1.
    @patch('random.randint')
    def test_selectStart_returns_jammingType(self, mock_randint):
        # Mock random.randint to return 1 for NormalorJamming, then 2 for jamming type
        mock_randint.side_effect = [1, 2]  # First call: NormalorJamming, Second call: jamming type
        result = self.jamming_attack.selectStart(3)
        self.assertEqual(result, 2)
        # Verify the sequence of calls
        expected_calls = [((0, 1),), ((1, 3),)]
        actual_calls = mock_randint.call_args_list
        self.assertEqual(actual_calls, [unittest.mock.call(*args) for args in expected_calls])

    # Test that selectStart returns the correct jamming type for each jammingTypes value.
    @patch('random.randint')
    def test_selectStart_jammingType_range(self, mock_randint):
        # Test for jammingTypes = 1
        mock_randint.side_effect = [1, 1]
        result = self.jamming_attack.selectStart(1)
        self.assertEqual(result, 1)
        mock_randint.reset_mock()

        # Test for jammingTypes = 2
        mock_randint.side_effect = [1, 2]
        result = self.jamming_attack.selectStart(2)
        self.assertEqual(result, 2)
        mock_randint.reset_mock()

        # Test for jammingTypes = 3
        mock_randint.side_effect = [1, 3]
        result = self.jamming_attack.selectStart(3)
        self.assertEqual(result, 3)

    # Test the buildElement method to ensure it appends elements correctly.
    def test_buildElement(self):
        start_index = 0
        end_index = 100
        traffic_type = Parameters.NORMAL_TRAFFIC

        self.jamming_attack.buildElement(start_index, end_index, traffic_type)
        expected_structure = [[start_index, end_index, traffic_type]]

        self.assertEqual(self.jamming_attack.jammingStructure, expected_structure)

    # Test the generateJamming method to ensure it builds the jammingStructure correctly.
    def test_generateJamming(self):
        # Ensure the jammingStructure is empty before calling generateJamming
        self.jamming_attack.jammingStructure = []

        # Call the method
        result_jamming_values, result_ground_truth = self.jamming_attack.generateJamming()

        # Verify that jammingStructure was built correctly
        expected_structure = [[0, self.size, Parameters.JAMMING_10DBM]]
        self.assertEqual(self.jamming_attack.jammingStructure, expected_structure)

        # Verify the results
        self.assertEqual(len(result_jamming_values), len(result_ground_truth))
        self.assertEqual(len(result_jamming_values), self.size)

        # Check that ground_truth labels are all OUTLIERS
        self.assertTrue(all(label == Parameters.OUTLIERS for label in result_ground_truth))

    # Test generateJamming when jammingStructure is empty.
    def test_generateJamming_with_empty_structure(self):
        # Ensure jammingStructure is empty
        self.jamming_attack.jammingStructure = []

        # Since generateJamming sets jammingStructure internally, we can test that the method doesn't raise exceptions when starting with an empty structure.
        with patch.object(Constructor, 'assemble', return_value=('jamming_data', 'ground_truth')) as mock_assemble:
            result = self.jamming_attack.generateJamming()
            mock_assemble.assert_called_once_with(self.jamming_attack.jammingStructure)
            self.assertEqual(result, ('jamming_data', 'ground_truth'))

    # Test method that generates jamming data and plots the results.
    def test_plot_generateJamming(self):
        # Ensure the jammingStructure is empty
        self.jamming_attack.jammingStructure = []

        # Call the generateJamming method
        result_jamming_values, result_ground_truth = self.jamming_attack.generateJamming()

        # Convert result_jamming_values to a NumPy array if not already
        if not isinstance(result_jamming_values, np.ndarray):
            result_jamming_values = np.array(result_jamming_values)

        # Flatten the arrays for plotting if necessary
        result_jamming_values = result_jamming_values.flatten()
        result_ground_truth = np.array(result_ground_truth)

        # Plotting the results
        fig, ax1 = plt.subplots(figsize=(12, 6))

        # Plot jamming_values
        color = 'tab:blue'
        ax1.set_xlabel('Sample Index')
        ax1.set_ylabel('Jamming Values (RSSI)', color=color)
        ax1.plot(result_jamming_values, color=color, label='Jamming Values')
        ax1.tick_params(axis='y', labelcolor=color)

        # Create a second y-axis for ground_truth
        ax2 = ax1.twinx()
        color = 'tab:red'
        ax2.set_ylabel('Ground Truth', color=color)
        ax2.plot(result_ground_truth, color=color, linestyle='--', label='Ground Truth')
        ax2.tick_params(axis='y', labelcolor=color)
        ax2.set_yticks([Parameters.INLIERS, Parameters.OUTLIERS])
        ax2.set_yticklabels(['Inliers', 'Outliers'])

        # Add legends
        lines_1, labels_1 = ax1.get_legend_handles_labels()
        lines_2, labels_2 = ax2.get_legend_handles_labels()
        ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right')

        # Add a title
        plt.title('Generated Jamming Data and Ground Truth')

        # Show the plot
        plt.show()

        # Assertions to ensure the method works as expected
        self.assertEqual(len(result_jamming_values), self.size)
        self.assertEqual(len(result_ground_truth), self.size)

        # Check that ground_truth labels are all OUTLIERS
        self.assertTrue(all(label == Parameters.OUTLIERS for label in result_ground_truth))

if __name__ == '__main__':
    unittest.main()
