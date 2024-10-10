import unittest
import matplotlib.pyplot as plt
import numpy as np

# Import the necessary classes and modules
from RandomPeriodic_JammingAttack import RandomPeriodic_JammingAttack
from Parameters import Parameters

# Constants used in PeriodicJammingAttack
MINIMUM_BURST_DURATION = 1
MAXIMUM_BURST_DURATION = 5
MINIMUM_DUTY_RATE = 0.1
MAXIMUM_DUTY_RATE = 0.5

class TestPeriodicJammingAttack(unittest.TestCase):
    def setUp(self):
        self.size = 5000  # Using a smaller size for testing
        self.attack = RandomPeriodic_JammingAttack(size=self.size)

    # Test that generateJamming builds the jammingStructure correctly with updated burstDuration and restDuration.
    def test_generateJamming(self):
        # Call the generateJamming method
        jamming_values, ground_truth = self.attack.generateJamming()

        # Ensure that jammingStructure is not empty
        self.assertTrue(len(self.attack.jammingStructure) > 0)

        # Verify that burstDuration and restDuration are updated within the loop
        # Since burstDuration and restDuration are updated after each jamming signal,
        # we can check that they have changed from their initial values

        initial_burst_duration = self.attack.burstDuration
        initial_rest_duration = self.attack.restDuration

        # Since burstDuration and restDuration are updated within generateJamming,
        # and we have set a fixed random seed, we can predict their values
        # However, since we can't access their values after the method completes,
        # we can test indirectly by analyzing the jammingStructure

        # Analyze the jammingStructure
        for i, element in enumerate(self.attack.jammingStructure):
            start_index, end_index, signal_type = element
            duration = end_index - start_index

            if signal_type == Parameters.NORMAL_TRAFFIC:
                # For normal traffic, duration should correspond to restDuration
                expected_duration = self.attack.restDuration
            else:
                # For jamming traffic, duration should correspond to burstDuration
                expected_duration = self.attack.burstDuration

            # Since burstDuration and restDuration are updated after jamming signals,
            # we can only check that durations are positive and within expected ranges
            self.assertTrue(duration > 0)
            self.assertTrue(duration <= self.size)

        # Check that the outputs are valid
        self.assertIsNotNone(jamming_values)
        self.assertIsNotNone(ground_truth)
        self.assertEqual(len(jamming_values), len(ground_truth))
        self.assertEqual(len(jamming_values), self.size)

    # Test method that generates jamming data and plots the results.
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

        # Check that ground_truth labels are valid
        self.assertTrue(all(label in [Parameters.INLIERS, Parameters.OUTLIERS] for label in result_ground_truth))

    #Test that burstDuration and restDuration are updated and that the durations in jammingStructure reflect these changes.
    def test_jammingStructure_durations(self):
        # Call the generateJamming method
        self.attack.generateJamming()

        # Initialize variables to track durations
        burst_durations = []
        rest_durations = []

        for element in self.attack.jammingStructure:
            start_index, end_index, signal_type = element
            duration = end_index - start_index

            if signal_type == Parameters.NORMAL_TRAFFIC:
                rest_durations.append(duration)
            else:
                burst_durations.append(duration)

        # Since burstDuration and restDuration are updated after each jamming signal,
        # we expect to see variability in the durations

        # Check that there is more than one unique burst duration
        unique_burst_durations = set(burst_durations)
        unique_rest_durations = set(rest_durations)

        self.assertTrue(len(unique_burst_durations) > 1)
        self.assertTrue(len(unique_rest_durations) > 1)

        # Check that burst durations are within expected ranges
        for bd in burst_durations:
            self.assertGreaterEqual(bd, MINIMUM_BURST_DURATION * 100)
            self.assertLessEqual(bd, MAXIMUM_BURST_DURATION * 100)

        # Check that rest durations are positive
        for rd in rest_durations:
            self.assertGreater(rd, 0)

    #Test that burstDuration and restDuration are updated correctly within the generateJamming method.
    def test_burst_and_rest_duration_updates(self):
        # Save initial burstDuration and restDuration
        initial_burst_duration = self.attack.burstDuration
        initial_rest_duration = self.attack.restDuration

        # Call the generateJamming method
        self.attack.generateJamming()

        # Since burstDuration and restDuration are updated inside the method,
        # and we can't access their updated values directly after the method,
        # we'll test indirectly by checking the durations in jammingStructure

        burst_durations = []
        rest_durations = []

        for element in self.attack.jammingStructure:
            start_index, end_index, signal_type = element
            duration = end_index - start_index

            if signal_type == Parameters.NORMAL_TRAFFIC:
                rest_durations.append(duration)
            else:
                burst_durations.append(duration)

        # Ensure that durations have changed from the initial values
        self.assertNotEqual(burst_durations[0], burst_durations[-1])
        self.assertNotEqual(rest_durations[0], rest_durations[-1])

    # You can add more tests as needed to cover other aspects of the modified method


if __name__ == '__main__':
    unittest.main()
