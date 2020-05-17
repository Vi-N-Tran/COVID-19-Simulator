from dictionary import *
import random


class Person:
    def __init__(self):
        self.min_age = dictionary.get("min_age")
        self.max_age = dictionary.get("max_age")
        self.exposure_scale = dictionary.get("exposure_scale")
        self.time_constant = dictionary.get("time_constant")

        # COVID lists
        self.infection_types = dictionary.get("infection_types")
        self.infection_states = dictionary.get("infection states")
        self.states_to_stype = dictionary.get("states_to_type")
        self.infection_types_rates = dictionary.get("infection_types_rates")

    def random_age(self):  # creates a random age person
        return self.min_age + random.random() * (self.max_age - self.min_age)

    def set_type(self, age):  # selects the type of progression based on  -> Be careful to match type with state later
        luck = random.random()  # luck number
        hospital_access = random.randint(0, 1)
        if hospital_access == 0:
            if luck > 0.5:
                infection_type = "no_hospital_recover"
            else:
                infection_type = "no_hospital_die"
        elif hospital_access == 1:
            # There are 5 types while having hospital
            n_type = luck * len(self.infection_types)
            infection_type = self.infection_types[n_type]

        return infection_type

    # Rate at which one person can infect others
    def set_infection_rate(self,type):
        return self.infection_types_rates.get(type)

### NEED MORE WORK
    # rate at which this person get sick/recover
    def increment_progress(self, age):
        # Arbitrary
        if age >= 60:
            return 1
        if 30 < age < 60:
            return 2
        if age < 30:
            return 3
