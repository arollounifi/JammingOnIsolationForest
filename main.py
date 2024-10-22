from TestCaseLauncher import TestCaseLauncher
from Parameters import Parameters

# TODO :
#  - testare con incremento dei parametri
#  - testare con incremento della dimensione
#  - calcolare media di X esecuzioni

def main():
    runTestsInPaperOrder(Parameters.MAJORITY_RULE_ISOLATION_FOREST, Parameters.WINDOW_SIZE)

def runBasicTests(testType, logResults, plotResults, classifierType, windowSize=None):
    tcl = TestCaseLauncher(Parameters.N_ESTIMATORS, Parameters.MAX_SAMPLES, Parameters.CONTAMINATION, Parameters.NORMAL_TRAFFIC_SIZE, Parameters.JAMMING_TRAFFIC_SIZE,  classifierType, windowSize)
    tcl.runSelectedTest(testType, logResults, plotResults)


def runGroundTruthTests(testType, classifierType, windowSize=None):
    tcl = TestCaseLauncher(Parameters.N_ESTIMATORS, Parameters.MAX_SAMPLES, Parameters.CONTAMINATION, Parameters.NORMAL_TRAFFIC_SIZE, Parameters.JAMMING_TRAFFIC_SIZE, classifierType, windowSize)
    tcl.groundTruthTest(testType)


def runMetricsTests(testType, logResults, plotResults, classifierType, windowSize=None):
    tcl = TestCaseLauncher(Parameters.N_ESTIMATORS, Parameters.MAX_SAMPLES, Parameters.CONTAMINATION, Parameters.NORMAL_TRAFFIC_SIZE, Parameters.JAMMING_TRAFFIC_SIZE, classifierType, windowSize)
    tcl.increasingMetricParameterTest(testType, Parameters.CONTAMINATION_ID, Parameters.START_CONTAMINATION, Parameters.END_CONTAMINATION, Parameters.STEP_SIZE_CONTAMINATION, logResults, plotResults)
    tcl.increasingMetricParameterTest(testType, Parameters.N_ESTIMATORS_ID, Parameters.START_ESTIMATORS, Parameters.END_ESTIMATORS, Parameters.STEP_SIZE_ESTIMATORS, logResults, plotResults)
    tcl.increasingMetricParameterTest(testType, Parameters.MAX_SAMPLES_ID, Parameters.START_MAX_SAMPLES, Parameters.END_MAX_SAMPLES, Parameters.STEP_SIZE_MAX_SAMPLES, logResults, plotResults)
    tcl.increasingMetricParameterTest(testType, Parameters.WINDOW_SIZE_ID, Parameters.START_WINDOW_SIZE, Parameters.END_WINDOW_SIZE, Parameters.STEP_SIZE_WINDOW_SIZE, logResults, plotResults)


