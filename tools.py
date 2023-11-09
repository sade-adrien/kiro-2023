import json
import numpy as np

class substation():
    def __init__(self, id, land_cable_type, substation_type):
        self.id = id
        self.land_cable_type = land_cable_type
        self.substation_type = substation_type
    
    def __str__(self):
        return f"{self.id=}, {self.land_cable_type=}, {self.substation_type=}"

    def __repr__(self):
        return self.__str__()
    
    def to_dict(self):
        return {'id': self.id, "land_cable_type": self.land_cable_type, "substation_type": self.substation_type}

class substation_substation_cable():
    def __init__(self, substation_id, other_substation_id, cable_type):
        self.substation_id = substation_id
        self.other_substation_id = other_substation_id
        self.cable_type = cable_type

    def __str__(self):
        return f"{self.substation_id=}, {self.other_substation_id=}, {self.cable_type=}"

    def __repr__(self):
        return self.__str__()
    
    def to_dict(self):
        return {"substation_id": self.substation_id, "other_substation_id": self.other_substation_id, "cable_type": self.cable_type}

class turbine():
    def __init__(self, id, substation_id):
        self.id = id
        self.substation_id = substation_id
    
    def __str__(self):
        return f"{self.id=}, {self.substation_id=}"

    def __repr__(self):
        return self.__str__()
    
    def to_dict(self):
        return {'id': self.id, 'substation_id': self.substation_id}

class parser_out():
    def __init__(self, instance_name, substations, substation_substation_cables, turbines):
        self.instance_name = instance_name
        self.folder_out = "instance_arrive/"
        self.substations = substations
        self.substation_substation_cables = substation_substation_cables
        self.turbines = turbines
    
    def create_json(self):
        dict_out = {
            "substations": self.substations,
            "substation_substation_cables": self.substation_substation_cables,
            "turbines": self.turbines
            }

        with open(f"{self.folder_out}/{self.instance_name}_out.json", "w+") as f:
            json.dump(dict_out, f)


def distance(substation1, substation2):
    #distance squared
    return (substation2['x'] - substation1['x'])**2 + (substation2['y'] - substation1['y'])**2

def get_substation(id, substation_list):
    for substation in substation_list:
        if substation['id'] == id:
            return substation
    raise ValueError(f"substation {id} not found")


def find_number_of_substations(data):
    substation_type_id = 2
    list_substations_type = data["substation_types"]
    substation_type = get_substation(substation_type_id, list_substations_type)
    
    total_power_max = get_power_w(data)

    return int(np.ceil(total_power_max / substation_type["rating"]))

def get_power_w(data):
    n_turbines = len(data['wind_turbines'])
    unit_power = 0
    for scenario in data['wind_scenarios']:
        unit_power = max(unit_power, scenario['power_generation'])
    
    return n_turbines * unit_power