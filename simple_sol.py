from tools import *

def turbines_sol(data):
    turbines_sol = []
    for t in data['wind_turbines']:
        turbines_sol.append(turbine(id=t['id'],
                                    substation_id=1).to_dict())
    return turbines_sol

def substation_substation_cables_sol(data):
    return []

def substations_sol(data):
    return [substation(1, 1, 1).to_dict()]