def runTimeTests(testType, logResults, plotResults, classifierType, windowSize=None):
    tcl = TestCaseLauncher(Parameters.N_ESTIMATORS, Parameters.MAX_SAMPLES, Parameters.CONTAMINATION, Parameters.NORMAL_TRAFFIC_SIZE, Parameters.JAMMING_TRAFFIC_SIZE, classifierType, windowSize)
    tcl.increasingMetricTimeTest(testType, Parameters.N_ESTIMATORS_ID, Parameters.START_ESTIMATORS, Parameters.END_ESTIMATORS, Parameters.STEP_SIZE_ESTIMATORS, logResults, plotResults)
    tcl.increasingMetricTimeTest(testType, Parameters.CONTAMINATION_ID, Parameters.START_CONTAMINATION, Parameters.END_CONTAMINATION, Parameters.STEP_SIZE_CONTAMINATION, logResults, plotResults)
    tcl.increasingMetricTimeTest(testType, Parameters.MAX_SAMPLES_ID, Parameters.START_MAX_SAMPLES, Parameters.END_MAX_SAMPLES, Parameters.STEP_SIZE_MAX_SAMPLES, logResults, plotResults)
    tcl.increasingMetricTimeTest(testType, Parameters.TESTING_SAMPLES_SIZE_ID, Parameters.START_TESTING_SAMPLES_SIZE, Parameters.END_TESTING_SAMPLES_SIZE, Parameters.STEP_SIZE_TESTING_SAMPLES_SIZE, logResults, plotResults)
    tcl.increasingMetricTimeTest(testType, Parameters.TRAINING_SAMPLES_SIZE_ID, Parameters.START_TRAINING_SAMPLES_SIZE, Parameters.END_TRAINING_SAMPLES_SIZE, Parameters.STEP_SIZE_TRAINING_SAMPLES_SIZE, logResults, plotResults)

    # jamming_size = 1 to evaluate classification time against a single data point
    jamming_traffic_size = 1

    tcl = TestCaseLauncher(Parameters.N_ESTIMATORS, Parameters.MAX_SAMPLES, Parameters.CONTAMINATION, Parameters.NORMAL_TRAFFIC_SIZE, jamming_traffic_size, classifierType, windowSize)
    tcl.increasingMetricTimeTest(testType, Parameters.MAX_SAMPLES_ID, Parameters.START_MAX_SAMPLES, Parameters.END_MAX_SAMPLES, Parameters.STEP_SIZE_MAX_SAMPLES, logResults, plotResults)


def runTestsInPaperOrder(classifierType, windowSize=None):
    tcl = TestCaseLauncher(Parameters.N_ESTIMATORS, Parameters.MAX_SAMPLES, Parameters.CONTAMINATION, Parameters.NORMAL_TRAFFIC_SIZE, Parameters.JAMMING_TRAFFIC_SIZE, classifierType, windowSize)
    #tcl.increasingMetricParameterTest(Parameters.TWO_RANDOM_PERIODIC_JAMMING, Parameters.MAX_SAMPLES_ID, Parameters.START_MAX_SAMPLES, Parameters.END_MAX_SAMPLES, Parameters.STEP_SIZE_MAX_SAMPLES, True, True)
    tcl.increasingMetricParameterTest(Parameters.PERIODIC_JAMMING, Parameters.N_ESTIMATORS_ID, Parameters.START_ESTIMATORS, Parameters.END_ESTIMATORS, Parameters.STEP_SIZE_ESTIMATORS, True, True)
    #tcl.increasingMetricParameterTest(Parameters.TWO_RANDOM_PERIODIC_JAMMING, Parameters.CONTAMINATION_ID, Parameters.START_CONTAMINATION, Parameters.END_CONTAMINATION, Parameters.STEP_SIZE_CONTAMINATION, True, True)


    #tcl = TestCaseLauncher(100, Parameters.MAX_SAMPLES, Parameters.CONTAMINATION, Parameters.NORMAL_TRAFFIC_SIZE, Parameters.JAMMING_TRAFFIC_SIZE, classifierType, windowSize)
    #tcl.runSelectedTest(Parameters.PERIODIC_JAMMING, True, True)

    #tcl = TestCaseLauncher(1000, Parameters.MAX_SAMPLES, Parameters.CONTAMINATION, Parameters.NORMAL_TRAFFIC_SIZE, Parameters.JAMMING_TRAFFIC_SIZE, classifierType, windowSize)
    #tcl.runSelectedTest(Parameters.PERIODIC_JAMMING, True, True)

    # Visualizza i dati del test
    #tcl.inputTest(Parameters.CONSTANT_JAMMING)


