import random

from dictionary import *

class State():
    # calculate infection by state
    # What should infection group have?
    # total people, number of days to simulate, state of sickness, type of people, pop in each state, pop per capita
    def __init__(self, dictionary, days_to_simulate):
        # FACTS for states
        self.total_people = dictionary.get("population")
        self.states = dictionary.get("states")
        self.population_by_state = dictionary.get("population_by_state")
        self.total_hospitals = dictionary.get("total_hospitals")
        self.total_beds = dictionary.get("total_beds")

        # Vars set to test
        self.min_age = dictionary.get("min_age")
        self.max_age = dictionary.get("max_age")
        self.exposure_scale = dictionary.get("exposure_scale")
        self.time_constant = dictionary.get("time_constant")
        self.num_types = len(dictionary.get("infection_types"))

        # COVID lists
        self.infection_types = dictionary.get("infection_types")
        self.infection_states = dictionary.get("infection states")
        self.states_to_stype = dictionary.get("states_to_type")
        self.infection_types_rates = dictionary.get("infection_types_rates")

        self.days_to_simulate = days_to_simulate

## Still need work  - Joe's idea
        for n in range(0, self.num_types):
            s = dict()  # s holds all the information for each type of progression.
            s['days_to_simulate'] = [0] * self.days_to_simulate  # number of people at each day
            s['days'][0] = self.starting_people  # start with everyone in initial state
            self.total_people += self.starting_people
            age = self.random_age()
            s['age'] = age  # used to set later parameters
            s['infection'] = self.set_infection_rate(
                age)  # sort of socila interaction ,rate, doesn't use age yet. yes a dictionary of dictionaries, default for now
            s['exposure'] = self.set_exposure(age)
            s['progtype'] = self.set_delay(age)
            s['delay'] = control['infection_progressions'][
                s['progtype']]  # insane redirecton  - setting how many days to each state
            s['daystate'] = list(['normal'] * self.numdays)

            for m in range(0, len(self.infection_states)):  # set what infection state we are in for eachday
                q = self.infection_states[m]
                st = s['delay'][q]  # which state
                if st < 0:
                    continue  # next loop, don't reach this state here
                for d in range(0, self.numdays):
                    if d >= st:
                        s['daystate'][d] = q  # which infection state on that day
            self.state.append(s)


# Joe's part
# Need to be switch over to analyzing states instead of people - Vi
    def progression(self):  # steps time forward
        for n in range(0, self.num_types):
            s = self.state[n]  # just make notation easier
            r = s['days']
            r[self.days_to_simulate - 1] += r[self.days_to_simulate - 2]  # dead stay dead
            for tmp in range(1, self.days_to_simulate - 2):  # insanely  inefficient will fix later
                d = self.days_to_simulate - tmp - 1
                r[d] = r[d - 1]  # move one day forward
            r[1] = 0  # until infected
            s['days'] = r

    def total_ever_infected_people(self):
        total = 0
        for n in range(0, self.num_types):
            total += self.starting_people - self.state[n]['days'][0]
        return (total)

    def infect_to_pool(self, P, coupling, mitigation):
        for n in range(0, self.num_types):
            s = self.state[n]  # just make notation easier
            r = s['days']
            for d in range(0, self.days_to_simulate):  # loop over days
                Kx = s['daystate'][d]  # what state are we in
                P.add_infection(s['infection'][Kx] * r[d] * self.exposure_scale * coupling * mitigation)
        return (P)  # return the updated pool

    def pool_to_infect(self, P, mitigation):
        for n in range(0, self.num_types):
            s = self.state[n]  # just make notation easier
            r = s['days']
            infects = s['exposure'] * P.get_infection() * r[
                0] * mitigation  # infect, normalize to density, integer people Total number infected.
            if infects > r[0]:  # prevent negative population
                infects = r[0]
            else:
                if infects < 1:  # need to take random chance
                    x = random.random()  # yes many better ways to do this
                    if infects > x:
                        infects = 1
                    else:
                        infects = 0
                else:
                    infects = round(infects)  # only integer peole infected.
            r[0] -= infects
            r[1] += infects

    # Clinst is a list of conditions to be summed
    def get_num_in_conditions(self, Clist):
        X = dict()
        tot = 0
        for k in self.infection_states:
            X[k] = 0  # creats zero item list
        for n in range(0, self.num_types):
            s = self.state[n]  # just make notation easier
            r = s['days']
            for d in range(0, self.days_to_simulate):  # loop over days
                Kx = s['daystate'][d]  # what state are we in
                if Kx in Clist:
                    tot += s['days'][d]
        return (tot)

    def get_demographics(self):  # rearrange data for plotting
        pconvert = {'asymptomatic': 0, 'minor': 1, 'hosptial': 2, 'ICU': 3, 'death': 4}
        data = dict()
        data['age'] = list()
        data['progression'] = list()
        for n in range(9, self.num_types):
            data['age'].append(self.state[n]['age'])
            x = self.state[n]['progtype']
            data['progression'].append(pconvert[x])  # horrible way to turn dictionary to nuimbers
        return (data)

    def testing_trigger(self):
        for n in range(0, 10):  # start with 10 infected
            self.state[n]['days'][1] = 1  # start one day in for some peolple
            self.state[n]['days'][0] -= 1