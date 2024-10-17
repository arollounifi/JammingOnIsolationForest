import numpy as np
from sklearn.ensemble import IsolationForest

#Questa classe rappresenta proprio il ML isolation forest nella sua verisione classica

class AnomalyClassifier: 
    
    #Standard isolation forest classifier
    def __init__ (self, trainingSample, n_estimators, contamination, max_samples):
        #trainingSample = np.array(trainingSample).reshape(-1, 1)
        self.__trainingSample = trainingSample
        self.__n_estimators = n_estimators
        self.__contamination = contamination
        self.__max_samples = max_samples
        self.__model = None

    #trains the model on the parameters given in the constructor
    def trainModel (self):
        self.__model = IsolationForest(n_estimators=self.__n_estimators, contamination=self.__contamination, max_samples=self.__max_samples, random_state=42, max_features=1.0)

        print("Type of self.__trainingSample:", type(self.__trainingSample))
        print("Shape of self.__trainingSample:", self.__trainingSample.shape)
        print("First few elements of self.__trainingSample:", self.__trainingSample[:5])

        self.__model.fit(self.__trainingSample)

    #classifies the passed data (the data should be a numpy array)
    def classify (self, data): 
        if (self.__model is None): 
            raise Exception('Model not trained')
        return self.__model.predict(data)