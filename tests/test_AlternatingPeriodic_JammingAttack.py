import random
import unittest
import matplotlib.pyplot as plt
import numpy as np

from AlternatingPeriodic_JammingAttack import AlternatingPeriodic_JammingAttack
from Constructor import Constructor
from Parameters import Parameters

# Constants used in PeriodicJammingAttack
MINIMUM_BURST_DURATION = 1
MAXIMUM_BURST_DURATION = 5
MINIMUM_DUTY_RATE = 0.1
MAXIMUM_DUTY_RATE = 0.5

class Test_AlternatingPeriodic_JammingAttack(unittest.TestCase):
    def setUp(self):
        self.size = 5000  # Using a smaller size for testing
        self.attack = AlternatingPeriodic_JammingAttack(size=self.size)



    #Test that generateJamming builds the jammingStructure correctly.
    def test_generateJamming_structure(self):
        self.attack.generateJamming()
        jamming_structure = self.attack.jammingStructure

        # Ensure that jammingStructure is not empty
        self.assertTrue(len(jamming_structure) > 0)

        # Check that the first element is normal traffic
        first_element = jamming_structure[0]
        self.assertEqual(first_element[0], 0)
        self.assertEqual(first_element[2], Parameters.NORMAL_TRAFFIC)

        # Check that signals alternate between jamming types
        for i in range(1, len(jamming_structure)):
            current_element = jamming_structure[i]
            prev_element = jamming_structure[i - 1]
            self.assertEqual(current_element[0], prev_element[1])  # Continuity
            if current_element[2] == Parameters.JAMMING_10DBM:
                self.assertEqual(prev_element[2], Parameters.JAMMING_NEG10DBM)
            elif current_element[2] == Parameters.JAMMING_NEG10DBM:
                self.assertIn(prev_element[2], [Parameters.NORMAL_TRAFFIC, Parameters.JAMMING_10DBM])
            else:
                self.fail(f"Unexpected signal type: {current_element[2]}")

    # Test that the outputs have the correct lengths.
    def test_generateJamming_output_lengths(self):

        jamming_values, ground_truth = self.attack.generateJamming()

        # Check that the outputs are not None
        self.assertIsNotNone(jamming_values)
        self.assertIsNotNone(ground_truth)

        # Check that the outputs have the expected length
        self.assertEqual(len(jamming_values), self.size)
        self.assertEqual(len(ground_truth), self.size)
        
    #Test method that generates jamming data and plots the results.
    def test_generateJamming_plot(self):
        jamming_values, ground_truth = self.attack.generateJamming()

        # Convert to NumPy arrays if not already
        jamming_values = np.array(jamming_values)
        ground_truth = np.array(ground_truth)

        # Plotting the results
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
        plt.title('Generated Jamming Data and Ground Truth')

        # Show the plot
        plt.show()

        # Assertions to ensure the method works as expected
        self.assertEqual(len(jamming_values), self.size)
        self.assertEqual(len(ground_truth), self.size)
        self.assertTrue(all(label in [Parameters.INLIERS, Parameters.OUTLIERS] for label in ground_truth))


if __name__ == '__main__':
    unittest.main()
