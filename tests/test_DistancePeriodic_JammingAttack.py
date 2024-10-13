import unittest
import random
import numpy as np
import matplotlib.pyplot as plt

# Import the necessary classes and modules
from DistancePeriodic_JammingAttack import DistancePeriodic_JammingAttack
from Parameters import Parameters
from Constructor import Constructor

# Constants used in DistancePeriodic_JammingAttack
MAXIMUM_BURST_DURATION = 5
MINIMUM_BURST_DURATION = 1
MAXIMUM_DUTY_RATE = 0.8
MINIMUM_DUTY_RATE = 0.3

class TestDistancePeriodicJammingAttack(unittest.TestCase):
    def setUp(self):
        self.size = 5000  # Use a smaller size for testing
        self.attack = DistancePeriodic_JammingAttack(size=self.size)

    #Test that apply_fspl_to_jamming attenuates jamming signals correctly.
    def test_apply_fspl_to_jamming(self):
        # Create a test signal list and jamming flags
        signal_list = np.ones(self.size) * -50  # Example RSSI values
        # Create jamming flags: True for jamming, False for normal traffic
        ground_truth = [Parameters.OUTLIERS if i % 2 == 0 else Parameters.INLIERS for i in range(self.size)]
        jamming_flags = [gt == Parameters.OUTLIERS for gt in ground_truth]

        modified_signal_list = self.attack.apply_fspl_to_jamming(signal_list, jamming_flags)

        # Check that jamming signals are attenuated
        for i in range(self.size):
            if jamming_flags[i]:
                self.assertLess(modified_signal_list[i], signal_list[i])  # Signal should be decreased
            else:
                self.assertEqual(modified_signal_list[i], signal_list[i])  # Signal should remain the same

    #Test that generateJamming produces outputs of the correct length and applies FSPL correctly.
    def test_generateJamming(self):
        jamming_values, ground_truth = self.attack.generateJamming()

        # Check that outputs are not None
        self.assertIsNotNone(jamming_values)
        self.assertIsNotNone(ground_truth)

        # Check that outputs have the expected length
        self.assertEqual(len(jamming_values), self.size)
        self.assertEqual(len(ground_truth), self.size)

        # Convert ground_truth to jamming flags
        jamming_flags = [gt == Parameters.OUTLIERS for gt in ground_truth]

        # Check that FSPL is applied to jamming signals
        original_jamming_values, _ = self.attack.constructor.assemble(self.attack.jammingStructure)
        modified_signal_list = self.attack.apply_fspl_to_jamming(original_jamming_values, jamming_flags)

        # The jamming_values from generateJamming should match the modified_signal_list
        np.testing.assert_array_almost_equal(jamming_values, modified_signal_list)

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
        plt.title('Generated Jamming Data with FSPL Applied and Ground Truth')

        # Show the plot
        plt.show()

        # Assertions to ensure the method works as expected
        self.assertEqual(len(jamming_values), self.size)
        self.assertEqual(len(ground_truth), self.size)
        self.assertTrue(all(label in [Parameters.INLIERS, Parameters.OUTLIERS] for label in ground_truth))

if __name__ == '__main__':
    unittest.main()
