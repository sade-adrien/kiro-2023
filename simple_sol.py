from tools import *

def turbines_sol(data):
    turbines_sol = []
    for t in data['wind_turbines']:
        turbines_sol.append(turbine(id=t['id'],
                                    substation_id=1).to_dict())
    return turbines_sol

def substation_substation_cables_sol():
    return []

def substations_sol():
    return []

