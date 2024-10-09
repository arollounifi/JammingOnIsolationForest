#Represents the result of a test
class TestResult: 
    def __init__ (self, inputData, n_estimators, contamination, max_samples, classification, resultMetrics, trainingTime = None, classificationTime = None): 
        self.inputData = inputData
        self.n_estimators = n_estimators
        self.contamination = contamination
        self.max_samples = max_samples
        self.classification = classification
        self.resultMetrics = resultMetrics
        self.classificationTime = classificationTime
        self.trainingTime = trainingTime
    
    def __str__(self):
        toString =  f"n_estimators: {self.n_estimators}, contamination: {self.contamination}, testing_size: {len(self.inputData)} resultMetrics: {self.resultMetrics}"
        if (self.classificationTime is not None): 
            toString += f"\n\tClassification time: {self.classificationTime}ms"
        if (self.trainingTime is not None):
            toString += f"\n\tTraining time: {self.trainingTime} ms"
        return toString


