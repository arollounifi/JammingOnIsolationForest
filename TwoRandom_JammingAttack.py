import random
from operator import index

from JammingAttack import JammingAttack
from Parameters import Parameters

#these values are to be intednded * 100
MAXIMUM_BURST_DURATION = 5
MINIMUM_BURST_DURTAION = 1

#this value is to be intended as the ratio of the burst duration to the total cycle period
MAXIMUM_DUTY_RATE_1 = 0.5
MINIMUM_DUTY_RATE_1 = 0.1

MAXIMUM_DUTY_RATE_2 = 0.8
MINIMUM_DUTY_RATE_2 = 0.3

class TwoRandom_JammingAttack(JammingAttack):
    def __init__(self, size = 20000, jammingTypes = None):
        super().__init__(size)

        print("two random periodic size:" + str(self.size))

        if jammingTypes is None:
            self.jammingTypes = [Parameters.JAMMING_10DBM, Parameters.JAMMING_NEG10DBM]
        else:
            self.jammingTypes = jammingTypes

        self.burstDurations ={}
        self.dutyRates = {}
        self.restDurations = {}
        self.last_attack_indices = {}

        for attack_type in self.jammingTypes:
            burstDuration = self.decideBurstDuration() * 100
            dutyRate = self.decideDutyRate(attack_type)
            restDuration = round((burstDuration / dutyRate) * (1 - dutyRate))

            self.burstDurations[attack_type] = burstDuration
            self.dutyRates[attack_type] = dutyRate
            self.restDurations[attack_type] = restDuration
            self.last_attack_indices[attack_type] = -restDuration #Allows to attack immediately if so desired

    def decideBurstDuration(self):
        return random.randint(MINIMUM_BURST_DURTAION, MAXIMUM_BURST_DURATION)

    def decideDutyRate(self, Attacker):
        if Attacker == self.jammingTypes[0]:
            return random.uniform(MINIMUM_DUTY_RATE_1, MAXIMUM_DUTY_RATE_1)
        else:
            return random.uniform(MINIMUM_DUTY_RATE_2, MAXIMUM_DUTY_RATE_2)

    #Determines if a jamming attack of a specific type can be inserted at the current index based on the rest duration
    def can_insert_attack(self, attack_type, index):
        last_attack_index = self.last_attack_indices[attack_type]
        rest_duration = self.restDurations[attack_type]
        return index >= last_attack_index + rest_duration

    # Inserts an attack of a given type, updates the index and returns the end index
    def insert_attack(self, attack_type, index):
        burst_duration = self.burstDurations[attack_type]
        attack_end_index = min(index + burst_duration, self.size)
        self.buildElement(index, attack_end_index, attack_type)
        self.last_attack_indices[attack_type] = attack_end_index

        new_burstDuration = self.decideBurstDuration() * 100
        new_dutyRate = self.decideDutyRate(attack_type)
        new_restDuration = round(new_burstDuration * ((1 - new_dutyRate) / new_dutyRate))

        self.restDurations[attack_type] = new_restDuration
        self.burstDurations[attack_type] = new_burstDuration
        self.dutyRates[attack_type] = new_dutyRate

        return attack_end_index

    # Inserts normal traffic from the current index to the end index and returns the end index
    def insert_normal_traffic(self, index, end_index):
        self.buildElement(index, end_index, Parameters.NORMAL_TRAFFIC)
        return end_index

    # Determines wich attacks are available to be inserted at the current index
    def get_next_available_attacks(self, index):
        available_attacks = []
        for attack_type in self.jammingTypes:
            if self.can_insert_attack(attack_type, index):
                available_attacks.append(attack_type)
        return available_attacks

    # Decides which attack to insert nect when multiple attacks are avaialble. The order in the JammingAttacks list is the priority.
    def decide_next_attack(self, available_attacks):
        # Assuming JammingAttacks[0] is the strongest attack available
        for attack_type in self.jammingTypes:
            if attack_type in available_attacks:
                return attack_type
        return None


    def get_next_available_time(self):
        #if all the elements in last_attack_indices are negative, then set the next_times to the rest durations
        if all(last_index < 0 for last_index in self.last_attack_indices.values()):
            return min(self.restDurations.values())
        else:
            next_times = [last_index + rest_duration for last_index, rest_duration in zip(
                self.last_attack_indices.values(), self.restDurations.values())]
        return min(next_times)

    def generateJamming(self):
        index = 0
        self.last_attack_indices = {
            attack_type: -self.restDurations[attack_type] for attack_type in self.jammingTypes}
        first_signal = self.selectStart(self.jammingTypes)

        if first_signal in self.jammingTypes:
            index = self.insert_attack(first_signal, index)
        else:
            next_available_time = self.get_next_available_time()
            end_index = min(next_available_time, self.size)
            index = self.insert_normal_traffic(index, end_index)

        while index < self.size:
            available_attacks = self.get_next_available_attacks(index)
            if available_attacks:
                attack_type = self.decide_next_attack(available_attacks)
                index = self.insert_attack(attack_type, index)
            else:
                next_available_time = self.get_next_available_time()
                end_index = min(next_available_time, self.size)
                index = self.insert_normal_traffic(index, end_index)

        return self.constructor.assemble(self.jammingStructure)