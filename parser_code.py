import json
from tools import parser_out
from simple_sol import substations_sol, substation_substation_cables_sol, turbines_sol

def test():
    print("hi")


list_instances = ["small"] # ["toy", "small", "medium", "large", "huge"]
for instance_name in list_instances:
    # read json file
    with open(f"instance_depart/{instance_name}.json") as f:
        data = json.load(f)

    turbines = turbines_sol(data)
    substations = substations_sol(data)
    substation_substation_cables = substation_substation_cables_sol(data)

    parser_out(instance_name, turbines, substations, substation_substation_cables).create_json()
