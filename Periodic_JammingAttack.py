import random
from JammingAttack import JammingAttack
from Parameters import Parameters

#these values are to be inteded * 100
MAXIMUM_BURST_DURATION = 5
MINIMUM_BURST_DURATION = 1

#this value is to be intended as the ratio of the burst duration to the total cycle period
MAXIMUM_DUTY_RATE = 0.5
MINIMUM_DUTY_RATE = 0.1

class Periodic_JammingAttack(JammingAttack):
    def __init__(self, size=20000, jammingType = Parameters.JAMMING_10DBM):
        super().__init__(size)
        self.jammingType = jammingType #only one type of jamming signal is considered
        self.burstDuration = self.decideBurstDuration() * 100
        self.dutyRate = self.decideDutyRate()
        self.restDuration = round((self.burstDuration/self.dutyRate)* (1-self.dutyRate))

    def generateJamming(self):
        index = 0
        current_signal = self.selectStart(self.jammingType)

        #print(f"Starting Signal: {start_signal}")
        #print(f"Burst Duration: {burst_duration}")
        #print(f"Duty Rate: {duty_rate}")

        while index < self.size:
            if current_signal == Parameters.NORMAL_TRAFFIC:
                # Calculate end index for the current signal
                end_index = index + self.restDuration
                if end_index > self.size:
                    end_index = self.size

                # Append the current element
                self.buildElement(index, end_index, Parameters.NORMAL_TRAFFIC)

                # Update index for the next element
                index = end_index

                # Swap the signal
                current_signal = 1 - current_signal  # Switch between 0 and 1
            else:
                # Calculate end index for the current signal
                end_index = index + self.burstDuration
                if end_index > self.size:
                    end_index = self.size

                # Append the current element
                self.buildElement(index, end_index, Parameters.JAMMING_10DBM)

                # Update index for the next element
                index = end_index

                # Swap the signal
                current_signal = 1 - current_signal

        return self.constructor.assemble(self.jammingStructure)
