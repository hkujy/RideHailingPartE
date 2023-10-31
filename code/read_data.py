"""
    read input data from files
"""
import pandas as pd
import numpy as np
import os
import sys
import myclass as mc
import copy
    


def read_data():
    """
        retrun demand, link, nodes
    """
    # step 1: create links
    links = []
    my_link = pd.read_excel('../input_network/Nguyen_Dupuis_0515.xlsx', sheet_name='link_info')
    my_link['I'] = 0
    for l in range(0, my_link.shape[0]):
       links.append(mc.EdgeClass()) 
       links[-1].id = l 
       links[-1].type = my_link["type"][l]
       links[-1].att = my_link["attribute"][l]
       links[-1].tail = my_link["from"][l]
       links[-1].head = my_link["to"][l]
       links[-1].flow = my_link["flow"][l]
       links[-1].fare = my_link["fare_rate"][l]
       links[-1].length = my_link["l_a"][l]
       #TODO: check how you set the cost values
       links[-1].cost.walk = my_link["walk"][l]
       links[-1].cost.wt = my_link["wait"][l]
       links[-1].cost.ct = my_link["congestion"][l]
       links[-1].cap = my_link["c_a"][l]
    # print(my_link)
    # for l in links:
        # mc.print_obj(l)
    # print(links)
    nodes = []
    my_node = pd.read_excel('../input_network/Nguyen_Dupuis_0515.xlsx', sheet_name='node_info')
    for n in range(0,my_node.shape[0]):
        nodes.append(mc.NodeClass())
        nodes[-1].id = n
        nodes[-1].name = my_node["name"][n]
        nodes[-1].att = my_node["attribute"][n]
        nodes[-1].x = my_node["x_coord"][n]
        nodes[-1].y = my_node["y_coord"][n]
    for n in nodes:
        mc.print_obj(n)

    # step 3: read demand

    my_demand = pd.read_excel('../input_network/Nguyen_Dupuis_0515.xlsx', sheet_name='demand_info')
    ODs = []
    for w in range(0,my_demand.shape[0]):
        ODs.append(mc.OdClass())
        ODs[-1].id = w
        ODs[-1].pair = my_demand["OD_pair"][w]
        ODs[-1].demand = my_demand["demand"][w]
        ODs[-1].origin = my_demand["origin"][w]
        ODs[-1].dest = my_demand["dest"][w]
    for w in ODs:
        mc.print_obj(w)

    # create link node relations
    for l in links:
        tail_node_name = l.tail
        tail_node_id = [n for n in nodes if n.name == tail_node_name][0].id
        nodes[tail_node_id].outlinks.append(l.id)
        head_node_name = l.head
        head_node_id = [n for n in nodes if n.name == head_node_name][0].id
        nodes[head_node_id].inlinks.append(l.id)

    net = mc.GraphClass() 
    net.ODs = copy.deepcopy(ODs)
    net.edges = copy.deepcopy(links)
    net.nodes = copy.deepcopy(nodes)


    return net



    # step 2: create nodes
    # exit()
    # my_node = pd.read_excel(r'D:\004_PhD_Dissertation\Paper_Code\Part3\input_network\Nguyen_Dupuis_0515.xlsx', sheet_name='node_info')
    # my_node = pd.read_excel('../input_network/Nguyen_Dupuis_0515.xlsx', sheet_name='node_info')
    my_link['name'] = my_link['from'].astype('str') +'-'+ my_link['to'].astype('str')
    # my_demand = pd.read_excel(r'D:\004_PhD_Dissertation\Paper_Code\Part3\input_network\Nguyen_Dupuis_0515.xlsx', sheet_name='demand_info')
    my_demand = pd.read_excel('../input_network/Nguyen_Dupuis_0515.xlsx', sheet_name='demand_info')
    print("Test reading demand")
    print(my_demand)
    print("Test reading links")
    print(my_link)
    print("Test reading nodes")
    print(my_node)

