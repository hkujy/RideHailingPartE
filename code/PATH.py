"""generate path set and compute path cost 
"""

import networkx as nx
import pandas as pd
import math

# generate a pathset
def get_path_set(G, origin_zone, destination_zone):
    """
    generate a path set and compute path attributes (O_node, D_node, links, cost, path flow, prob, logit_prob, y_flow) 

    Args:
        G ([graph]): [network]
        origin_zone ([list]): [list of origin zones]
        destination_zone ([list]): [list of destination zones]
        theta_1 ([float]): [parameter of logit model for path choice]
        
    Returns:
        [pd.DataFrame]: [path set]
    """

    # initialize a paths set
    paths = []
    for i in origin_zone:
        for j in destination_zone:
            for path in nx.all_simple_edge_paths(G, source= i, target= j): # generate all paths 
                od_pair = i +'-'+ j # record origin zone and destination zone
                links = path # record links
                link_sque =[G.edges[edge]['link_id'] for edge in path] # record links ID
                name_sque = [G.edges[edge]['name'] for edge in path]
                attribute_set = [G.edges[edge]['attribute'] for edge in path]            
                paths.append([od_pair, links, link_sque, name_sque, attribute_set])

    # generate a path information table based pandas DataFrame
    path_set = pd.DataFrame(paths, columns = ['OD_pair', 'links','link_sque','name_sque','attribute_set'])

    # map travel mode
    def map_mode(x):
        if x['attribute_set'] in [['board_auto', 'auto', 'alight_auto']]:
            return 'auto'
        elif x['attribute_set'] in [['board_transit', 'transit', 'alight_transit'],
                                    ['board_transit', 'transit', 'transit-transfer', 'alight_transit']]:
            return 'transit'
        elif x['attribute_set'] in [['board_auto', 'auto', 'P&R', 'transit', 'alight_transit'], 
                                    ['board_auto', 'auto', 'P&R', 'transit', 'transit-transfer', 'alight_transit']]:
            return 'P&R'
        elif x['attribute_set'] in [['board_ride-hailing', 'ride-hailing', 'R&T', 'transit', 'alight_transit'],
                                    ['board_ride-hailing', 'ride-hailing', 'R&T', 'transit', 'transit-transfer', 'alight_transit']]:
            return 'R&T'
        else:
            return 'other'

    path_set['attribute_set'] = path_set['attribute_set'].apply(lambda x: sorted(set(x),key=x.index))
    path_set['mode'] = path_set.apply(map_mode, axis=1)
    path_set = path_set[path_set['mode'].isin(['auto', 'P&R','transit', 'R&T'])]
    path_set['path_id'] = range(1, len(path_set)+1)
    path_set['path_id'] = 'path' + '-' + path_set['path_id'].astype('str')

    return path_set[['OD_pair','path_id','mode','link_sque','name_sque','attribute_set']]

#######################################################################################
def get_path_info(path_set, link_table):
    """according to link-path matrix index to compute each path information

    Args:
        path_set ([pd.DataFrame]): [path set]

    Returns:
        [pd.DataFrame]: [path set after computing information]
    """
    path_length =[]
    path_travel= []
    path_walk = []
    path_wait = [] 
    path_congestion = []
    path_penalty = []
    path_fare = []
    for i in range(len(path_set)):
        link_sque = path_set['link_sque'].iloc[i]
        one_path = link_table[link_table['link_id'].isin(link_sque)]
        path_length.append(one_path['l_a'].sum())
        path_travel.append(one_path['travel'].sum())
        path_walk.append(one_path['walk'].sum())
        path_wait.append(one_path['wait'].sum())
        path_congestion.append(one_path['congestion'].sum())
        path_penalty.append(one_path['penalty'].sum()) 
        path_fare.append(one_path['fare_rate'].sum())
    
    path_set['path_length'] = path_length
    path_set['path_travel'] = path_travel
    path_set['path_walk'] = path_walk
    path_set['path_wait'] = path_wait
    path_set['path_congestion'] = path_congestion
    path_set['path_penalty'] = path_penalty
    path_set['path_fare'] = path_fare
    
    return path_set

########################################################################################
def cost_func(x, miu_in, miu_out, lamda_0_transit):
    """compute path cost

    Args:
        x ([pd.DataFrame]): [path info]
        miu_in (int, optional): [in-vahile VOT]. Defaults to 2.
        miu_out (int, optional): [out-vahile VOT]. Defaults to 3.
        lamda_0_transit (int, optional): [transit ticket]. Defaults to 3.

    Returns:
        [pd.Series]: [path cost]
    """
    cost = miu_in / 60 * (x['path_travel'] + x['path_congestion']) + miu_out / 60 * (x['path_walk']+ x['path_wait'] + x['path_penalty']) + x['path_fare']

    if x['mode'] in ['auto']:
        return -cost
        
    elif x['mode'] in ['transit', 'P&R', 'R&T']:
        return -(cost + lamda_0_transit)
    
    elif x['mode'] in ['R&T']:
        return -(cost + lamda_0_transit + 10 ) # 起步价

def cost_exp(x, theta_1):
    """compute cost exp

    Args:
        x ([pd.DataFrame]): [path info]
        theta_1 (float, optional): [logit parameter in path level]. Defaults to 0.1.

    Returns:
        [type]: [description]
    """
    return  math.exp(theta_1 * (x['path_cost'] / 100)) # cost的尺度很大，除以100

def path_cost(path_set, miu_in, miu_out, lamda_0_transit, theta_1):
    """path_set after computing path cost

    Args:
        path_set ([pd.DataFrame]): [path info]

    Returns:
        [pd.DataFrame]: [path set with path cost]
    """
    path_set['path_duration'] = path_set['path_travel'] + path_set['path_walk'] + path_set['path_wait'] + path_set['path_congestion']
    path_set['path_cost'] = path_set.apply(cost_func, miu_in=miu_in, miu_out=miu_out, lamda_0_transit=lamda_0_transit, axis=1)
    path_set['path_exp'] = path_set.apply(cost_exp, theta_1=theta_1, axis=1)

    #path_set = path_set[['OD_pair','path_id','mode','link_sque','name_sque''path_length','path_duration','path_cost', 'path_exp']]
    return path_set






