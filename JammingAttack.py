import random
from Parameters import Parameters
from Constructor import Constructor


class JammingAttack:
    def __init__(self, base_reading, size = 20000):
        self.base_reading = base_reading
        self.size = size
        self.jammingStructure = []

    #Selects the starting signal
    def selectStart(self):
        return random.randint(1, 3)

    def buildElement(self, startIndex, endIndex, Type):
        self.jammingStructure.append([startIndex, endIndex, Type])

    #Genrates the jamming data and the ground truth
    def generateJamming(self):
        self.jammingStructure[:self.size] = Parameters.JAMMING_10DBM
        return Constructor.assemble(self.jammingStructure)