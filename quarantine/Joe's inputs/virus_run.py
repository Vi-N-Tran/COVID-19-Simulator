# #virus_run.py
#
# import virus_sim
# import math
# import random
# import matplotlib.pyplot as plt
#
#
# control = dict()
# control['population'] = 300000000
# control['num_groups'] = 200  # number of different city / metropolitan areas
# control['sim_days']  = 100  # number of days in simulation
# control['types']= 100  # numberof different types of people simulated
# control['pop_per_type'] = round(control['population'] / (control['types'] * control['num_groups']))
#
#
# control['min_age'] = 1
# control['max_age'] = 80   # ages of people
#
#
# control['hospitals'] =  10 # ratio of availble hospitals to initial people. BROKEN DISABLED
#
#
# control['mitigation_on'] = .001  #control['hospitals']/2
# control['mitigation_off'] =  .0001 # control['hospitals'] / 20
# control['mitigation_ratio'] = 1  # reductino in spread during mitigation. now NO MITIGATION
#
#
# control['time_constant'] = 1  # lifeime in days of virus in environment
# control['exposure_scale'] = 0.5 # overall infection rate tuning parameter
# control['max_cross_infect'] = 0.02  # multiplier for infections between cities. (2X air travel for now)
# control['no_hospital_death'] = .10   # 1/4 die if no hospital, othere take longer to heal (see below).
#
# #infection_types = ['asymptomatic', 'minor', 'hosptial', 'ICU', 'death']
# control['progression_probability'] = [.25, 0.85, 0.94, 0.992, 1000, 1000, 1000]   # probabilty of reachign each state, before age correction, never reach lsat state
#
#
# # CAUTION CHANGING THINGS BELOW HERE
#
# # states of infection (This is an insane thicket of redirections, probably created by a drunken madman)
# control['infection_states']  = ['normal', 'exposed', 'infectious', 'sick', 'byPerson_try1', 'ICU', 'recovered', 'dead']
#
# # types of infections - how the disease will progress in a particular person
# control['infection_types'] = ['asymptomatic', 'minor', 'hosptial', 'ICU', 'death',  'no_h_recover', 'no_h_die']
#
# its = control['infection_types']
# ins = control['infection_states']  # simplify notation
# # default rates at which you infect other.   uses infection_states above.
# control['base_infection']  = {ins[0]:0.0, ins[1]:0.0, ins[2]:1.0, ins[3]: 1.0, ins[4]: 0.1, ins[5] : 0.1, ins[6]:0.0, ins[7]: 0.0}
#
#
# # types of progressions in infections - default values.  Ef.  how a "hosptital" case will progress with time
# #  a time of -1 means we never get to that state.
# tmp= dict()
# tmp[its[0]] = {ins[0]:0, ins[1]:1, ins[2]:5, ins[3]: -1, ins[4]: -1, ins[5] : -1, ins[6]:20, ins[7]:-1}
# tmp[its[1]] = {ins[0]:0, ins[1]:1, ins[2]:5, ins[3]: 10, ins[4]: -1, ins[5] : -1, ins[6]:20, ins[7]:-1}
# tmp[its[2]] = {ins[0]:0, ins[1]:1, ins[2]:5, ins[3]: 10, ins[4]: 14, ins[5] : -1, ins[6]:22, ins[7]:-1}
# tmp[its[3]] = {ins[0]:0, ins[1]:1, ins[2]:5, ins[3]: 10, ins[4]: 14, ins[5] : 20, ins[6]:22, ins[7]:-1}
# tmp[its[4]] = {ins[0]:0, ins[1]:1, ins[2]:5, ins[3]: 8, ins[4]: 12, ins[5] : 16, ins[6]: -1, ins[7]:25}
# tmp[its[5]] = {ins[0]:0, ins[1]:1, ins[2]:5, ins[3]: 10, ins[4]: -1, ins[5] : -1, ins[6]:28, ins[7]:-1}
# tmp[its[6]] = {ins[0]:0, ins[1]:1, ins[2]:5, ins[3]: 8, ins[4]: -1, ins[5] : -1, ins[6]: -1, ins[7]:12}
# control['infection_progressions'] = tmp       # copy into overall dictionary
#
#
# #runs the simulation
# data = virus_sim.run_sim(control)
# virus_sim.plot_data(data, control)




