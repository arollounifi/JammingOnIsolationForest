import random
from operator import index

from JammingAttack import JammingAttack
from Parameters import Parameters#these values are to be intednded * 100

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
        if jammingTypes is None:
            self.jammingTypes = [Parameters.JAMMING_10DBM, Parameters.JAMMING_NEG10DBM]
        self.jammingTypes = jammingTypes
        self.burstDuration = self.decideBurstDuration() * 100
        self.dutyRate1 = self.decideDutyRate(jammingTypes[0])
        self.dutyRate2 = self.decideDutyRate(jammingTypes[1])
        self.restDuration1 = round((self.burstDuration/self.dutyRate1)* (1-self.dutyRate1))
        self.restDuration2 = round((self.burstDuration/self.dutyRate2)* (1-self.dutyRate2))

    def decideDutyRate(self, Attacker ):
        if Attacker == self.jammingTypes[0]:
            return random.uniform(MINIMUM_DUTY_RATE_1, MAXIMUM_DUTY_RATE_1)
        else:
            return random.uniform(MINIMUM_DUTY_RATE_2, MAXIMUM_DUTY_RATE_2)

    # TODO -> update the attack duration after each attack
    def generateJamming(self):
        index = 0
        lastAttackIndex1 = 0
        lastAttackIndex2 = 0
        first_signal = self.selectStart(self.jammingTypes)

        # print(f"Starting Signal: {start_signal}")
        # print(f"Burst Duration: {burst_duration}")
        # print(f"Duty Rate: {duty_rate}")

        #creation of the first block
        if first_signal == Parameters.NORMAL_TRAFFIC:
            # Calculate end index for the current signal
            end_index = index + random.choice([self.restDuration1, self.restDuration2])
            self.buildElement(index, end_index, Parameters.NORMAL_TRAFFIC)
            index = end_index

        elif first_signal == self.jammingTypes[0]:
            end_index = index + self.burstDuration
            self.buildElement(index, end_index, Parameters.JAMMING_10DBM)
            index, lastAttackIndex1 = end_index

        else:
            end_index = index + self.burstDuration
            self.buildElement(index, end_index, Parameters.JAMMING_NEG10DBM)
            index, lastAttackIndex2 = end_index

        last_signal = first_signal

        #Geneartion of the rest of the blocks
        while index < self.size:
            '''
            Se l'ultimo segnale è traffico normale, 
                si controlla se è possibile inserire un attacco di tipo 1 o 2
                    se è possibile si inserisce l'attacco di tipo 1 o 2
                altrimenti si inserisce traffico normale
            '''
            if last_signal == Parameters.NORMAL_TRAFFIC:
                # Controllo se è possibile inserire un attacco di tipo 1
                if index > lastAttackIndex1 + self.restDuration1 and index < lastAttackIndex2 + self.restDuration2:
                    if index + self.burstDuration > self.size:
                        end_index = self.size
                    else:
                        end_index = index + self.burstDuration
                    self.buildElement(index, end_index, self.jammingTypes[1])
                    last_signal = self.jammingTypes[1]
                    index, lastAttackIndex2 = end_index

                # Controllo se è possibile inserire un attacco di tipo 2
                elif index < lastAttackIndex1 + self.restDuration1 and index > lastAttackIndex2 + self.restDuration2:
                    if index + self.burstDuration > self.size:
                        end_index = self.size
                    else:
                        end_index = index + self.burstDuration
                    self.buildElement(index, end_index, self.jammingTypes[0])
                    last_signal = self.jammingTypes[0]
                    index, lastAttackIndex1 = end_index

                # Non è possibile inserire nessun attacco quindi si inserisce traffico normale fino alla disponibilità di un attacco
                elif index > lastAttackIndex1 + self.restDuration1 and index > lastAttackIndex2 + self.restDuration2:
                    diff1 = index - lastAttackIndex1 + self.restDuration1
                    diff2 = index - lastAttackIndex2 + self.restDuration2
                    if index + min(diff1, diff2) > self.size:
                        end_index = self.size
                    else:
                        end_index = index + min(diff1, diff2)
                    self.buildElement(index, end_index, Parameters.NORMAL_TRAFFIC)
                    last_signal = Parameters.NORMAL_TRAFFIC
                    index = end_index

                else:
                    # If both are available, the first strongest one is selected
                    if index + self.burstDuration > self.size:
                        end_index = self.size
                    else:
                        end_index = index + self.burstDuration
                    self.buildElement(index, end_index, self.jammingTypes[0])
                    last_signal = self.jammingTypes[0]
                    index, lastAttackIndex1 = end_index

            # Se l'ultimo segnale è di tipo 1
            #   si controlla se è possibile inserire un attacco di tipo 2
            #       se è possibile si inserisce l'attacco di tipo 2
            #   altrimenti si inserisce traffico normale
            #   Se nel mentre è possibile inserire un attacco di tipo 1, si inserisce l'attacco di tipo 1
            elif last_signal == self.jammingTypes[0]:
                if index < lastAttackIndex2 + self.restDuration2:
                    if index + self.burstDuration > self.size:
                        end_index = self.size
                    else:
                        end_index = index + self.burstDuration
                    self.buildElement(index, end_index, self.jammingTypes[1])
                    last_signal = self.jammingTypes[1]
                    index, lastAttackIndex2 = end_index
                else:
                    diff = index - lastAttackIndex2 + self.restDuration2
                    if index + diff < lastAttackIndex1 + self.restDuration1:
                        if index + self.burstDuration > self.size:
                            end_index = self.size
                        else:
                            end_index = index + self.burstDuration
                        self.buildElement(index, end_index, self.jammingTypes[0])
                        last_signal = self.jammingTypes[0]
                        index, lastAttackIndex1 = end_index
                    else:
                        if index + diff > self.size:
                            end_index = self.size
                        else:
                            end_index = index + diff
                        self.buildElement(index, end_index, Parameters.NORMAL_TRAFFIC)
                        last_signal = Parameters.NORMAL_TRAFFIC
                        index = end_index

            # Se l'ultimo segnale è di tipo 2
            #   si controlla se è possibile inserire un attacco di tipo 1
            #       se è possibile si inserisce l'attacco di tipo 1
            #   altrimenti si inserisce traffico normale
            #   Se nel mentre è possibile inserire un attacco di tipo 2, si inserisce l'attacco di tipo 2
            else:
                if index < lastAttackIndex1 + self.restDuration1:
                    if index + self.burstDuration > self.size:
                        end_index = self.size
                    else:
                        end_index = index + self.burstDuration
                    self.buildElement(index, end_index, self.jammingTypes[0])
                    last_signal = self.jammingTypes[0]
                    index, lastAttackIndex1 = end_index
                else:
                    diff = index - lastAttackIndex1 + self.restDuration1
                    if index + diff < lastAttackIndex2 + self.restDuration2:
                        if index + self.burstDuration > self.size:
                            end_index = self.size
                        else:
                            end_index = index + self.burstDuration
                        self.buildElement(index, end_index, self.jammingTypes[1])
                        last_signal = self.jammingTypes[1]
                        index, lastAttackIndex2 = end_index
                    else:
                        if index + diff > self.size:
                            end_index = self.size
                        else:
                            end_index = index + diff
                        self.buildElement(index, end_index, Parameters.NORMAL_TRAFFIC)
                        last_signal = Parameters.NORMAL_TRAFFIC
                        index = end_index




