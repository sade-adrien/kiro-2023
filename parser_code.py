import json
from tools import parser_out
from second_sol import substations_sol, substation_substation_cables_sol, turbines_sol, turbines_cluster

def test():
    print("hi")


list_instances = ["small"] # ["toy", "small", "medium", "large", "huge"]
for instance_name in list_instances:
    # read json file
    with open(f"instance_depart/{instance_name}.json") as f:
        data = json.load(f)
    
    turbines_clus = turbines_cluster(data, 3)

    substations = substations_sol(data, turbines_clus)
    turbines = turbines_sol(data, substations, turbines_clus[1])
    
    substation_substation_cables = substation_substation_cables_sol(data)

    parser_out(
        instance_name = instance_name,
        turbines = turbines,
        substations = substations,
        substation_substation_cables=substation_substation_cables).create_json()
