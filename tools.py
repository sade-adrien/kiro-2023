class Turbine():
    def __init__(self, id, substation_id):
        self.id = id
        self.substation_id = substation_id
    
    def __str__(self):
        return f"Turbine {self.id} at substation {self.substation_id}"