'''    #Test per vedere i cambiamenti di performance e di tempo al variare del numero di estimatori
    #tcl.increasingMetricParameterTest(Parameters.CONSTANT_JAMMING, Parameters.N_ESTIMATORS_ID, Parameters.START_ESTIMATORS, Parameters.END_ESTIMATORS, Parameters.STEP_SIZE_ESTIMATORS, True, True)
    #tcl.increasingMetricTimeTest(Parameters.CONSTANT_JAMMING, Parameters.N_ESTIMATORS_ID, Parameters.START_ESTIMATORS, Parameters.END_ESTIMATORS, Parameters.STEP_SIZE_ESTIMATORS, True, True)
    
    # Test per vedere i cambiamenti di performance e di tempo al variare della contaminazione
    #tcl.increasingMetricParameterTest(Parameters.CONSTANT_JAMMING, Parameters.MAX_SAMPLES_ID, Parameters.START_MAX_SAMPLES, Parameters.END_MAX_SAMPLES, Parameters.STEP_SIZE_MAX_SAMPLES, True, True)
    #tcl.increasingMetricTimeTest(Parameters.CONSTANT_JAMMING, Parameters.MAX_SAMPLES_ID, Parameters.START_MAX_SAMPLES, Parameters.END_MAX_SAMPLES, Parameters.STEP_SIZE_MAX_SAMPLES, True, True)
    
    # Test per vedere i cambiamenti di performance e di tempo al variare della contaminazione
    #tcl.increasingMetricParameterTest(Parameters.CONSTANT_JAMMING, Parameters.CONTAMINATION_ID, Parameters.START_CONTAMINATION, Parameters.END_CONTAMINATION, Parameters.STEP_SIZE_CONTAMINATION, True, True)
    #tcl.increasingMetricTimeTest(Parameters.CONSTANT_JAMMING, Parameters.CONTAMINATION_ID, Parameters.START_CONTAMINATION, Parameters.END_CONTAMINATION, Parameters.STEP_SIZE_CONTAMINATION, True, True)


    # Settaggio dei nuovi parametri per il test
    Parameters.N_ESTIMATORS = 15
    Parameters.MAX_SAMPLES = 10
    Parameters.CONTAMINATION = 0.09
    windowSize = Parameters.WINDOW_SIZE
    
    #Creao il nuovo test case launcher con i nuovi parametri
    #tcl = TestCaseLauncher(Parameters.N_ESTIMATORS, Parameters.MAX_SAMPLES, Parameters.CONTAMINATION, Parameters.NORMAL_TRAFFIC_SIZE, Parameters.JAMMING_TRAFFIC_SIZE, classifierType, windowSize)
    
    # Test su un parametro dopo i cambiamenti di valore
    #tcl.increasingMetricParameterTest(Parameters.CONSTANT_JAMMING, Parameters.WINDOW_SIZE_ID, Parameters.START_WINDOW_SIZE, Parameters.END_WINDOW_SIZE, Parameters.STEP_SIZE_WINDOW_SIZE, True, True)
    
    #tcl.compareModels(Parameters.CONSTANT_JAMMING, Parameters.TESTING_SAMPLES_SIZE_ID, Parameters.START_TESTING_SAMPLES_SIZE, Parameters.END_TESTING_SAMPLES_SIZE, Parameters.STEP_SIZE_TESTING_SAMPLES_SIZE, [Parameters.STANDARD_ISOLATION_FOREST, Parameters.MAJORITY_RULE_ISOLATION_FOREST], ['r', 'b'], True, True)

    Parameters.NORMAL_TRAFFIC_SIZE = 10000
    Parameters.CONSTANT_JAMMING_SIZE = 10000
    Parameters.PERIODIC_JAMMING_SIZE = 10000
    
    tcl = TestCaseLauncher(Parameters.N_ESTIMATORS, Parameters.MAX_SAMPLES, Parameters.CONTAMINATION, Parameters.NORMAL_TRAFFIC_SIZE, Parameters.CONSTANT_JAMMING_SIZE, Parameters.PERIODIC_JAMMING_SIZE, classifierType, windowSize)

    #tcl.basicOnlyJammingTest(Parameters.CONSTANT_JAMMING, True, True)
    tcl.basicOnlyJammingTest(Parameters.PERIODIC_JAMMING, True, True)    
    tcl.basicOnlyNormalTrafficTest(True, True)'''

if __name__ == '__main__':
    main()
