from copyreg import constructor

import numpy as np

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

# ---- DATA ----#

# NORMAL_TRAFFIC_FILE = 'data/normal_traffic.txt'

# CONSTANT_JAMMING_FILE = 'data/constant_jammer.txt'

# PERIODIC_JAMMING_FILE = 'data/periodic_jammer.txt'


# Wrapper class for TestRunner
# This class launches the test cases by setting the parameters and plots the results
class TestCaseLauncher:

    def __init__(self, n_estimators, max_samples, contamination, normal_traffic_size, jamming_traffic_size,
                 classifierType=Parameters.STANDARD_ISOLATION_FOREST, windowSize=None):
        # self.__normalTraffic = FileHandler.readAndParseFile(NORMAL_TRAFFIC_FILE, normal_traffic_size)
        # self.__constantJamming = FileHandler.readAndParseFile(CONSTANT_JAMMING_FILE, constant_jamming_size)
        # self.__periodicJamming = FileHandler.readAndParseFile(PERIODIC_JAMMING_FILE, periodic_jamming_size)
        self.__nEstimators = n_estimators
        self.__maxSamples = max_samples
        self.__contamination = contamination
        self.__tr = None
        self.__classifierType = classifierType
        self.__windowSize = windowSize

        self.normal_traffic_size = normal_traffic_size
        self.jamming_traffic_size = jamming_traffic_size

    def __getJammingAndGruondTruth(self, jammingType):
        match jammingType:
            case Parameters.CONSTANT_JAMMING:
                attack = JammingAttack(self.normal_traffic_size)
                return attack.generateJamming()
            case Parameters.PERIODIC_JAMMING:
                attack = Periodic_JammingAttack(Parameters.JAMMING_10DBM)
                return attack.generateJamming()
            case Parameters.ALTERNATING_PERIODIC_JAMMING:
                attack = AlternatingPeriodic_JammingAttack([Parameters.JAMMING_10DBM, Parameters.JAMMING_NEG10DBM])
                return attack.generateJamming()
            case Parameters.DISTANCE_PERIODIC_JAMMING:
                attack = DistancePeriodic_JammingAttack(Parameters.JAMMING_10DBM)
                return attack.generateJamming()
            case Parameters.RANDOM_PERIODIC_JAMMING:
                attack = RandomPeriodic_JammingAttack(Parameters.JAMMING_10DBM)
                return attack.generateJamming()
            case Parameters.TWO_RANDOM_PERIODIC_JAMMING:
                attack = TwoRandom_JammingAttack([Parameters.JAMMING_10DBM, Parameters.JAMMING_NEG10DBM])
                return attack.generateJamming()
            case _:
                raise Exception('Invalid jamming type')

    def __getNormalTraffic(self):
        jammingStructure = []
        constructor = Constructor()
        jammingStructure.append([0, self.normal_traffic_size, Parameters.NORMAL_TRAFFIC])
        return constructor.assemble(jammingStructure)

    # Prepares the model for the test. Test input is the normal traffic concatenated with the jamming signal
    def __prepareModel(self, jammingType):
        trainingSample = self.__getNormalTraffic()
        jammingTestInput, jammingGroundTruth = self.__getJammingAndGruondTruth(jammingType)
        # testInput = np.concatenate((trainingSample, jammingTestInput))
        # groundTruth = np.concatenate((self.__getNormalTrafficGroundTruth(), jammingGroundTruth))
        self.__tr = TestRunner(trainingSample, jammingTestInput, jammingGroundTruth, self.__nEstimators,
                               self.__contamination, self.__maxSamples, self.__classifierType, self.__windowSize)

    # Splits the data points based on the classification results
    # TODO documentare meglio questa funzione
    def __separateInliersFromOutliers(self, inputData, classificationResults):
        x = range(len(inputData))
        normal_x = [x[i] for i in range(len(x)) if classificationResults[i] == 1]
        normal_y = [inputData[i] for i in range(len(inputData)) if classificationResults[i] == 1]
        jamming_x = [x[i] for i in range(len(x)) if classificationResults[i] == -1]
        jamming_y = [inputData[i] for i in range(len(inputData)) if classificationResults[i] == -1]
        return [normal_x, jamming_x], [normal_y, jamming_y]  # restituisce 2 liste a loro volta composte da 2 liste

    # Plotting function for the scatter plot of inliers and outliers (shows the model classification)
    def __plotInliersOutliers(self, result, labels, colors, title, axisLabels):
        x, result = self.__separateInliersFromOutliers(result.inputData, result.classification)
        Plotter.scatterPlot(x, result, labels, colors, title, axisLabels)

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

    # Simple normal traffic concatenated with constant jamming test
    def basicNormalJammingConcatenatedTest(self, jammingType, displayResultMetrics=True, displayPlot=True):
        self.__prepareModel(jammingType)
        self.__runBasicTest('Model classification of Normal Traffic and Jamming Signal', displayResultMetrics,
                            displayPlot)

    def __runBasicTest(self, graphTitle, displayResultMetrics=True, displayPlot=True):
        result = self.__tr.runTest()
        if displayResultMetrics:
            print(result)
        if displayPlot:
            self.__plotInliersOutliers(result, ['Normal Traffic', 'Jamming Signal'], ['b', 'r'], graphTitle,
                                       ['Data Point', 'RSS[dBm]'])

    '''
    Mi servono i seguenti test per ogni tipo
        uno normale
    '''

    # Runs tests where a parameter is increased in a range
    def increasingMetricParameterTest(self, jammingType, parameter_id, startValue, endValue, stepSize,
                                      displayResultMetrics=True, displayPlot=True):
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

    # TODO da sistema per adattarlo al nuovo sistema
    '''def groundTruthTest(self, jammingType):
        signal, groundTruth = self.__getJammingSignalAndGroundTruth(jammingType)
        r = TestResult(signal, 0, 0, 0, groundTruth, None)
        self.__plotInliersOutliers(r, ['Normal Traffic', 'Jamming Signal'], ['b', 'r'], 'Ground truth definition',
                                   ['Data Point', 'RSS[dBm]'])

    def inputTest(self, jammingType):
        jammingSignal, groundTruth = self.__getJammingSignalAndGroundTruth(jammingType)
        testedSignal = np.concatenate((self.__normalTraffic, jammingSignal))
        Plotter.plotSegmentedGraph(range(len(testedSignal)), testedSignal, len(self.__normalTraffic), 'b', 'r',
                                   'Input data in the case of Constant Jamming', ['Data Point', 'RSS[dBm]'],
                                   ['Normal Traffic', 'Jamming Signal'])'''

    # time test with increasing metric value
    #TODO da adattare al nuovo sistema
    def increasingMetricTimeTest(self, jammingType, parameter_id, startValue, endValue, stepSize,
                                 displayResultMetrics=True, displayPlot=True):
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
    #TODO da adattare al nuovo sistema
    def compareModels(self, jammingType, parameter_id, startValue, endValue, stepSize, models, plotColors,
                      displayResultMetrics=True, displayPlot=True):
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

    # Vecchi metodi non più usati
    '''
    #returns the ground truth for the various types of data
    def __getNormalTrafficGroundTruth(self): 
        return Parameters.INLIERS * np.ones(len(self.__normalTraffic))
    def __getConstantJammingGroundTruth(self): 
        return Parameters.OUTLIERS * np.ones(len(self.__constantJamming))
    def __getPeriodicJammingGroundTruth(self): 
        start_offset = 293
        pause = 557
        jamming_time = 372

        samplesNumber = len(self.__periodicJamming)

        ground_truth = Parameters.INLIERS * np.ones(samplesNumber)

        for i in range (0, int(samplesNumber/(jamming_time + pause)) + 1): 
            jamming_start = start_offset + i *(jamming_time + pause)
            jamming_end = jamming_start + jamming_time
            if (jamming_start >= samplesNumber):
                break
            if (jamming_end >= samplesNumber):
                jamming_end = samplesNumber
            ground_truth[jamming_start:jamming_end] = Parameters.OUTLIERS
        return ground_truth

    def __getJammingSignalAndGroundTruth(self, signalType):
        if signalType == Parameters.CONSTANT_JAMMING: 
            return self.__constantJamming, self.__getConstantJammingGroundTruth()
        elif signalType == Parameters.PERIODIC_JAMMING: 
            return self.__periodicJamming, self.__getPeriodicJammingGroundTruth()
        else: 
            raise Exception('Invalid signal type')

    def basicOnlyJammingTest(self, jammingType, displayResultMetrics = True, displayPlot = True):
        trainingSample = self.__normalTraffic
        jammingTestInput, jammingGroundTruth = self.__getJammingSignalAndGroundTruth(jammingType)
        self.__tr = TestRunner(trainingSample, jammingTestInput, jammingGroundTruth, self.__nEstimators, self.__contamination, self.__maxSamples, self.__classifierType, self.__windowSize)
        self.__runBasicTest('Model classification of Jamming Signal', displayResultMetrics, displayPlot)

    def basicOnlyNormalTrafficTest(self, displayResultMetrics = True, displayPlot = True):
        trainingSample = self.__normalTraffic
        testInput = self.__normalTraffic
        groundTruth = self.__getNormalTrafficGroundTruth()
        self.__tr = TestRunner(trainingSample, testInput, groundTruth, self.__nEstimators, self.__contamination, self.__maxSamples, self.__classifierType, self.__windowSize)
        self.__runBasicTest('Model classification of Normal Traffic', displayResultMetrics, displayPlot)
    '''