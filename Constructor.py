from FileHandler import FileHandler
from Parameters import Parameters


class Constructor:
    def __init__(self):
        self.__normalValues = FileHandler.readAndParseFile(Parameters.NORMAL_TRAFFIC_FILE, Parameters.NORMAL_TRAFFIC_SIZE)
        self.__jammingValues_10dBm = FileHandler.readAndParseFile(Parameters.JAMMING_10DBM_FILE, Parameters.CONSTANT_JAMMING_SIZE)
        self.__jammingValues_neg10dBm = FileHandler.readAndParseFile(Parameters.JAMMING_NEG10DBM_FILE, Parameters.CONSTANT_JAMMING_SIZE)
        self.__jammingValues_neg40dBm = FileHandler.readAndParseFile(Parameters.JAMMING_NEG40DBM_FILE, Parameters.CONSTANT_JAMMING_SIZE)

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
            jammingsValues = self.__jammingValues_neg10dBm[self.__lastJammingNeg10dBmIndex:self.__lastJammingNeg10dBmIndex + size]
            self.__lastJammingNeg10dBmIndex += size
            return jammingsValues

        elif type == Parameters.JAMMING_NEG40DBM:
            jammingValues = self.__jammingValues_neg40dBm[self.__lastJammingNeg40dBmIndex:self.__lastJammingNeg40dBmIndex + size]
            self.__lastJammingNeg40dBmIndex += size
            return jammingValues

        else:
            raise Exception("The jamming type is not valid")

    def getNormalValues(self, size):
        jammingValues = self.__normalValues[self.__lastNormalIndex:self.__lastNormalIndex + size]
        self.__lastNormalIndex += size
        return jammingValues

    def assemble(self, jammingStructure):
        if jammingStructure is None or len(jammingStructure) == 0:
            raise Exception("The jamming structure is empty")

        self.__lastJammingNeg10dBmIndex = 0
        self.__lastJammingNeg40dBmIndex = 0
        self.__lastJamming10dBmIndex = 0
        self.__lastNormalIndex = 0

        jammingValues = []
        groundTruth = [None] * jammingStructure[-1][1]

        for element in jammingStructure:
            if element[2] != Parameters.NORMAL_TRAFFIC:
                jammingValues.extend(self.getJammingValues(element[2], element[1] - element[0]))
                groundTruth[element[0]:element[1]] = [Parameters.OUTLIERS] * (element[1] - element[0])
            else:
                jammingValues.extend(self.getNormalValues(element[1] - element[0]))
                groundTruth[element[0]:element[1]] = [Parameters.INLIERS] * (element[1] - element[0])
        return jammingValues, groundTruth



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