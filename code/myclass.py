"""
    class
"""
class CompeteLinkClass():
    def __init__(self,_lid):
        self.edgeId = _lid
        self.CommonLines = []

class BusClass(object):
    def __init__(self):
        self.id = -1
        self.stops = []
        self.sts= []  # travel time between two stops
        self.fre = -1
        self.cap = -1

    def get_cost_between_any_two_stops(self,_start_stop,_end_stop):
        """
            given any two stops of a bus line
            find the travel time between the two stops
            #TODO: not yet debug this function
        """
        _time = 0.0
        for i in range(0,len(self.stops)):
            if (self.stops[i] == _start_stop):
                for j in range(i+1,len(self.stops)):
                    # print("i={0},j={1}".format(i,j))
                    if self.stops[j] == _end_stop:
                        _time = _time + self.sts[j-1]
                        break
                    else:
                        _time = _time + self.sts[j-1]
        return _time

class NodeClass(object):
    def __init__(self):
        self.id = -1
        self.name = "undefined"
        self.att = "undefined"
        self.x = -1
        self.y = -1
        self.outlinks=[]
        self.inlinks=[]

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

        self.nest_modes = {"single":["car","RH","bus"],
                           "combine":["P+R","R+H"]}
        self.modes = ["car","RH","bus","P+R","R+H"]   # how many modes connecting this OD pair
        self.mode_path_set = {"car":[], "bus":[], "RH":[], "bus":[], "P+R":[], "R+H":[] }

        self.mode_flow = {"car":-1, "bus":-1, "RH":-1, "bus":-1, "P+R":-1, "R+H":-1}
        self.mode_utility = {"car":-1, "bus":-1, "RH":-1, "bus":-1, "P+R":-1, "R+H":-1}

        self.nest_mode_flow = {"single":-1, "combine":-1}
        self.nest_mode_utility = {"single":-1, "combine":-1}


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
        self.from_node = "undefined"
        self.to_node = "undefined"
        self.lenth = 0
        self.flow = -1
        self.cost = CostClass()
        self.cap = -1
    #   add properties for bus links
    #   - set of bus lines contained 
        self.bus_lines = []
    #   - competing sections 
        self.compete_bus_links = []
    # #   - set of normal links it traverse
    #     I donnot think we need the following data in the current version
    #     self.traverse_road_links = [] 
    #   - frequency of the bus line 
        self.fre = []

    def cal_bus_edge_fre(self,_buses):
        """
            cal the total frequency of bus lines on one edge
        """
        for b in self.bus_lines:
            self.fre.append(_buses[b].fre)
     

class GraphClass(object):
    def __init__(self):
        self.ODs = []
        self.edges = []
        self.nodes = []
        self.buses = []

def print_obj(obj):
    """
        print  a class objective
    """
    print('\n'.join(['%s:%s' % item for item in obj.__dict__.items()]))