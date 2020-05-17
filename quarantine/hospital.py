import random


class Hospital:
    def __init__(self, dictionary):
        self.hospitals = dictionary['total_hospitals']
        self.no_hospital_death_rate = 0.25  # Arbitrary guess -------------> Need to fix
        self.states_to_type = dictionary["states_to_type"]

    # Need to edit to switch to calculating for states
    def process(self, State):  # pass an infection group
        hcases = float(State.get_num_in_conditions(['byPerson_try1', 'ICU']))  # how many in byPerson_try1
        total = float(State.total_initial_people())
        if hcases > total * self.hospitals:  # too many peole to fit in hospita,
            ratio = float(hcases) / float(total * self.hospitals) - 1.0  # multiplies numbers
            for n in range(0, State.numtypes):  # just randomly move over
                if random.random() < ratio:  # move one
                    s = State.state[n]
                    if (random.random() < self.no_hospital_death_rate) or (s['progtype'] == 'death'):  # died
                        s['progtype'] = 'no_h_die'
                    else:  # lived
                        s['progtype'] = 'no_h_recover'
                    s['delay'] = self.infection_progressions[
                        s['progtype']]  # insane redirecton  - setting how many days to each state
                    s['daystate'] = list(['normal'] * State.numdays)
                    for m in range(0, len(State.infection_states)):  # set what infection state we are in for eachday
                        q = State.infection_states[m]
                        st = s['delay'][q]  # which state
                        if st < 0:
                            continue  # next loop, don't reach this state here
                        for d in range(0, State.numdays):
                            if d >= st:
                                s['daystate'][d] = q  # which infection state on that day
                    State.state[n] = s  # copy back
            return (State)
