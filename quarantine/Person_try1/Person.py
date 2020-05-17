from traceback import *


class Person:
    INFECTED_DAYS = 7
    SICK_DAYS = 14
    day_infected = 0
    infectious = False
    sick = False

    def __init__(self, age=40): # Age is set at 40 as default because it is median age in U.S.
        self.age = age
        self.infected_rate = 0

    def increment_day(self):

        # Increment day
        self.day_infected += 1

        # Update amount of people to infect
        if self.day_infected == 7:
            if 0 < self.age < 5:
                self.infected_rate = 12
            elif 5 <= self.age < 15:
                self.infected_rate = 14
            elif 15 <= self.age < 55:
                self.infected_rate = 23
            elif 55 <= self.age < 65:
                self.infected_rate = 17
            elif self.age >= 65:
                self.infected_rate = 14

        elif self.day_infected >= 8:
            self.infected_rate = 5

        # Keep track of person's state (infectious or sick or both)
        if 7 <= self.day_infected < 14:
            self.infectious = True
        if 14 >= self.day_infected:
            self.sick = True

    # Getter methods
    def get_sick(self):
        return self.sick

    def get_infectious(self):
        return self.infectious

    def get_infected_rate(self):
        return self.infected_rate

    def get_day_infected(self):
        return self.day_infected










