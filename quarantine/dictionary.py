# Information from:
# https://www.aha.org/statistics/fast-facts-us-hospitals
# https://worldpopulationreview.com/states/

dictionary = {
    "population": 328200000,
    "states": 50,
    "population_type": ["<1,000,000", "<3,000,000", "<6,000,000", "<10,000,000", "<15,000,000", ">15,000,000"],
    "population_per_acre": ["<10", "<30", "<100", "<1000", "<3000", "<10,000"],

    "population_per_acre_dict":
        {"<1,000,000": "<10", "<3,000,000": "<30","<6,000,000":"<100", "<10,000,000": "<1000", "<15,000,000": "<3000",
         ">15,000,000": "<10,000"},

    "population_by_state":
        {"<1,000,000": ["Wyoming", "North Dakota", "South Dakota", "Delaware", "Vermont", "Alaska"],
         "<3,000,000": ["Montana", "Idaho","New Mexico", "Nebraska", "Kansas", "Mississipi", "West Virginia", "New Hamshire", "Maine", "Rhode Island", "Hawaii"],
         "<6,000,000": ["Oregon", "Nevada", "Utah", "Colorado", "Oklahoma","Arkansas","Louisiana", "Iowa", "Minesota", "Wisconson", "Kentucky", "Alabama","South Carolina", "Connecticut"],
         "<10,000,000": ["Washington", "Arizona", "Missori", "Tennesee", "Indiana", "Virgina", "Maryland", "New Jersey", "Massachusettes"],
         "<15,000,000": ["Illinois", "Michigan", "Ohio", "Georgia", "North Carolina", "Pennsylvania"],
         ">15,000,000": ["New York", "California", "Texas", "Florida"]},

    "min_age": 1,
    "max_age": 90,
    "total_hospitals": 6146,
    "total_beds": 924107,
    "time_constant": 1, # number of days of virus life span
    "exposure_scale": 0.5, # percent of people in which one person can infect

    "infection_types_rates": # Rate at which the type can infect others
        {'asymptomatic': 1, 'minor':0.5, 'hosptial':0.1, 'ICU':0.05, 'death':0,  'no_hospital_recover':0.5, 'no_hospital_die': 0},

    "infection_types": #Types of infection
            ['asymptomatic', 'minor', 'hosptial', 'ICU', 'death',  'no_hospital_recover', 'no_hospital_die'],

    "infection_states": # Rate at which the state can infect others
        {'normal':0, 'exposed':0.5, 'infectious':1, 'sick':1, 'byPerson_try1':0.1, 'ICU':0.05, 'recovered':0, 'dead':0},

    "states_to_type":
        {
            "normal": {'asymptomatic': -1, 'minor':-1, 'hosptial':-1, 'ICU':-1, 'death':-1,  'no_hospital_recover':-1, 'no_hospital_die': -1 },
            "exposed": {'asymptomatic': 5, 'minor':5, 'hosptial':-1, 'ICU':-1, 'death':-1,  'no_hospital_recover':-1, 'no_hospital_die': -1 },
            "infectious": {'asymptomatic': 5, 'minor':5, 'hosptial':-1, 'ICU':-1, 'death':-1,  'no_hospital_recover':-1, 'no_hospital_die': -1 },
            "sick": {'asymptomatic': -1, 'minor':5, 'byPerson_try1': 5, 'ICU':5, 'death':-1,  'no_hospital_recover':5, 'no_hospital_die': 5 },
            "byPerson_try1": {'asymptomatic': -1, 'minor':-1, 'hosptial':10, 'ICU':5, 'death':5,  'no_hospital_recover':-1, 'no_hospital_die': 10 },
            "ICU": {'asymptomatic': -1, 'minor':-1, 'hosptial':-1, 'ICU':10, 'death':5,  'no_hospital_recover':-1, 'no_hospital_die': 10 },
            "recovered": {'asymptomatic': 5, 'minor':5, 'hosptial':-1, 'ICU':-1, 'death':-1,  'no_hospital_recover':10, 'no_hospital_die': -1 },
            "dead": {'asymptomatic': -1, 'minor':-1, 'hosptial':-1, 'ICU':-1, 'death':10,  'no_hospital_recover':-1, 'no_hospital_die': 10 },
        },
}


