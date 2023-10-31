"""_summary_
    create data structure class 
"""

class OdClass(object):
    def __init__(self):
        self.id = -1
        self.origin = -1
        self.dest = -1
        self.demand = -1
        self.modes = []
        self.logsum = []
    def ini(self,_id,_o,_d,_demand):
        self.id =_id
        self.origin = _o
        self.dest = _d
        self.demand = _demand

class ModeEvoClass(object):
    # this assoicated with each OD pair
    def __init__(self):
        self.id = -1
        self.type = -1
        self.od = -1
        self.flow =[]
        self.utility =[]
        # self.utility = -1
        self.prob = []
        self.flow_ratio = []
        self.paths = []
        self.case_id = -1
        self.day_id = -1
        self.logsum = []
        # self.paths_index = []

    # def set_path_index(self,_paths):
        # for p in _paths:
            # if p.mode==self.type and p.od==self.od:
                # self.paths_index.append(p.id)

class PathClass(object):
    def __init__(self):
        self.id = -1
        self.mode = -1
        self.od = -1
        self.name = []
        self.cost = []
        self.nodes = []
        self.prob = []
        self.flow_ratio = []
        self.flow = []
        self.tt = -1
        self.wt = -1
        self.ct = -1
        self.case_id = -1

class EdgeClass(object):
    def __init__(self):
        self.id = -1
        self.type = -1
        self.head = -1
        self.tail = -1  
        self.flow = []
        self.cost = []
    def ini(self,_id,_type,_cost):
        self.id = _id
        self.type = _type
        self.cost = _cost

class GraphClass(object):
    def __init__(self):
        self.OD = []
        self.edge = []
        self.day = []
    def set_od(self,_od:OdClass):
        for w in range(_od):
            self.OD.append(w)
    def set_edge(self, _edges:EdgeClass):
        for e in range(_edges):
            self.edge.append(e)
