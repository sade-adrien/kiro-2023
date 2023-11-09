class substation():
    def __init__(self, id, land_cable_type, substation_type):
        self.id = id
        self.land_cable_type = land_cable_type
        self.substation_type = substation_type
    
    def __str__(self):
        return f"{self.id=}, {self.land_cable_type=}, {self.substation_type=}"

    def __repr__(self):
        return self.__str__()

class substation_substation_cable():
    def __init__(self, substation_id, other_substation_id, cable_type):
        self.substation_id = substation_id
        self.other_substation_id = other_substation_id
        self.cable_type = cable_type

    def __str__(self):
        return f"{self.substation_id=}, {self.other_substation_id=}, {self.cable_type=}"

    def __repr__(self):
        return self.__str__()

class turbine():
    def __init__(self, id, substation_id):
        self.id = id
        self.substation_id = substation_id
    
    def __str__(self):
        return f"{self.id=}, {self.substation_id=}"

    def __repr__(self):
        return self.__str__()