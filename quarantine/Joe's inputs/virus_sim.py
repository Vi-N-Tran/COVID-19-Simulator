#virus_test
import math
import random
import matplotlib.pyplot as plt


# infection pool is the amount of virus in the environment
class infection_pool():
    def __init__(self, initial_people, time_constant):
        self.num = float(initial_people)  # how many peole in the initial state
        self.virus_load = 0.0       # initial virus load
        self.time_constant = time_constant  # exponential decay time in days
        
    def add_infection(self, x):   # when groups of people contribute infections.   Coupling 1 for normal groups, could be less higher up the tree heiarchty
        self.virus_load += x

    def get_infection(self):   # when the pool is use to infect a group of people
        return(self.virus_load / self.num)

    def get_total_infection(self):   # total infection load
        return(self.virus_load)

    def progression(self ):           # move forward one day with exponential decay
        self.virus_load = self.virus_load * math.exp(-1.0/self.time_constant)

# called once to set up the infection state.
class infection_group():
    def __init__(self, control):
        self.total_people = 0
        self.exposure_scale = control['exposure_scale']
        self.numdays = 32   # just for now, need to fix
        self.numtypes = control['types']
        self.starting_people = control['pop_per_type'] # number of peopel alive at start each state
        self.pool = 0        # amount of infection in pool
        self.min_age = control['min_age']
        self.max_age = control['max_age']
        self.progression_probability = control['progression_probability']
        self.base_infection = control['base_infection']
        self.infection_types = control['infection_types']
        self.infection_states = control['infection_states']
        self.state = list()
        for n in range( 0, self.numtypes):
            s = dict()                    # s holds all the information for each type of progression.
            s['days'] = [0]*self.numdays  # number of people at each day
            s['days'][0] = self.starting_people  # start with everyone in initial state
            self.total_people += self.starting_people
            age = self.random_age()
            s['age'] = age  #used to set later parameters
            s['infection'] = self.set_infection_rate(age)   # sort of socila interaction ,rate, doesn't use age yet. yes a dictionary of dictionaries, default for now
            s['exposure'] = self.set_exposure(age)
            s['progtype'] = self.set_delay(age)
            s['delay'] = control['infection_progressions'][s['progtype']]  #insane redirecton  - setting how many days to each state
            s['daystate'] = list(['normal']*self.numdays)

            for m in range(0,len(self.infection_states)):       # set what infection state we are in for eachday
                q = self.infection_states[m]
                st = s['delay'][q]   # which state
                if st < 0:
                    continue         # next loop, don't reach this state here
                for d in range(0, self.numdays):
                    if d >= st:
                        s['daystate'][d] = q  # which infection state on that day
            self.state.append(s)


    def random_age(self): # creates a random age person
        return(self.min_age + random.random()*(self.max_age - self.min_age))  # for now just linear function

    def set_delay(self, age):  # selects the type of progression based on age
        r = list()
        luck = random.random()                     # luck number
        for n in range(0, len(self.infection_types)):  # loop over possible infection types.
                # scale as inverse age, just test for now, need real scaling as functino of age
            tmp = 1-self.progression_probability[n]   #distance from units
            tmp2 = tmp * math.pow(age/20,1)
            v = 1-tmp2
            if luck < v:  # just making some sort of range
                tp = self.infection_types[n]
                return(tp)


