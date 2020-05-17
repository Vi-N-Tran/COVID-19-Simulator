from dictionary import *
state_count = 0
for key in dictionary.get("population_by_state").keys():
    print(key)
    for a in dictionary.get("population_by_state").get(key):
        state_count += 1

print(state_count)
