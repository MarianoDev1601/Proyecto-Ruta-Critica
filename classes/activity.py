class Activity:
    def __init__(self, number:str, description:str, duration:float, predecessors:list=[]):
        self.number:str = number
        self.description:str = description
        self.duration:float = duration
        self.predecessors:list = predecessors
        self.successors:list = []
        self.esd:float = None
        self.efd:float = None
        self.lsd:float = None
        self.lfd:float = None

    def get_holgura(self):
        if (self.esd is not None):
            return self.efd - self.esd
        else:
            return None
    
    def add_predecessor(self, predecessor_number:str):
        self.predecessors.append(predecessor_number)
    
    def add_successor(self, successor_number:str):
        self.successors.append(successor_number)
    
    def remove_predecessor(self, predecessor_number:str):
        self.predecessors.remove(predecessor_number)
    
    def remove_successor(self, successor_number:str):
        self.successors.remove(successor_number)
    
    def update_early_dates(self, esd:float):
        self.esd = esd
        self.efd = esd + self.duration
    
    def update_late_dates(self, lfd:float):
        self.lfd = lfd
        self.lsd = self.lfd - self.duration

    def reset(self):
        self.esd:float = None
        self.efd:float = None
        self.lsd:float = None
        self.lfd:float = None