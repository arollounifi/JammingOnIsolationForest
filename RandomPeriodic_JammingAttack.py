from Periodic_JammingAttack import Periodic_JammingAttack
from Parameters import Parameters

class RandomPeriodic_JammingAttack(Periodic_JammingAttack):
    def __init__(self, size = 20000):
        super().__init__(size)

        print("random periodic size:" + str(self.size))

    def generateJamming(self):
        index = 0
        current_signal = self.selectStart(self.jammingType)

        # print(f"Starting Signal: {start_signal}")
        # print(f"Burst Duration: {burst_duration}")
        # print(f"Duty Rate: {duty_rate}")

        while index < self.size:
            if current_signal == Parameters.NORMAL_TRAFFIC:
                # Calculate end index for the current signal
                end_index = index + self.restDuration
                if end_index > self.size:
                    end_index = self.size

                self.buildElement(index, end_index, Parameters.NORMAL_TRAFFIC)

                index = end_index
                current_signal = 1 - current_signal  # Switch between 0 and 1
                self.restDuration = round((self.burstDuration / self.dutyRate) * (1 - self.dutyRate))

            else:
                # Calculate end index for the current signal
                end_index = index + self.burstDuration
                if end_index > self.size:
                    end_index = self.size

                self.buildElement(index, end_index, Parameters.JAMMING_10DBM)

                index = end_index
                current_signal = 1 - current_signal
                self.burstDuration = self.decideBurstDuration() * 100

        return self.constructor.assemble(self.jammingStructure)