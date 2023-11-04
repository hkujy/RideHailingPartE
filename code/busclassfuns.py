"""_summary_
for the bus class and operations 
"""
import myclass as mc 
import pandas as pd
import mypara

def get_bus_edge_index(_para:mypara.ParaClass,_id):
    """
        the bus id starts after the edges index
    """
    return (_para.para_dict['Num_None_BusLinks'] + _id)

def read_bus_data():
    """_summary_
    """
    df = pd.read_csv('../input_network/Stops.txt',header=None,delim_whitespace=True)
    buses = []

    for i in range(0, df.shape[0]):
       buses.append(mc.BusClass())
       buses[-1].id = i  
       for j in range(1,df.shape[1]-1):  # staring from 1, as the first is the bus number index
           if df[j][i]>0:
               buses[-1].stops.append(df[j][i])

    df = pd.read_csv('../input_network/buscap.txt',header=None,delim_whitespace=True)
    for b in range(0, df.shape[0]):
        buses[b].cap = df[0][b]
    df = pd.read_csv('../input_network/inifre.txt',header=None,delim_whitespace=True)
    for b in range(0, df.shape[0]):
        buses[b].fre = df[0][b]

    # read travel time between bus stops 
    df = pd.read_csv('../input_network/BusStopTimes.txt')
    for row in range(0, df.shape[0]):
        _id = df["line"][row]-1
        _tt = df["time"][row]
        buses[_id].sts.append(_tt)
        
    print("---------------------------------------")
    print("-----------Print Check Bus Linkes------")
    for b in buses:
        mc.print_obj(b)
    print("-----------Print Check Bus Linkes------")
    return buses

def cal_bus_edge_inveh_and_waiting_time(_edges,_buses,_para:mypara.ParaClass):
    """
        this is written in case of changing frequency will affect the bus cost
    """
    #TODO: not yet debug this function
    ## loop the bus links only
    for e in range(_para.para_dict['Num_None_BusLinks'],len(_edges)):
        if _edges[e].type!="bus":
            print("Warning: bus edge type does not set correctly")
        #### cal calute the waiting time cost
        ## double check whether this is the same as your paper
        _edges[e].cost.wt = 1.0/sum(_edges[e].fre)  
        _edges[e].cost.inveh = 0.0
        _edges[e].cap = 0
        start_stop = _edges[e].from_node
        end_stop = _edges[e].to_node
        for lid in _edges[e].bus_lines:
            line_time = _buses[lid].get_cost_between_any_two_stops(start_stop,end_stop)
            _edges[e].cost.inveh = _edges[e].cost.inveh + line_time * (_buses[lid].fre/sum(_edges[e].fre))
            _edges[e].cap = _edges[e].cap+(_buses[lid].fre/sum(_edges[e].fre))*_buses[lid].cap

def cal_bus_edge_congestion_cost(_edges,_buses,_para:mypara.ParaClass):
    """
        1.after compute the path flow 
        2.compute the bus edge flow
        3.considers the competing bus section
    """
    #TODO: not yet debug this function
    # step 1: 
    for e in range(_para.para_dict['Num_None_BusLinks'],len(_edges)):
        compete_flow = 0.0
        for ce in _edges[e].compete_bus_links: # loop competing links
            compete_edge_id = ce.edgeId 
            for l in ce.CommonLines:   # loop all the section
                compete_flow=compete_flow + \
                (_buses[l].fre/sum(_edges[compete_edge_id].fre))*_edges[compete_edge_id].flow

        # TODO: you may add BRP function paramters to the following bus function
        print("---------------------------------------")
        print("Reminder: update Bus BPR cost function")
        _edges[e].cost.ct = (compete_flow + _edges[e].flow)/(_edges[e].cap)         
        print("---------------------------------------")

def append_bus_edges(_edges,_buses,_para:mypara.ParaClass):
    """_summary_
        append bus links to existing set of links
    """
    #TODO: not yet debug this function
    # step 1 . create basic bus edges
    _para.para_dict['Num_None_BusLinks'] =len(_edges)
    df = pd.read_csv("../input_network/BusLinkOverView.txt")
    print(df)
    for row in range(0,df.shape[0]):
        _id = df["link"][row]-1    # make it starting from 0 
        _from_node = df["anode"][row]
        _to_node = df["bnode"][row]
        # append bus edges 
        _edges.append(mc.EdgeClass())
        _edges[-1].id= get_bus_edge_index(_para,_id)  
        _edges[-1].type = "bus"     # how do you set the types 
        _edges[-1].from_node = _from_node      
        _edges[-1].to_node = _to_node

    # step 2 . append transit lines to the bus edges

    df = pd.read_csv("../input_network/BusLinkContainLines.txt")
    for row in range(0,df.shape[0]):
        _id = df["Link"][row]-1    # make it starting from 0 
        _line = df["Line"][row]-1
        _edge_id = get_bus_edge_index(_para,_id)
        _edges[_edge_id].bus_lines.append(_line)
        _edges[_edge_id].fre.append(_buses[_line].fre)

    # step 3 . get competing section and correpsonding bus lines
    df = pd.read_csv("../input_network/BusLink2Compete.txt")
    print(df)
    # input()
    for row in range(0,df.shape[0]):
        _id = df["Link"][row]-1    # make it starting from 0 
        _edge_id = get_bus_edge_index(_para,_id)
        _compete_lid = df["Comp"][row]
        _compete_edge_id = get_bus_edge_index(_para,_compete_lid) 
        _edges[_edge_id].compete_bus_links.append(mc.CompeteLinkClass(_compete_edge_id))
        for l in _edges[_edge_id].bus_lines:
            if l in _edges[_compete_edge_id].bus_lines:
                _edges[_edge_id].compete_bus_links[-1].CommonLines.append(l)


def Test_Cal_Bus_Congestion_Cost(_net:mc.GraphClass,_para: mypara.ParaClass):
    """
        function to test the calucation of bus congestion cost
    """
    # step 1: give bus edges random flow value
    for e in _net.edges:
        if e.type=="bus":
           e.flow = e.id*10   # just an arbitrary value as the flow value
    cal_bus_edge_congestion_cost(_net.edges,_net.buses,_para)


def print_bus_edges(_edges):
    """
        print and check the bus edges
    """
    for e in _edges:
        if e.type == "bus":
            print("****************")
            print("edge id = {0}".format(e.id))
            print("ContainLines = ",e.bus_lines)
            print("ContainLinefre = ",e.fre)
            print("WaitingTime = ",e.cost.wt)
            print("Cap = ",e.cap)
            print("Inveh = ",e.cost.inveh)
            print("CongestionCost = ", e.cost.ct)
            for ce in e.compete_bus_links:
                print("com_edge_id = {0}".format(ce.edgeId))
                print("CommonLines = ",ce.CommonLines)


