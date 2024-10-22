import random
from signal import signal

import numpy as np

from Periodic_JammingAttack import Periodic_JammingAttack
from Parameters import Parameters

#these values are to be inteded * 100
MAXIMUM_BURST_DURATION = 5
MINIMUM_BURST_DURATION = 1

#this value is to be intended as the ratio of the burst duration to the total cycle period
MAXIMUM_DUTY_RATE = 0.8
MINIMUM_DUTY_RATE = 0.3

class DistancePeriodic_JammingAttack(Periodic_JammingAttack):
    def __init__(self, size=20000):
        super().__init__(size)

        print("Distance periodic size:" + str(self.size))

        self.burstDuration = self.decideBurstDuration() * 100
        self.dutyRate = self.decideDutyRate()
        self.restDuration = round((self.burstDuration/self.dutyRate)* (1-self.dutyRate))

    def apply_fspl_to_jamming(self, signal_list, jamming_flags):
        """
        Applies the Free-Space Path Loss (FSPL) model to simulate the jammer moving away from the receiver.

        Parameters:
        - signal_list (list or array-like): The signal values.
        - jamming_flags (list or array-like): A boolean list where True indicates a jamming signal.
        - frequency (float): Frequency in Hz (e.g., 2.412 GHz -> 2.412e9 Hz).
        - initial_distance (float): The initial distance from the jammer to the receiver in meters.
        - distance_increment (float): The increment by which the distance increases at each step.

        Source: https://inet.omnetpp.org/docs/showcases/wireless/pathloss/doc/index.html
        """
        c = 3e8  # Speed of light in meters per second
        num_steps = len(signal_list)
        frequency  = 5.805e9
        initial_distance = 0.0002
        distance_increment = 0.00001

        print(type(signal_list))
        # Initialize the modified signal list as a copy of the original
        modified_signal_list = np.array(signal_list, copy=True)
        print(type(modified_signal_list))

        # Generate distances for the jamming signals
        distances = np.array([initial_distance + i * distance_increment for i in range(num_steps)])
        print(distances)

        # Calculate FSPL for the distances
        fspl = 20 * np.log10(distances) + 20 * np.log10(frequency) + 20 * np.log10(4 * np.pi / c)
        print(fspl)

        # Apply FSPL only to jamming signals
        for i in range(num_steps):
            if jamming_flags[i] == Parameters.OUTLIERS:  # Apply FSPL only if it's a jamming signal
                signal_list[i] -= fspl[i]

        return signal_list

    def generateJamming(self):
        jammingValues, groundTruth = super().generateJamming()
        jammingValues = self.apply_fspl_to_jamming(jammingValues, groundTruth)
        return jammingValues, groundTruth