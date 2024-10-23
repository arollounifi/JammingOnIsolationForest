import random

import numpy as np

from FileHandler import FileHandler
from Parameters import Parameters
import pandas as pd



class Constructor:
    def __init__(self):
        self.__normalValues = FileHandler.readAndParseFile(Parameters.NORMAL_TRAFFIC_FILE, Parameters.NORMAL_TRAFFIC_SIZE)
        self.__jammingValues_10dBm = FileHandler.readAndParseFile(Parameters.JAMMING_10DBM_FILE, Parameters.JAMMING_TRAFFIC_SIZE)
        self.__jammingValues_neg10dBm = FileHandler.readAndParseFile(Parameters.JAMMING_NEG10DBM_FILE, Parameters.JAMMING_TRAFFIC_SIZE)
        self.__jammingValues_neg40dBm = FileHandler.readAndParseFile(Parameters.JAMMING_NEG40DBM_FILE, Parameters.JAMMING_TRAFFIC_SIZE)

        if not isinstance(self.__normalValues, np.ndarray):
            raise ValueError("Expected normal traffic data to be a NumPy array")
        if self.__normalValues.ndim != 2:
            raise ValueError("Expected normal traffic data to be a 2D array")
        if self.__normalValues.shape[1] != 2:
            raise ValueError("Expected normal traffic data to have 2 columns (rssi and max_magnitude)")

        if not isinstance(self.__jammingValues_10dBm, np.ndarray):
            raise ValueError("Expected normal traffic data to be a NumPy array")
        if self.__jammingValues_10dBm.ndim != 2:
            raise ValueError("Expected normal traffic data to be a 2D array")
        if self.__jammingValues_10dBm.shape[1] != 2:
            raise ValueError("Expected normal traffic data to have 2 columns (rssi and max_magnitude)")

        self.__lastNormalIndex = 0
        self.__lastJamming10dBmIndex = 0
        self.__lastJammingNeg10dBmIndex = 0
        self.__lastJammingNeg40dBmIndex = 0

    def getJammingValues(self, type, size):
        if type == Parameters.JAMMING_10DBM:
            jammingValues = self.__jammingValues_10dBm[self.__lastJamming10dBmIndex:self.__lastJamming10dBmIndex + size]
            self.__lastJamming10dBmIndex += size
            return jammingValues

        elif type == Parameters.JAMMING_NEG10DBM:
            jammingValues = self.__jammingValues_neg10dBm[self.__lastJammingNeg10dBmIndex:self.__lastJammingNeg10dBmIndex + size]
            #jammingValues = self.dirtyValues(jammingValues, 0.021429, 1.345)
            self.__lastJammingNeg10dBmIndex += size
            return jammingValues

        elif type == Parameters.JAMMING_NEG40DBM:
            jammingValues = self.__jammingValues_neg40dBm[self.__lastJammingNeg40dBmIndex:self.__lastJammingNeg40dBmIndex + size]
            #jammingValues = self.dirtyValues(jammingValues, 0.021429, 2.345)
            self.__lastJammingNeg40dBmIndex += size
            return jammingValues

        else:
            raise Exception("The jamming type is not valid")

    def dirtyValues(self, data, anomalyRate, anomalyFactor, scale = 5):

        pd_data = pd.Series(data[:,0].flatten())

        meanDaata = pd_data.mean()
        stdData = pd_data.std()

        upperBound = meanDaata + anomalyFactor * stdData
        lowerBound = meanDaata - anomalyFactor * stdData
        numAnomalies = int(len(data) * anomalyRate)
        anomalyIndices = np.random.choice(pd_data.index, numAnomalies, replace=False)

        for index in anomalyIndices:
            if np.random.rand() > 0.5:
                data[index, 0] = upperBound + np.random.exponential(scale=scale)
                #data[index, 1] = upperBound + np.random.exponential(scale=scale)

            else:
                data[index, 0] = lowerBound - np.random.exponential(2)
                #data[index, 1] = upperBound + np.random.exponential(scale=scale)


        return data

    def getNormalValues(self, size, training = False):
        if training == True:
            jammingValues = self.__normalValues[0:size]
            jammingValues = self.dirtyValues(jammingValues, 0.351429, 2.345)
            return jammingValues

        jammingValues = self.__normalValues[self.__lastNormalIndex:self.__lastNormalIndex + size]
        jammingValues = self.dirtyValues(jammingValues, 0.351429, 2.345)
        self.__lastNormalIndex += size

        '''if jammingValues.ndim > 1 and jammingValues.shape[1] > 1:  # Check if it's a 2D array
            first_column = jammingValues[:, 0]  # Select the first column
        else:
            first_column = jammingValues  # If it's 1D, use the values as is

        # Save the first column to a text file, one value per line
        with open('normal_values.txt', 'w') as f_values:
            for value in first_column.flatten():
                f_values.write(f'{value:.2f}\n')  # Save each value on a new line with 2 decimal places'''


        return jammingValues

    def assemble(self, jammingStructure, training = False):
        if jammingStructure is None or len(jammingStructure) == 0:
            raise Exception("The jamming structure is empty")

        if training == True:
            start_idx = jammingStructure[0]
            end_idx = jammingStructure[1]
            size = end_idx - start_idx
            self.getNormalValues(size, training = True)


        self.__lastJammingNeg10dBmIndex = 0
        self.__lastJammingNeg40dBmIndex = 0
        self.__lastJamming10dBmIndex = 0
        self.__lastNormalIndex = 0

        jammingValues_list = []
        groundTruth = []

        for element in jammingStructure:
            start_idx = element[0]
            end_idx = element[1]
            size = end_idx - start_idx
            if element[2] != Parameters.NORMAL_TRAFFIC:
                data = self.getJammingValues(element[2], size)

                #print(f"getJammingValues returned data of type {type(data)} and shape {data.shape}")

                jammingValues_list.append(data)
                groundTruth.extend([Parameters.OUTLIERS] * size)
            else:
                data = self.getNormalValues(size)

                #print(f"getNormalValues returned data of type {type(data)} and shape {data.shape}")

                jammingValues_list.append(data)
                groundTruth.extend([Parameters.INLIERS] * size)

        jammingValues = np.concatenate(jammingValues_list)
        ground = np.array(groundTruth)

        '''# Export only the first column of the jammingValues matrix to a text file
        if jammingValues.ndim > 1 and jammingValues.shape[1] > 1:  # Check if it's a 2D array
            first_column = jammingValues[:, 0]  # Select the first column
        else:
            first_column = jammingValues  # If it's 1D, use the values as is

        # Save the first column to a text file, one value per line
        with open('jamming_values_first_column.txt', 'w') as f_values:
            for value in first_column.flatten():
                f_values.write(f'{value:.2f}\n')  # Save each value on a new line with 2 decimal places

        # Save ground truth to a separate text file, one value per line
        with open('ground_truth.txt', 'w') as f_ground:
            for label in ground:
                f_ground.write(f'{label}\n')  # Save each ground truth label on a new line'''

        return jammingValues, ground



    #GETTERS AND SETTERS
    def get_NormalValues(self):
        return self.__normalValues

    def get_JammingValues_10dBm(self):
        return self.__jammingValues_10dBm

    def get_JammingValues_neg10dBm(self):
        return self.__jammingValues_neg10dBm

    def get_JammingValues_neg40dBm(self):
        return self.__jammingValues_neg40dBm

    def get_LastNormalIndex(self):
        return self.__lastNormalIndex

    def get_LastJamming10dBmIndex(self):
        return self.__lastJamming10dBmIndex

    def get_LastJammingNeg10dBmIndex(self):
        return self.__lastJammingNeg10dBmIndex

    def get_LastJammingNeg40dBmIndex(self):
        return self.__lastJammingNeg40dBmIndex