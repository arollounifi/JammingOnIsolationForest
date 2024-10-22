from copyreg import constructor

import numpy as np
from matplotlib import pyplot as plt

from Parameters import Parameters
from TestRunner import TestRunner
from Plotter import Plotter
from TestResult import TestResult

from JammingAttack import JammingAttack
from AlternatingPeriodic_JammingAttack import AlternatingPeriodic_JammingAttack
from DistancePeriodic_JammingAttack import DistancePeriodic_JammingAttack
from Periodic_JammingAttack import Periodic_JammingAttack
from RandomPeriodic_JammingAttack import RandomPeriodic_JammingAttack
from TwoRandom_JammingAttack import TwoRandom_JammingAttack

from Constructor import Constructor


# Wrapper class for TestRunner
# This class launches the test cases by setting the parameters and plots the results
class TestCaseLauncher:

    def __init__(self, n_estimators, max_samples, contamination, normal_traffic_size, jamming_traffic_size, classifierType=Parameters.STANDARD_ISOLATION_FOREST, windowSize=None):

        self.__nEstimators = n_estimators
        self.__maxSamples = max_samples
        self.__contamination = contamination
        self.__tr = None
        self.__classifierType = classifierType
        self.__windowSize = windowSize

        self.normal_traffic_size = normal_traffic_size
        self.jamming_traffic_size = jamming_traffic_size

    def __getJammingAndGroundTruth(self, jammingType):
        match jammingType:
            case Parameters.CONSTANT_JAMMING:
                attack = JammingAttack(self.jamming_traffic_size)
                data, groundTruth = attack.generateJamming()
            case Parameters.PERIODIC_JAMMING:
                attack = Periodic_JammingAttack(self.jamming_traffic_size, Parameters.JAMMING_10DBM)
                data, groundTruth = attack.generateJamming()
            case Parameters.ALTERNATING_PERIODIC_JAMMING:
                attack = AlternatingPeriodic_JammingAttack(self.jamming_traffic_size, [Parameters.JAMMING_10DBM, Parameters.JAMMING_NEG10DBM])
                data, groundTruth = attack.generateJamming()
            case Parameters.DISTANCE_PERIODIC_JAMMING:
                attack = DistancePeriodic_JammingAttack(self.jamming_traffic_size)
                data, groundTruth = attack.generateJamming()
            case Parameters.RANDOM_PERIODIC_JAMMING:
                attack = RandomPeriodic_JammingAttack(self. jamming_traffic_size)
                data, groundTruth = attack.generateJamming()
            case Parameters.TWO_RANDOM_PERIODIC_JAMMING:
                attack = TwoRandom_JammingAttack(self.jamming_traffic_size, [Parameters.JAMMING_10DBM, Parameters.JAMMING_NEG10DBM])
                data, groundTruth = attack.generateJamming()
            case _:
                raise Exception('Invalid jamming type')

        if not isinstance(data, np.ndarray):
            raise ValueError("Expected jamming data to be a NumPy array")
        if data.ndim != 2:
            raise ValueError("Expected jamming data to be a 2D array")
        if data.shape[1] != 2:
            raise ValueError("Expected jamming data to have 2 columns (rssi and max_magnitude)")

        #self.print_data(data)

        return data, groundTruth

    def print_data(self, data):
        plt.figure()
        plt.plot(data[:, 0], label='RSSI')
        plt.title('Normal Values - RSSI')
        plt.xlabel('Index')
        plt.ylabel('RSSI (dBm)')
        plt.legend()
        plt.show()
        # Plot max_magnitude
        plt.figure()
        plt.plot(data[:, 1], label='Max Magnitude')
        plt.title('Normal Values - Max Magnitude')
        plt.xlabel('Index')
        plt.ylabel('Max Magnitude')
        plt.legend()
        plt.show()

    def __getNormalTraffic(self):
        jammingStructure = []
        constructor = Constructor()
        jammingStructure.append([0, self.normal_traffic_size, Parameters.NORMAL_TRAFFIC])
        normalValues, NormalGroundTruth = constructor.assemble(jammingStructure)

        if not isinstance(normalValues, np.ndarray):
            raise ValueError("Expected normal traffic data to be a NumPy array")
        if normalValues.ndim != 2:
            raise ValueError("Expected normal traffic data to be a 2D array")
        if normalValues.shape[1] != 2:
            raise ValueError("Expected normal traffic data to have 2 columns (rssi and max_magnitude)")

        #self.print_data(normalValues)

        return normalValues, NormalGroundTruth

    # Prepares the model for the test. Test input is the normal traffic concatenated with the jamming signal
    def __prepareModel(self, jammingType):
        trainingSample, trainingSampleGoundTruth = self.__getNormalTraffic()
        jammingTestInput, jammingGroundTruth = self.__getJammingAndGroundTruth(jammingType)

        #print(f"Training sample shape: {trainingSample.shape}")
        #print(f"Testing sample shape: {jammingTestInput.shape}")
        #print(f"Ground truth length: {len(jammingGroundTruth)}")

        self.__tr = TestRunner(trainingSample, jammingTestInput, jammingGroundTruth, self.__nEstimators, self.__contamination, self.__maxSamples, self.__classifierType, self.__windowSize)

    #EX __runBasicTest + basicNormalJammingConcatenatedTest
    def runSelectedTest(self, jammingType, graphTitle, displayResultMetrics = True, displayPlot = True):
        self.__prepareModel(jammingType)
        result = self.__tr.runTest()
        if displayResultMetrics:
            print(result)
        if displayPlot:
            self.__plotInliersOutliers(result, ['Normal Traffic', 'Jamming Signal'], ['b', 'r'], graphTitle, ['Data Point', 'RSS[dBm]', 'Max Magnitude'])

    # Runs tests where a parameter is increased in a range
    def increasingMetricParameterTest(self, jammingType, parameter_id, startValue, endValue, stepSize, displayResultMetrics=True, displayPlot=True):
        self.__prepareModel(jammingType)
        results = self.__tr.increasingParameterTest(startValue, endValue, stepSize, parameter_id)
        if displayResultMetrics:
            for result in results:
                print(result)
        if displayPlot:
            x = np.arange(startValue, endValue, stepSize)
            self.__plotMetrics(x, results, ['Accuracy', 'Precision', 'Recall', 'F1'], ['b', 'r', 'g', 'm'],
                               'Impact of ' + parameter_id + ' variation on performance metrics',
                               [parameter_id, 'Metric Value'])

    #Generates and visualizes the ground truth for the jamming signal
    def groundTruthTest(self, jammingType):
        signal, groundTruth = self.__getJammingAndGroundTruth(jammingType)
        r = TestResult(signal, 0, 0, 0, groundTruth, None)
        self.__plotInliersOutliers(r, ['Normal Traffic', 'Jamming Signal'], ['b', 'r'], 'Ground truth definition',
                                   ['Data Point', 'RSS[dBm]', ])

    # Visualizes the input data for the jamming signal
    def inputTest(self, jammingType):
        jammingSignal, groundTruth = self.__getJammingAndGroundTruth(jammingType)
        Plotter.plotSegmentedGraph(range(len(jammingSignal)), jammingSignal[:,0], jammingSignal[:,1], self.normal_traffic_size, 'b', 'r',
                                   'Input data in the case of Constant Jamming', ['Data Point', 'RSS[dBm]'],
                                   ['Normal Traffic', 'Jamming Signal'])

    # time test with increasing metric value
    def increasingMetricTimeTest(self, jammingType, parameter_id, startValue, endValue, stepSize, displayResultMetrics=True, displayPlot=True):
        self.__prepareModel(jammingType)
        results = self.__tr.increasingTimeTest(startValue, endValue, stepSize, parameter_id)
        if displayResultMetrics:
            for result in results:
                print(result)
            averageTrainingTime = np.mean([result.trainingTime for result in results])
            averageClassificationTime = np.mean([result.classificationTime for result in results])
            print(f"Average training time: {averageTrainingTime}ms")
            print(f"Average classification time: {averageClassificationTime}ms")
        if displayPlot:
            x = np.arange(startValue, endValue, stepSize)
            self.__plotTime(x, results, ['Training Time', 'Classification Time'], ['b', 'r'],
                            'Impact of ' + parameter_id + ' variation on ', [parameter_id, 'Time[ms]'])

    # Compares the performance of two models based on a parameter
    def compareModels(self, jammingType, parameter_id, startValue, endValue, stepSize, models, plotColors, displayResultMetrics=True, displayPlot=True):
        results = []
        for model in models:
            self.__classifierType = model
            self.__prepareModel(jammingType)
            results.append(self.__tr.increasingTimeTest(startValue, endValue, stepSize, parameter_id))
        if displayResultMetrics:
            for result in results:
                for r in result:
                    print(r)
        if displayPlot:
            x = np.arange(startValue, endValue, stepSize)
            trainingTimes = [[result.trainingTime for result in res] for res in results]
            classificationTimes = [[result.classificationTime for result in res] for res in results]
            Plotter.plotInSameGraph(x, trainingTimes, models, plotColors,
                                    'Impact of ' + parameter_id + ' variation on training time',
                                    [parameter_id, 'Time[ms]'])
            Plotter.plotInSameGraph(x, classificationTimes, models, plotColors,
                                    'Impact of ' + parameter_id + ' variation on classification time',
                                    [parameter_id, 'Time[ms]'])

    # Splits the data points based on the classification results
    def __separateInliersFromOutliers(self, inputData, classificationResults):

        x = range(len(inputData))
        normal_x = [x[i] for i in range(len(x)) if classificationResults[i] == 1]
        normal_y = [inputData[i] for i in range(len(inputData)) if classificationResults[i] == 1]
        jamming_x = [x[i] for i in range(len(x)) if classificationResults[i] == -1]
        jamming_y = [inputData[i] for i in range(len(inputData)) if classificationResults[i] == -1]
        return [normal_x, jamming_x], [normal_y, jamming_y]  # restituisce 2 liste a loro volta composte da 2 liste

    # Plotting function for the scatter plot of inliers and outliers (shows the model classification)
    def __plotInliersOutliers(self, result, labels, colors, title, axisLabels):
        x, result_rssi = self.__separateInliersFromOutliers(result.inputData[:, 0], result.classification)  # Separazione per rssi
        _, result_max_magnitude = self.__separateInliersFromOutliers(result.inputData[:, 1], result.classification)  # Separazione per max_magnitude

        # Plot RSSI
        Plotter.scatterPlot(x, result_rssi, labels, colors, ' - RSSI', axisLabels)

        # Plot Max Magnitude
        Plotter.scatterPlot(x, result_max_magnitude, labels, colors, ' - Max Magnitude', axisLabels)

    # raccoglie in diverse liste i vari parametri in delle liste di risultati
    # usato per rappresentare come variano le performance quando vario i parametri
    def __plotMetrics(self, x, results, labels, colors, title, axisLabels):
        accuracy = [result.resultMetrics.accuracy for result in results]  # raccoglie tutte le accuracy
        precision = [result.resultMetrics.precision for result in results]  # raccoglie tutte le preicison
        recall = [result.resultMetrics.recall for result in results]  # raccoglie tutti i racell
        f1 = [result.resultMetrics.f1 for result in results]  # raccoglie tutti gli f1
        Plotter.plotInSameGraph(x, [accuracy, precision, recall, f1], labels, colors, title,
                                axisLabels)  # stampa tutti i risultati raccolti

    # raccoglie in diverse liste i vari tempi delle liste dei risultati
    # usato per rappresentare come vairano i tempi di esecuzione ed addestramento al variare dei parametri
    def __plotTime(self, x, results, labels, colors, title, axisLabels):
        trainingTime = [result.trainingTime for result in results]  # raccoglie tutti i tempi di addestrameto
        classificationTime = [result.classificationTime for result in
                              results]  # raccoglie tutti i tempi di classificazione
        Plotter.plotInSameGraph(x, [trainingTime], [labels[0]], colors[0], title + labels[0], axisLabels)
        Plotter.plotInSameGraph(x, [classificationTime], [labels[1]], colors[1], title + labels[1], axisLabels)