# distribution of overall infection rate multipliers, goes as random ^2.
    def set_infection_rate(self, age):
        r = random.random()
        x = dict()
        for k, v in self.base_infection.items():
            x[k] = v * 4 * r*r # scale infection rate
        return(x)

   # distributio nof overall exposre multipliers goes as random ^2
    def set_exposure(self, age):
        return(4* math.pow(random.random(),2) * self.exposure_scale)


    def progression(self):                                   # steps time forward
        for n in range (0, self.numtypes):
            s = self.state[n]     # just make notation easier
            r = s['days']
            r[self.numdays-1] += r[self.numdays-2]  # dead stay dead
            for tmp in range(1, self.numdays-2):  #insanely  inefficient will fix later
                d = self.numdays - tmp-1
                r[d] = r[d-1]                # move one day forward
            r[1]= 0                          # until infected
            s['days'] = r

    def total_initial_people(self):
        return(self.total_people)

    def total_ever_infected_people(self):
        tot = 0
        for n in range (0, self.numtypes):
            tot += self.starting_people -  self.state[n]['days'][0]
        return(tot)

    def infect_to_pool(self, P, coupling, mitigation):
        for n in range (0, self.numtypes):
            s = self.state[n]     # just make notation easier
            r = s['days']
            for d in range(0, self.numdays):   # loop over days
                Kx = s['daystate'][d]         #what state are we in
                P.add_infection(s['infection'][Kx] * r[d] *  self.exposure_scale * coupling * mitigation)
        return(P)  # return the updated pool

    def pool_to_infect(self, P, mitigation):
        for n in range (0, self.numtypes):
            s = self.state[n]     # just make notation easier
            r = s['days']
            infects = s['exposure'] * P.get_infection() * r[0] * mitigation  # infect, normalize to density, integer people Total number infected.
            if infects > r[0]:                                      # prevent negative population
                infects = r[0]
            else:
                if infects < 1:    # need to take random chance
                    x = random.random()  #yes many better ways to do this
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
            X[k] = 0                # creats zero item list
        for n in range (0, self.numtypes):
            s = self.state[n]     # just make notation easier
            r = s['days']
            for d in range(0, self.numdays):   # loop over days
                Kx = s['daystate'][d]         #what state are we in
                if Kx in Clist:
                    tot += s['days'][d]
        return(tot)


    def get_demographics(self):  # rearrange data for plotting
        pconvert = {'asymptomatic':0, 'minor':1, 'hosptial':2, 'ICU':3, 'death':4}
        data = dict()
        data['age'] = list()
        data['progression'] = list()
        for n in range (9, self.numtypes):
            data['age'].append(self.state[n]['age'])
            x = self.state[n]['progtype']
            data['progression'].append(pconvert[x])    #horrible way to turn dictionary to nuimbers
        return(data)





    def testing_trigger(self):
        for n in range(0, 10):   # start with 10 infected
            self.state[n]['days'][1] = 1  # start one day in for some peolple
            self.state[n]['days'][0] -=1


class hospital():
    def __init__(self, control):
        self.hospitals = control['hospitals']
        self.noh_death = control['no_hospital_death']
        self.infection_progressions = control['infection_progressions']

    def process(self, G):  # pass an infection group
        hcases= float(G.get_num_in_conditions(['byPerson_try1', 'ICU']))  # how many in byPerson_try1
        total = float(G.total_initial_people())
        if hcases > total * self.hospitals:  # too many peole to fit in hospita,
            ratio = float(hcases) / float(total * self.hospitals)  - 1.0 # multiplies numbers
            for n in range(0, G.numtypes):  # just randomly move over
                if random.random() < ratio:  # move one
                    s = G.state[n]
                    if (random.random() < self.noh_death) or (s['progtype'] == 'death'):    #died
                        s['progtype'] = 'no_h_die'
                    else:                                   #lived
                        s['progtype'] = 'no_h_recover'
                    s['delay'] = self.infection_progressions[s['progtype']]  #insane redirecton  - setting how many days to each state
                    s['daystate'] = list(['normal']*G.numdays)
                    for m in range(0,len(G.infection_states)):       # set what infection state we are in for eachday
                        q = G.infection_states[m]
                        st = s['delay'][q]   # which state
                        if st < 0:
                            continue         # next loop, don't reach this state here
                        for d in range(0, G.numdays):
                            if d >= st:
                                s['daystate'][d] = q  # which infection state on that day
                    G.state[n] = s        # copy back
            return(G)


                        
