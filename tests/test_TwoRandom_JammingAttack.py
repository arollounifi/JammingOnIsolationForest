import unittest
import random
import numpy as np
import matplotlib.pyplot as plt

# Import the necessary classes and modules
from TwoRandom_JammingAttack import TwoRandom_JammingAttack
from Parameters import Parameters
from Constructor import Constructor

# Constants used in TwoRandom_JammingAttack
MAXIMUM_BURST_DURATION = 5
MINIMUM_BURST_DURATION = 1
MAXIMUM_DUTY_RATE_1 = 0.5
MINIMUM_DUTY_RATE_1 = 0.1
MAXIMUM_DUTY_RATE_2 = 0.8
MINIMUM_DUTY_RATE_2 = 0.3

class TestTwoRandomJammingAttack(unittest.TestCase):

    # Set a fixed random seed for reproducibility
    def setUp(self):
        self.size = 5000  # Using a smaller size for testing
        self.jammingTypes = [Parameters.JAMMING_10DBM, Parameters.JAMMING_NEG10DBM]
        self.attack = TwoRandom_JammingAttack(size=self.size, jammingTypes=self.jammingTypes)
        # Ensure JammingAttacks is set if used in the class
        self.attack.JammingAttacks = self.attack.jammingTypes

    # Test that decideDutyRate returns values within the expected ranges for each attacker.
    def test_decideDutyRate(self):
        # Test for jammingTypes[0]
        duty_rate1 = self.attack.decideDutyRate(self.jammingTypes[0])
        self.assertGreaterEqual(duty_rate1, MINIMUM_DUTY_RATE_1)
        self.assertLessEqual(duty_rate1, MAXIMUM_DUTY_RATE_1)

        # Test for jammingTypes[1]
        duty_rate2 = self.attack.decideDutyRate(self.jammingTypes[1])
        self.assertGreaterEqual(duty_rate2, MINIMUM_DUTY_RATE_2)
        self.assertLessEqual(duty_rate2, MAXIMUM_DUTY_RATE_2)

    # Test that can_insert_attack correctly determines if an attack can be inserted.
    def test_can_insert_attack(self):
        attack_type = self.jammingTypes[0]
        index = 100
        self.attack.last_attack_indices[attack_type] = 50
        self.attack.restDurations[attack_type] = 40

        # Expected to return True since index >= last_attack_index + rest_duration
        result = self.attack.can_insert_attack(attack_type, index)
        self.assertTrue(result)

        # Now test with index = 80, expected to return False
        index = 80
        result = self.attack.can_insert_attack(attack_type, index)
        self.assertFalse(result)

    # Test that insert_attack updates jammingStructure and last_attack_indices correctly.
    def test_insert_attack(self):
        self.attack.jammingStructure = []
        index = 0
        attack_type = self.jammingTypes[0]
        expected_end_index = min(index + self.attack.burstDurations[attack_type], self.size)
        attack_end_index = self.attack.insert_attack(attack_type, index)

        # Verify that jammingStructure has one new element
        self.assertEqual(len(self.attack.jammingStructure), 1)
        element = self.attack.jammingStructure[0]
        self.assertEqual(element[0], index)
        self.assertEqual(element[2], attack_type)

        self.assertEqual(element[1], expected_end_index)
        self.assertEqual(attack_end_index, expected_end_index)
        self.assertEqual(self.attack.last_attack_indices[attack_type], attack_end_index)

    # Test that insert_normal_traffic updates jammingStructure correctly.
    def test_insert_normal_traffic(self):

        self.attack.jammingStructure = []
        index = 0
        end_index = 100
        new_index = self.attack.insert_normal_traffic(index, end_index)

        self.assertEqual(len(self.attack.jammingStructure), 1)
        element = self.attack.jammingStructure[0]
        self.assertEqual(element[0], index)
        self.assertEqual(element[1], end_index)
        self.assertEqual(element[2], Parameters.NORMAL_TRAFFIC)
        self.assertEqual(new_index, end_index)

    # Test that get_next_available_attacks returns the correct list of available attacks.
    def test_get_next_available_attacks(self):
        index = 100
        self.attack.last_attack_indices[self.jammingTypes[0]] = 50
        self.attack.restDurations[self.jammingTypes[0]] = 40
        self.attack.last_attack_indices[self.jammingTypes[1]] = 90
        self.attack.restDurations[self.jammingTypes[1]] = 30

        available_attacks = self.attack.get_next_available_attacks(index)
        self.assertIn(self.jammingTypes[0], available_attacks)
        self.assertNotIn(self.jammingTypes[1], available_attacks)

    # Test that get_next_available_time returns the correct next available time.
    def test_get_next_available_time(self):
        self.attack.last_attack_indices[self.jammingTypes[0]] = 50
        self.attack.restDurations[self.jammingTypes[0]] = 40
        self.attack.last_attack_indices[self.jammingTypes[1]] = 90
        self.attack.restDurations[self.jammingTypes[1]] = 30

        next_time = self.attack.get_next_available_time()
        self.assertEqual(next_time, 90)  # 50 + 40 = 90, 90 + 30 = 120, min(90, 120) = 80

    #Test that decide_next_attack selects the attack with the highest priority.
    def test_decide_next_attack(self):
        self.attack.JammingAttacks = self.attack.jammingTypes  # Ensure JammingAttacks is set
        available_attacks = [self.jammingTypes[1], self.jammingTypes[0]]
        selected_attack = self.attack.decide_next_attack(available_attacks)
        self.assertEqual(selected_attack, self.jammingTypes[0])

    # Test that generateJamming builds the jammingStructure and outputs correctly.
    def test_generateJamming(self):
        jamming_values, ground_truth = self.attack.generateJamming()

        # Check that jammingStructure is not empty
        self.assertTrue(len(self.attack.jammingStructure) > 0)
        # Verify outputs
        self.assertIsNotNone(jamming_values)
        self.assertIsNotNone(ground_truth)
        self.assertEqual(len(jamming_values), len(ground_truth))
        self.assertEqual(len(jamming_values), self.size)

        # Optionally, check the contents of jammingStructure
        for element in self.attack.jammingStructure:
            start_index, end_index, signal_type = element
            self.assertGreaterEqual(start_index, 0)
            self.assertLessEqual(end_index, self.size)
            self.assertGreater(end_index, start_index)
            self.assertIn(signal_type, self.jammingTypes + [Parameters.NORMAL_TRAFFIC])

    #Test method that generates jamming data and plots the results.
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