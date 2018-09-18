class State:
    def __init__(self,id,full_name,short_name,state_value):
        self.primary_key = id
        self.full_name = full_name
        self.short_name = short_name
        self.state_value = state_value

    def print_properties(self):
        print("\t ------> Primary Key %s"%(self.primary_key))
        print("\t Full Name :%s"%(self.full_name))
        print("\t Short Name :%s"%(self.short_name))
        print("\t State Value :%s"%(self.state_value))