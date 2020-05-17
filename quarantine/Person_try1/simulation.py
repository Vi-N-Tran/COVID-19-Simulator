#******** definitions ********#
# IT = interaction rate

#******** assumptions ********#
# interact with 5 new people every day
# average person is 40 year old
# 10 days after getting sick is healthy again  -----------------> need to fact check

from Person import *

# Number of days want to test since virus first introduced
DAYS_TEST = 26

# variables
healthy_num = 327200000
sick_num = 1
day = 1

sick_list = [Person()]

# count up the days want to test
for day in range(1, DAYS_TEST):
    # Make new batch of people infected and add them to sick list. Take person out of sick list when they get better
    for person in sick_list:

        person.increment_day()

        if person.get_infectious():
            # infected person is healthy again
            if person.get_sick() and person.get_day_infected() >= 24:
                # print("removed one person")
                sick_list.remove(person)
                healthy_num += 1
                sick_num -= 1
            # Person is infecting others
            else:
                for num in range(person.get_infected_rate()):
                    sick_list.append(Person())
                    healthy_num -= 1
                    sick_num += 1

    print("sick_num on day " + str(day) + ": " + str(sick_num))





