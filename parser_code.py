from tools import parser_out
from simple_sol import substations_sol, substation_substation_cables_sol, turbines_sol

def test():
    print("hi")

def __main__():
    list_instances = ["small"] # ["toy", "small", "medium", "large", "huge"]
    for instance_name in list_instances:
        turbines = turbines_sol()
        substations = substations_sol()
        substation_substation_cables = substation_substation_cables_sol()

        parser_out(instance_name, turbines, substations, substation_substation_cables).create_json()
