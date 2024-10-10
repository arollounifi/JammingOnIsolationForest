import random
from Parameters import Parameters
from Constructor import Constructor


class JammingAttack:
    def __init__(self, size = 20000):
        self.size = size
        self.jammingStructure = []
        self.constructor = Constructor()

    #Selects the starting signal
    #jammingTypes: the number of jamming types to select from
    def selectStart(self, jammingTypes: int):
        if jammingTypes <1 or jammingTypes > 3:
            raise Exception("The jamming type is not valid")

        NormalorJamming = random.randint(0, 1)

        if NormalorJamming == 0:
            return Parameters.NORMAL_TRAFFIC
        else:
            return random.randint(1, jammingTypes)

    def buildElement(self, startIndex, endIndex, Type):
        self.jammingStructure.append([startIndex, endIndex, Type])

    #Genrates the jamming data and the ground truth
    def generateJamming(self):
        if not self.jammingStructure:
            self.buildElement(0, self.size, Parameters.JAMMING_10DBM)
        return self.constructor.assemble(self.jammingStructure)


