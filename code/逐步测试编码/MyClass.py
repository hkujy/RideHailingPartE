"""_summary_
    create data structure class 
"""
class NodeClass(object):
    """
        node class
    """
    def __init__(self):
        self.id = -1
        self.name = "undefined"
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
class ModeClass(object):
    # this assoicated with each OD pair
    def __init__(self):
        self.id = -1
        self.name = "undefined"
        self.type = -1
        self.od = -1
        self.flow =[]
        self.prob = []
        self.flow_ratio = []
        self.paths = []
        self.logsum_utility= []

class PathClass(object):
    def __init__(self):
        self.id = -1
        self.mode = -1
        self.conected_Od = -1
        self.cost = []
        self.nodes = []
        self.prob = []
        self.flow = []
        self.tt = -1
        self.wt = -1
        self.ct = -1
class EdgeClass(object):
    def __init__(self):
        self.id = -1
        self.type = "undefined"
        self.att = "undefined"
        self.head = -1
        self.tail = -1  
        self.flow = []
        self.cost = []
class GraphClass(object):
    def __init__(self):
        self.ODs = []
        self.edges  = []
        self.nodes = []
