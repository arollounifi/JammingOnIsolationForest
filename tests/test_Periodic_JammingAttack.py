import unittest
import matplotlib.pyplot as plt
import numpy as np

# Import the necessary classes and modules
from Periodic_JammingAttack import Periodic_JammingAttack
from Parameters import Parameters

# Constants used in PeriodicJammingAttack
MINIMUM_BURST_DURATION = 1
MAXIMUM_BURST_DURATION = 5
MINIMUM_DUTY_RATE = 0.1
MAXIMUM_DUTY_RATE = 0.5

class TestPeriodicJammingAttack(unittest.TestCase):
    def setUp(self):
        self.size = 5000  # Using a smaller size for testing
        self.attack = Periodic_JammingAttack(size=self.size)

    # Test that decideBurstDuration returns a value within the expected range.
    def test_decideBurstDuration(self):
        burst_duration = self.attack.decideBurstDuration()
        self.assertGreaterEqual(burst_duration, MINIMUM_BURST_DURATION)
        self.assertLessEqual(burst_duration, MAXIMUM_BURST_DURATION)

    # Test that decideDutyRate returns a value within the expected range.
    def test_decideDutyRate(self):
        duty_rate = self.attack.decideDutyRate()
        self.assertGreaterEqual(duty_rate, MINIMUM_DUTY_RATE)
        self.assertLessEqual(duty_rate, MAXIMUM_DUTY_RATE)

    #Test that generateJammingStructure correctly builds the jammingStructure.
    def test_generateJammingStructure(self):
        self.attack.generateJammingStructure()
        # Ensure that jammingStructure is not empty
        self.assertTrue(len(self.attack.jammingStructure) > 0)

        # Check that the elements in jammingStructure have the correct format
        previousType = None
        for element in self.attack.jammingStructure:
            # Each element should be a list of [start_index, end_index, traffic_type]
            self.assertEqual(len(element), 3)
            start_index, end_index, traffic_type = element
            self.assertIsInstance(start_index, (int, float))
            self.assertIsInstance(end_index, (int, float))
            # traffic_type should be Parameters.NORMAL_TRAFFIC or a jamming type (e.g., 1)
            self.assertIn(traffic_type, [Parameters.NORMAL_TRAFFIC, Parameters.JAMMING_10DBM])
            self.assertFalse(traffic_type == previousType)
            self.assertGreaterEqual(start_index, 0)
            self.assertLessEqual(end_index, self.size)
            self.assertGreater(end_index, start_index)
            previousType = traffic_type

    #Test that generateJamming returns valid data and ground truth.
    def test_generateJamming(self):
        jamming_values, ground_truth = self.attack.generateJamming()

        # Check that the outputs are not None
        self.assertIsNotNone(jamming_values)
        self.assertIsNotNone(ground_truth)

        # Check that they are of the same length
        self.assertEqual(len(jamming_values), len(ground_truth))

        # Check that the length matches the attack size
        self.assertEqual(len(jamming_values), self.size)

    #Test method that generates the jamming structure and plots the results.
    def test_plot_generateJamming(self):
        # Ensure the jammingStructure is empty
        self.attack.jammingStructure = []

        # Call the generateJamming method
        result_jamming_values, result_ground_truth = self.attack.generateJamming()

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


if __name__ == '__main__':
    unittest.main()
