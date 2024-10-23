class Parameters: 
    #---- MODEL ----#
    N_ESTIMATORS = 100
    MAX_SAMPLES = 'auto'
    CONTAMINATION = 0.1
    WINDOW_SIZE =20

    NORMAL_TRAFFIC_SIZE = 20000
    JAMMING_TRAFFIC_SIZE = 5000

    #---- CONTAMINATION TEST ----#
    START_CONTAMINATION = 0.01
    END_CONTAMINATION = 0.5
    STEP_SIZE_CONTAMINATION = 0.01

    #---- ESTIMATORS TEST ----#
    START_ESTIMATORS = 1
    END_ESTIMATORS = 100
    STEP_SIZE_ESTIMATORS = 1

    #---- MAX SAMPLES TEST ----#
    START_MAX_SAMPLES = 1
    END_MAX_SAMPLES = 100
    STEP_SIZE_MAX_SAMPLES = 1

    #---- TESTING SAMPLES SIZE TEST ----#
    START_TESTING_SAMPLES_SIZE = 1
    END_TESTING_SAMPLES_SIZE = 20000
    STEP_SIZE_TESTING_SAMPLES_SIZE = 100

    #---- TRAINING SAMPLES SIZE TEST ----#

    START_TRAINING_SAMPLES_SIZE = 100
    END_TRAINING_SAMPLES_SIZE = 1000
    STEP_SIZE_TRAINING_SAMPLES_SIZE = 100

    #---- WINDOW SIZE TEST ----#
    START_WINDOW_SIZE = 1
    END_WINDOW_SIZE = 100
    STEP_SIZE_WINDOW_SIZE = 1

    #---- MODEL LABELING ----#
    INLIERS = 1
    OUTLIERS = -1

    #---- TESTED PARAMETERS ----#
    N_ESTIMATORS_ID = "n_estimators"
    CONTAMINATION_ID = "contamination"
    MAX_SAMPLES_ID = "max_samples"
    TESTING_SAMPLES_SIZE_ID = "testing_samples_size"
    TRAINING_SAMPLES_SIZE_ID = "training_samples_size"
    WINDOW_SIZE_ID = "window_size"

    #---- CLASSIFIER TYPES ----#
    STANDARD_ISOLATION_FOREST = 'Standard Isolation Forest'
    MAJORITY_RULE_ISOLATION_FOREST = 'Majority Rule Isolation Forest'

#--------------------------

    #---- JAMMING FILES ----#
    JAMMING_NEG10DBM_FILE = 'data/Jamming neg10dBm.csv'
    JAMMING_NEG40DBM_FILE = 'data/Jamming neg40dbm.csv'
    JAMMING_10DBM_FILE = 'data/Jamming 10dbm.csv'

    #JAMMING_NEG10DBM_FILE = '/home/aure/PycharmProjects/JammingAttacksAnomalyDetection-Revised/data/Jamming neg10dBm.csv'
    #JAMMING_NEG40DBM_FILE = '/home/aure/PycharmProjects/JammingAttacksAnomalyDetection-Revised/data/Jamming neg40dBm.csv'
    #JAMMING_10DBM_FILE = '/home/aure/PycharmProjects/JammingAttacksAnomalyDetection-Revised/data/Jamming 10dBm.csv'
    NORMAL_TRAFFIC_FILE = 'data/5GHz Background.csv'

    #---- JAMMING SIGNALS ----#
    JAMMING_10DBM = 1
    JAMMING_NEG10DBM = 2
    JAMMING_NEG40DBM = 3
    NORMAL_TRAFFIC = 0

    #---- JAMMING TYPES ----#
    CONSTANT_JAMMING = 1000
    PERIODIC_JAMMING = 1001
    ALTERNATING_PERIODIC_JAMMING = 1002
    DISTANCE_PERIODIC_JAMMING = 1003
    RANDOM_PERIODIC_JAMMING = 1004
    TWO_RANDOM_PERIODIC_JAMMING = 2000