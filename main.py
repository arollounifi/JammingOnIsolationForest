from TestCaseLauncher import TestCaseLauncher
from Parameters import Parameters

# TODO :
#  - testare con incremento dei parametri
#  - testare con incremento della dimensione
#  - calcolare media di X esecuzioni

def main():
    runTestsInPaperOrder(Parameters.MAJORITY_RULE_ISOLATION_FOREST, Parameters.WINDOW_SIZE)


def runTestsInPaperOrder(classifierType, windowSize=None):
    tcl = TestCaseLauncher(Parameters.N_ESTIMATORS, Parameters.MAX_SAMPLES, Parameters.CONTAMINATION, Parameters.NORMAL_TRAFFIC_SIZE, Parameters.JAMMING_TRAFFIC_SIZE, classifierType, windowSize)
    #tcl.increasingMetricParameterTest(Parameters.TWO_RANDOM_PERIODIC_JAMMING, Parameters.MAX_SAMPLES_ID, Parameters.START_MAX_SAMPLES, Parameters.END_MAX_SAMPLES, Parameters.STEP_SIZE_MAX_SAMPLES, True, True)
    tcl.increasingMetricParameterTest(Parameters.PERIODIC_JAMMING, Parameters.N_ESTIMATORS_ID, Parameters.START_ESTIMATORS, Parameters.END_ESTIMATORS, Parameters.STEP_SIZE_ESTIMATORS, True, True)
    #tcl.increasingMetricParameterTest(Parameters.TWO_RANDOM_PERIODIC_JAMMING, Parameters.CONTAMINATION_ID, Parameters.START_CONTAMINATION, Parameters.END_CONTAMINATION, Parameters.STEP_SIZE_CONTAMINATION, True, True)

if __name__ == '__main__':
    main()
