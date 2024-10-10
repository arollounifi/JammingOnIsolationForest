import random
from Parameters import Parameters
from Constructor import Constructor

#---- THESE ARE PLACEHOLDERS ----
MAXIMUM_BURST_DURATION = 0
MINIMUM_BURST_DURTAION = 0
MAXIMUM_DUTY_RATE = 0
MINIMUM_DUTY_RATE = 0

class JammingAttack:
    def __init__(self, size = 20000):
        self.size = size
        self.jammingStructure = []
        self.constructor = Constructor()

    # TODO -> Update the tests for this method
    #Selects the starting signal
    #jammingTypes: the number of jamming types to select from
    def selectStart(self, jammingTypes = None):
        if jammingTypes is None:
            raise Exception("The jamming type is not valid")

        NormalorJamming = random.randint(0, 1)

        if NormalorJamming == 0:
            return Parameters.NORMAL_TRAFFIC
        else:
            return random.choice(jammingTypes)

    def buildElement(self, startIndex, endIndex, Type):
        self.jammingStructure.append([startIndex, endIndex, Type])

    def decideBurstDuration(self):
        return random.randint(MINIMUM_BURST_DURTAION, MAXIMUM_BURST_DURATION)

    def decideDutyRate(self):
        return random.uniform(MINIMUM_DUTY_RATE, MAXIMUM_DUTY_RATE)

    #Genrates the jamming data and the ground truth
    def generateJamming(self):
        if not self.jammingStructure:
            self.buildElement(0, self.size, Parameters.JAMMING_10DBM)
        return self.constructor.assemble(self.jammingStructure)


