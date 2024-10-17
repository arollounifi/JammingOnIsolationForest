import os
import unittest
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

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
        self.assertEqual(len(self.constructor.get_JammingValues_10dBm()), Parameters.JAMMING_TRAFFIC_SIZE)
        self.assertEqual(len(self.constructor.get_JammingValues_neg10dBm()), Parameters.JAMMING_TRAFFIC_SIZE)
        self.assertEqual(len(self.constructor.get_JammingValues_neg40dBm()), Parameters.JAMMING_TRAFFIC_SIZE)

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

    def test_introduce_anomalies(self):
        # Dataset di esempio
        dataset = np.array([-80, -82, -79, -83, -81, -84, -85, -77, -80, -81])

        # Test 1: Verifica che il risultato sia un array NumPy
        dati_sporcati = self.constructor.dirtyNormalValues(dataset, 0.071429, 2.345)
        assert isinstance(dati_sporcati, np.ndarray), "Il risultato non è un array NumPy!"

        # Test 2: Verifica che il numero di anomalie sia corretto
        anomaly_ratio = 0.2  # Impostiamo il rapporto di anomalie al 20%
        dati_sporcati = self.constructor.dirtyNormalValues(dataset, anomaly_ratio, 2.345)
        num_anomalies = int(len(dataset) * anomaly_ratio)
        num_changes = np.sum(dataset != dati_sporcati)  # Conta quanti valori sono cambiati
        assert num_changes == num_anomalies, f"Il numero di anomalie introdotte è sbagliato! (Aspettato: {num_anomalies}, Trovato: {num_changes})"

        # Test 3: Verifica che la lunghezza del risultato sia la stessa dell'input
        dati_sporcati = self.constructor.dirtyNormalValues(dataset, anomaly_ratio, 2.345)
        assert len(dati_sporcati) == len(dataset), "La lunghezza dell'array è cambiata!"

        # Test 4: Stampa i valori originali e quelli "sporcati"
        print("Dati originali:")
        print(dataset)
        print("\nDati sporcati:")
        print(dati_sporcati)

    def test_type_checking_simulation(self):
        # Create sample data arrays
        self.normalValues = np.linspace(-80, -60, 1000)  # Example RSSI values for normal traffic
        self.jammingValues_10dBm = np.linspace(-50, -30, 1000)
        self.jammingValues_neg10dBm = np.linspace(-70, -50, 1000)
        self.jammingValues_neg40dBm = np.linspace(-90, -70, 1000)

        # Initialize Constructor instance
        self.constructor = Constructor()

        # Inject sample data into the Constructor instance
        self.constructor._Constructor__normalValues = self.normalValues
        self.constructor._Constructor__jammingValues_10dBm = self.jammingValues_10dBm
        self.constructor._Constructor__jammingValues_neg10dBm = self.jammingValues_neg10dBm
        self.constructor._Constructor__jammingValues_neg40dBm = self.jammingValues_neg40dBm

        jammingStructure = [
            (0, 100, Parameters.NORMAL_TRAFFIC),
            (100, 200, Parameters.JAMMING_10DBM),
            (200, 300, Parameters.NORMAL_TRAFFIC),
            (300, 400, Parameters.JAMMING_NEG10DBM),
            (400, 500, Parameters.NORMAL_TRAFFIC),
            (500, 600, Parameters.JAMMING_NEG40DBM),
            (600, 700, Parameters.NORMAL_TRAFFIC)
        ]

        # Call the assemble method
        jammingValues, groundTruth = self.constructor.assemble(jammingStructure)

        # Verify the types of the outputs
        self.assertIsInstance(jammingValues, list)
        self.assertIsInstance(groundTruth, list)

        # Verify the lengths of the outputs
        expected_length = jammingStructure[-1][1]  # Should be 700
        self.assertEqual(len(jammingValues), expected_length)
        self.assertEqual(len(groundTruth), expected_length)

        # Convert jammingValues to a NumPy array for further checks
        jammingValues_array = np.array(jammingValues)

        # Ensure all elements are numeric
        self.assertTrue(np.issubdtype(jammingValues_array.dtype, np.number))

        # Reshape the data for IsolationForest (expects 2D array)
        X = jammingValues_array.reshape(-1, 1)

        # Verify the shape is appropriate
        self.assertEqual(X.shape, (expected_length, 1))

        # Attempt to fit IsolationForest
        try:
            clf = IsolationForest(random_state=42)
            clf.fit(X)
        except Exception as e:
            self.fail(f"IsolationForest failed to fit the data: {e}")

        # If no exception, the data is acceptable
        print("Data is acceptable for IsolationForest.")

    def test_assemble_with_actual_data(self):
        # Create a sample jammingStructure
        # For the purpose of the test, we'll create a simple structure
        jammingStructure = [
            (0, 500, Parameters.NORMAL_TRAFFIC),
            (500, 1000, Parameters.JAMMING_10DBM),
            (1000, 1500, Parameters.NORMAL_TRAFFIC),
            (1500, 2000, Parameters.JAMMING_NEG10DBM),
            (2000, 2500, Parameters.NORMAL_TRAFFIC),
            (2500, 3000, Parameters.JAMMING_NEG40DBM),
            (3000, 3500, Parameters.NORMAL_TRAFFIC)
        ]

        # Call the assemble method
        try:
            jammingValues, groundTruth = self.constructor.assemble(jammingStructure)
        except Exception as e:
            self.fail(f"assemble method raised an exception: {e}")

        # Verify the types of the outputs
        self.assertIsInstance(jammingValues, list)
        self.assertIsInstance(groundTruth, list)

        # Verify the lengths of the outputs
        expected_length = jammingStructure[-1][1]  # Should be 35000
        self.assertEqual(len(jammingValues), expected_length)
        self.assertEqual(len(groundTruth), expected_length)

        # Convert jammingValues to a NumPy array for further checks
        jammingValues_array = np.array(jammingValues)

        # Ensure all elements are numeric
        self.assertTrue(np.issubdtype(jammingValues_array.dtype, np.number))

        # Reshape the data for IsolationForest (expects 2D array)
        X = jammingValues_array.reshape(-1, 1)

        # Verify the shape is appropriate
        self.assertEqual(X.shape, (expected_length, 1))

        # Attempt to fit IsolationForest
        try:
            clf = IsolationForest(random_state=42)
            clf.fit(X)
        except Exception as e:
            self.fail(f"IsolationForest failed to fit the data: {e}")

        # If no exception, the data is acceptable
        print("Data is acceptable for IsolationForest.")

        # Print success message
        print("Test passed successfully.")

if __name__ == '__main__':
    unittest.main()
