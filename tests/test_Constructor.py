import os
import unittest
import numpy as np
import matplotlib.pyplot as plt

# Importing the necessary classes
from FileHandler import FileHandler
from Parameters import Parameters
from Constructor import Constructor


class TestConstructor(unittest.TestCase):

    #setUp method is called before each test in this class that creates a new Constructor
    def setUp(self):
        self.constructor = Constructor()

    #tearDown method is called after each test
    def tearDown(self):
        self.constructor = None

    # Test that the Constructor class initializes correctly by loading data from files.
    def test_constructor_initialization(self):
        # Check that the loaded data is not None
        self.assertIsNotNone(self.constructor.get_NormalValues())
        self.assertIsNotNone(self.constructor.get_JammingValues_10dBm())
        self.assertIsNotNone(self.constructor.get_JammingValues_neg10dBm())
        self.assertIsNotNone(self.constructor.get_JammingValues_neg40dBm())

        # Optionally check the sizes match the expected sizes from Parameters
        self.assertEqual(len(self.constructor.get_NormalValues()), Parameters.NORMAL_TRAFFIC_SIZE)
        self.assertEqual(len(self.constructor.get_JammingValues_10dBm()), Parameters.CONSTANT_JAMMING_SIZE)
        self.assertEqual(len(self.constructor.get_JammingValues_neg10dBm()), Parameters.CONSTANT_JAMMING_SIZE)
        self.assertEqual(len(self.constructor.get_JammingValues_neg40dBm()), Parameters.CONSTANT_JAMMING_SIZE)

    # Test that the getJammingValues method returns the correct amount of data
    def test_getJammingValues(self):
        size = 5

        # Test for JAMMING_10DBM
        values = self.constructor.getJammingValues(Parameters.JAMMING_10DBM, size)
        self.assertEqual(len(values), size)
        self.assertEqual(self.constructor.get_LastJamming10dBmIndex(), size)

        # Test for JAMMING_NEG10DBM
        values = self.constructor.getJammingValues(Parameters.JAMMING_NEG10DBM, size)
        self.assertEqual(len(values), size)
        self.assertEqual(self.constructor.get_LastJammingNeg10dBmIndex(), size)

        # Test for JAMMING_NEG40DBM
        values = self.constructor.getJammingValues(Parameters.JAMMING_NEG40DBM, size)
        self.assertEqual(len(values), size)
        self.assertEqual(self.constructor.get_LastJammingNeg40dBmIndex(), size)

        # Test for invalid jamming type
        with self.assertRaises(Exception) as context:
            self.constructor.getJammingValues('INVALID_TYPE', size)
        self.assertIn("The jamming type is not valid", str(context.exception))

    #Test the getNormalValues method to ensure it returns the correct amount of data
    def test_getNormalValues(self):
        constructor = Constructor()
        size = 5
        values = constructor.getNormalValues(size)
        self.assertEqual(len(values), size)

    # Test the assemble method to ensure it generates the correct jamming values and ground truth labels
    def test_assemble(self):
        # Define a jamming structure
        # Each tuple is (start_index, end_index, traffic_type)
        jamming_structure = [
            (0, 5, Parameters.NORMAL_TRAFFIC),
            (5, 10, Parameters.JAMMING_10DBM),
            (10, 15, Parameters.NORMAL_TRAFFIC),
            (15, 20, Parameters.JAMMING_NEG10DBM),
        ]

        # Call the assemble method
        jamming_values, ground_truth = self.constructor.assemble(jamming_structure)

        # Verify the lengths of the outputs
        expected_length = 20  # Total length from jamming_structure
        self.assertEqual(len(jamming_values), expected_length)
        self.assertEqual(len(ground_truth), expected_length)
        self.assertEqual(len(jamming_values), len(ground_truth))

        # Verify ground truth labels
        expected_ground_truth = (
                [Parameters.INLIERS] * 5 +
                [Parameters.OUTLIERS] * 5 +
                [Parameters.INLIERS] * 5 +
                [Parameters.OUTLIERS] * 5
        )
        self.assertEqual(ground_truth, expected_ground_truth)

    #Test that the assemble method raises an exception when given an empty list.
    def test_assemble_empty_structure(self):
        with self.assertRaises(Exception) as context:
            self.constructor.assemble([])
        self.assertIn("The jamming structure is empty", str(context.exception))

    #Test that the assemble method raises an exception when given None as input.
    def test_assemble_none_structure(self):
        with self.assertRaises(Exception) as context:
            self.constructor.assemble(None)
        self.assertIn("The jamming structure is empty", str(context.exception))

    # Test method that assembles data and plots jammingValues and groundTruth in a single graph.
    def test_plot_jamming_values_and_ground_truth(self):
        # Define a jamming structure
        jamming_structure = [
            (0, 50, Parameters.NORMAL_TRAFFIC),
            (50, 100, Parameters.JAMMING_10DBM),
            (100, 150, Parameters.NORMAL_TRAFFIC),
            (150, 200, Parameters.JAMMING_NEG10DBM),
            (200, 250, Parameters.NORMAL_TRAFFIC),
        ]

        # Assemble the data
        jamming_values, ground_truth = self.constructor.assemble(jamming_structure)

        # Convert jamming_values to a NumPy array if not already
        if not isinstance(jamming_values, np.ndarray):
            jamming_values = np.array(jamming_values)

        # Flatten the arrays for plotting
        jamming_values = jamming_values.flatten()
        ground_truth = np.array(ground_truth)

        # Create a figure and axis
        fig, ax1 = plt.subplots(figsize=(12, 6))

        # Plot jamming_values
        color = 'tab:blue'
        ax1.set_xlabel('Sample Index')
        ax1.set_ylabel('Jamming Values (RSSI)', color=color)
        ax1.plot(jamming_values, color=color, label='Jamming Values')
        ax1.tick_params(axis='y', labelcolor=color)

        # Create a second y-axis for ground_truth
        ax2 = ax1.twinx()
        color = 'tab:red'
        ax2.set_ylabel('Ground Truth', color=color)
        ax2.plot(ground_truth, color=color, linestyle='--', label='Ground Truth')
        ax2.tick_params(axis='y', labelcolor=color)
        ax2.set_yticks([Parameters.INLIERS, Parameters.OUTLIERS])
        ax2.set_yticklabels(['Inliers', 'Outliers'])

        # Add legends
        lines_1, labels_1 = ax1.get_legend_handles_labels()
        lines_2, labels_2 = ax2.get_legend_handles_labels()
        ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right')

        # Add a title
        plt.title('Jamming Values and Ground Truth')

        # Show the plot
        plt.show()

if __name__ == '__main__':
    unittest.main()
