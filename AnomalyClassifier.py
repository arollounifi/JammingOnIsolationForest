import numpy as np
from sklearn.ensemble import IsolationForest

#Questa classe rappresenta proprio il ML isolation forest nella sua verisione classica

class AnomalyClassifier: 
    
    #Standard isolation forest classifier
    def __init__ (self, trainingSample, n_estimators, contamination, max_samples):
        if not isinstance(trainingSample, np.ndarray):
            raise ValueError("trainingSample must be a NumPy array")
        if trainingSample.ndim != 2 or trainingSample.shape[1] != 2:
            raise ValueError("trainingSample must be a 2D array with exactly 2 columns (for rssi and max_magnitude)")

        self.__trainingSample = trainingSample
        self.__n_estimators = n_estimators
        self.__contamination = contamination
        self.__max_samples = max_samples
        self.__model = None

    #trains the model on the parameters given in the constructor
    def trainModel (self):
        self.__model = IsolationForest(n_estimators=self.__n_estimators, contamination=self.__contamination, max_samples=self.__max_samples, max_features=2)

        #print("Type of self.__trainingSample:", type(self.__trainingSample))
        #print("Shape of self.__trainingSample:", self.__trainingSample.shape)
        #print("First few elements of self.__trainingSample:", self.__trainingSample[:5])
        #print(f"Training model with n_estimators={self.__n_estimators}")

        self.__model.fit(self.__trainingSample)

    #classifies the passed data (the data should be a numpy array)
    def classify (self, data): 
        if (self.__model is None): 
            raise Exception('Model not trained')

        if not isinstance(data, np.ndarray):
            raise ValueError("data must be a NumPy array")
        if data.ndim != 2 or data.shape[1] != 2:
            raise ValueError("data must be a 2D array with exactly 2 columns (for rssi and max_magnitude)")

        return self.__model.predict(data)