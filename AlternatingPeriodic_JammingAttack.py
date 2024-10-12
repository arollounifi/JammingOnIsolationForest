import random
from JammingAttack import JammingAttack
from Parameters import Parameters
from Periodic_JammingAttack import Periodic_JammingAttack

#these values are to be inteded * 100
MAXIMUM_BURST_DURATION = 5
MINIMUM_BURST_DURATION = 1

#this value is to be intended as the ratio of the burst duration to the total cycle period
MAXIMUM_DUTY_RATE = 0.5
MINIMUM_DUTY_RATE = 0.1

class AlternatingPeriodic_JammingAttack(Periodic_JammingAttack):
    def __init__(self, size=20000, jammingTypes = None):
        super().__init__(size)
        if jammingTypes is None:
            self.jammingType = [Parameters.JAMMING_10DBM, Parameters.JAMMING_NEG10DBM]
        else:
            self.jammingType = jammingTypes
        self.burstDuration = self.decideBurstDuration() * 100
        self.dutyRate = self.decideDutyRate()

        # While one attacks the other rests.
        # Therefore, the rest duration one is the same as the burst duration of the other
        self.restDuration = round((self.burstDuration/self.dutyRate)* (1-self.dutyRate))

    def generateJamming(self):
        index = 0

        # In this case we manually select the starting signal to be normal traffic to show the RSSI difference between the two jamming signals
        current_signal = Parameters.NORMAL_TRAFFIC

        #print(f"Starting Signal: {start_signal}")
        #print(f"Burst Duration: {burst_duration}")
        #print(f"Duty Rate: {duty_rate}")

        end_index = self.restDuration
        self.buildElement(index, end_index, Parameters.NORMAL_TRAFFIC)
        index = end_index

        current_signal = random.choice(self.jammingType)

        while index < self.size:
            if current_signal == Parameters.JAMMING_NEG10DBM:
                # Calculate end index for the current signal
                end_index = index + self.restDuration
                if end_index > self.size:
                    end_index = self.size

                self.buildElement(index, end_index, self.jammingType[1])
                index = end_index
                current_signal = Parameters.JAMMING_10DBM  # Switch between the 2 jamming types
            else:
                # Calculate end index for the current signal
                end_index = index + self.burstDuration
                if end_index > self.size:
                    end_index = self.size

                self.buildElement(index, end_index, self.jammingType[0])
                index = end_index
                current_signal = Parameters.JAMMING_NEG10DBM

        return self.constructor.assemble(self.jammingStructure)
