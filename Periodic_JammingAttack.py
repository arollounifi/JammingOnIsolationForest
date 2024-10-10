import random
from copyreg import constructor
from distutils.command.build import build
from operator import index

from JammingAttack import JammingAttack
from Parameters import Parameters

#these values are to be inteded * 100
MAXIMUM_BURST_DURATION = 5
MINIMUM_BURST_DURATION = 1

#this value is to be intended as the ratio of the burst duration to the total cycle period
MAXIMUM_DUTY_RATE = 0.5
MINIMUM_DUTY_RATE = 0.1

class Periodic_JammingAttack(JammingAttack):
    def __init__(self, size=20000):
        super().__init__(size)
        self.jammingTypes = 1 #only one type of jamming signal is considered
        self.burstDuration = self.decideBurstDuration() * 100
        self.dutyRate = self.decideDutyRate()
        self.restDuration = round((self.burstDuration/self.dutyRate)* (1-self.dutyRate))


    def decideBurstDuration(self):
        return random.randint(MINIMUM_BURST_DURATION, MAXIMUM_BURST_DURATION)

    def decideDutyRate(self):
        return random.uniform(MINIMUM_DUTY_RATE, MAXIMUM_DUTY_RATE)

    def generateJamming(self):
        index = 0
        current_signal = self.selectStart(self.jammingTypes)

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
