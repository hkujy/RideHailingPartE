"""
class
"""
class NodeClass(object):
    def __init__(self):
        self.id = -1
        self.name = "undefined"
        self.att = "undefined"
        self.x = -1
        self.y = -1
        self.outlinks=[]
        self.outlinks=[]

class CostClass(object):
    def __init__(self):
        self.inveh = -1   # inveh travel time 
        self.wt = -1   # waiting time
        self.ct = -1   # congestion cost
        self.fare = -1  # fare
        self.tt = -1    # total travel cost
        self.walk = -1    # total travel cost

class OdClass(object):
    def __init__(self):
        self.id = -1
        self.pair = "undefined"
        self.origin = -1
        self.dest = -1
        self.demand = -1
        #TODO: here I only list two modes as an example, you need to add others
        self.nest_modes = {"auto":["car","RH"],
                           "tranit":["bus"],
                           "combine":["P+R","R+H"]}
        self.modes = ["car","RH","bus","P+R","R+H"]   # how many modes connecting this OD pair
        self.mode_path_set = {"car":[], "bus":[], "RH":[], "bus":[], "P+R":[], "R+H":[] }
        self.mode_flow = {"car":-1, "bus":-1, "RH":-1, "bus":-1, "P+R":-1, "R+H":-1}
        self.mode_utility = {"car":-1, "bus":-1, "RH":-1, "bus":-1, "P+R":-1, "R+H":-1}
        self.nest_mode_flow = {"auto":-1, "tranit":-1, "combine":-1}
        self.nest_mode_utility = {"auto":-1, "tranit":-1, "combine":-1}


class PathClass(object):
    def __init__(self):
        self.id = -1
        self.mode = -1
        self.od = -1
        self.cost = CostClass()
        self.nodes = []  # visited nodes
        self.edges = []  # visted edges
        self.prob = -1
        self.flow = []  # flow value

class EdgeClass(object):
    def __init__(self):
        self.id = -1
        self.type = -1
        self.att = "undefined"
        self.head = "undefined"
        self.tail = "undefined"
        self.lenth = 0
        self.flow = -1
        self.cost = CostClass()
        self.cap = -1

class GraphClass(object):
    def __init__(self):
        self.ODs = []
        self.edges = []
        self.nodes = []

class BusClass(object):
    """
        Bus class 
        The vector contains the cost for all days
    """
    def __init__(self):
        self.id = -1
        self.fre = []
        self.cap = -1

def print_obj(obj):
    """
        print  a class objective
    """
    print('\n'.join(['%s:%s' % item for item in obj.__dict__.items()]))