class mitigation_policy():
    def __init__(self, control):
        self.in_mitigation = False    # not currently mitigating
        self.mitigation_off= control['mitigation_off']
        self.mitigation_on = control['mitigation_on']
        self.mitigation_ratio = control['mitigation_ratio']
        
    def dumb_policy(self, G):   # dumb policy. trigger, if hospitals overload, release if 14 days decrease
        x = G.get_num_in_conditions(['byPerson_try1', 'ICU'])
        t = G.total_initial_people()
        if self.in_mitigation:
            if x/t <  self.mitigation_off:
                self.in_mitigation = False
        else:
            if x/ t > self.mitigation_on:
                self.in_mitigation = True
        if self.in_mitigation == True:
            return(self.mitigation_ratio)       
        else:
            return(1)   # no mitigation 
                
    


        



def run_sim(control):
    print("start")
    Glist = list()      # infection groups
    Plist = list()      # pool list for each grops
    Mlist = list()      # mitigation policies
    Hlist = list()      # byPerson_try1 list

    data = dict()       #will hold output data

    data['infection_states'] = dict()
    for m in  range(0, len(control['infection_states'])): # ugly conversion of list to dictionary
        data['infection_states'][control['infection_states'][m]] = list([0]*control['sim_days'])



    cases = list()      # total sick peolpe
    uninfected = list() # uninfected people
    grandtot = list()
    grandnorm = list()
    cross_infect = list()
    agelist = list()
    proglist = list()
    infection_progressions= dict()

    totpeople = 0;
    for r in range(0, control['num_groups']):
        G = infection_group(control)         # create a group of people to infect
        P = infection_pool(G.total_initial_people(), control['time_constant'])
        M = mitigation_policy(control)
        H = hospital(control)
        Glist.append(G)
        Plist.append(P)
        Mlist.append(M)
        Hlist.append(H)



        cases.append([0]*control['sim_days'])
        uninfected.append([0]*control['sim_days'])
        cross_infect.append(control['max_cross_infect'] * random.random())
        totpeople += G.total_initial_people()
        D = G.get_demographics()


    v = list([0]*5)
    for n in range(0, len(D['age'])):
        tmp = D['progression'][n]
        v[tmp] += 1  # crude histogram
    print(v)


    bigpool =infection_pool(totpeople, 1)  # pool for infection between cities


    Glist[0].testing_trigger()            # starts infection in just one city */

    conditions = ['sick', 'byPerson_try1', 'ICU']   # just this condition fro now.

    for n in range(0,control['sim_days']):
        print("day = ", n)
        cases.append(list())
        for r in range(0, control['num_groups']):
            G = Glist[r]
            P = Plist[r]
            M = Mlist[r]
            H = Hlist[r]
            G.infect_to_pool(P,  coupling = 1, mitigation = M.dumb_policy(G)) # apply simplistic mitigation policy
            G.pool_to_infect(P, mitigation = M.dumb_policy(G))
            G.infect_to_pool(bigpool, cross_infect[r], 1) # no mitigation on large scale
            G.pool_to_infect(bigpool, 1)
            #H.process(G)         # DISABLE FOR NOW - BROKEN
            G.progression()
            P.progression()
            tmp = G.get_num_in_conditions(conditions)
            #print("n = ", n, "r = ", r, "tmp = ", tmp)
            cases[r][n] += tmp
            uninfected[r][n] += G.get_num_in_conditions(['normal'])

            for q in control['infection_states']:
                data['infection_states'][q][n] += G.get_num_in_conditions([q])


        bigpool.progression()          # this is the pool of virus between teh "cities"

    for n in range (0, control['sim_days']):
        grandtot.append(0)
        grandnorm.append(0)
    for r in range(0, control['num_groups']):
        plt.semilogy(cases[r])
        for n in range(0, control['sim_days']):
            grandtot[n] += cases[r][n]
            grandnorm[n] += uninfected[r][n]
    plt.semilogy(grandtot)
    plt.semilogy(grandnorm)
    #print("enter 1 to continue")

    x= input()  # just a delay
    plt.show()
    return(data)

def plot_data(data, control):
    for n in range(0, len(control['infection_states'])):
        v = data['infection_states'][control['infection_states'][n]]
        print(control['infection_states'][n], v[control['sim_days']-1])
        plt.semilogy(v)
    plt.legend(control['infection_states'])
    plt.show()

