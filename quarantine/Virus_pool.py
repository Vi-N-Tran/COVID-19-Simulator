import math
import random

class Virus_pool():
    def __init__(self, initial_people, time_constant):
        self.num = float(initial_people)  # how many people in initially -> same for every state for now
        self.virus_num = 0.0  # initial virus num
        self.time_constant = time_constant  # time in days in which virus would go away

    def add_infection(self, x):
        self.virus_num += x

    def get_infection(self):  # when the pool is use to infect a group of people
        return self.virus_num / self.num

    def get_total_infection(self):  # total infection load
        return self.virus_num

    # Joe's equation
    def progression(self):  # move forward one day with exponential decay
        self.virus_num = self.virus_num * math.exp(-1.0 / self.time_constant)
