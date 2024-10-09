import random
from Parameters import Parameters
from Constructor import Constructor


class JammingAttack:
    def __init__(self, size = 20000):
        self.size = size
        self.jammingStructure = []

    #Selects the starting signal
    def selectStart(self):
        return random.randint(1, 3)

    def buildElement(self, startIndex, endIndex, Type):
        self.jammingStructure.append([startIndex, endIndex, Type])

    #Genrates the jamming data and the ground truth
    def generateJamming(self):
        if not self.jammingStructure:
            self.buildElement(0, self.size, Parameters.JAMMING_10DBM)
        contructor = Constructor()
        return contructor.assemble(self.jammingStructure)


