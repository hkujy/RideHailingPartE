"MAS assignment"

import link
import network
import path 
import mode
import path_to_link
import ride_hailing
import pandas as pd
from sklearn.metrics import mean_squared_error
import numpy as np


def assignment(my_link, my_node, my_demand, origin_zone, destination_zone,  
                   miu_in, miu_out, lamda_0_auto, lamda_0_transit, lamda_0_hailing, lamda_0_PR, 
                   N_hailing, theta_1, theta_2, A=2, bus_cap=120, maximum_iter = 200):
    
    """MSA solution for SUE equilibrium 

    Args:
        my_link ([pd.DataFrame]): [link table information]
        my_node ([pd.DataFrame): [node table information]
        my_demand ([pd.DataFrame]): [demand information]
        origin_zone ([list]): [origin]
        destination_zone ([list]): [destination]
        miu_in ([float]): [VOT in vehicle]
        miu_out ([float]): [VOT out vehicle]
        lamda_0_transit ([float]): [ticket price]
        lamda_0_hailing ([float]): [fare rate]
        lamda_0_PR ([float]): [parking charge]
        N_hailing ([float]): [fleet size]
        theta_1 ([float]): [logit parameter for path]
        theta_2 ([type]): [logit parameter for mode]
        maximum_iter (int, optional): [maximum iteration]. Defaults to 200.

    Returns:
        [tuple]: [iteration, res_link_flow, res_path_flow, res_path_set, res_mode_set, idle_ride_hailing]
    """

    # 0. generate path set
    my_network = network.get_graph(link_table=my_link, node_table=my_node)
    my_path_set = path.get_path_set(G=my_network, origin_zone=origin_zone, destination_zone=destination_zone)

    # 1. initializing path set
    # 1.1 initializing path cost
    my_path_set = path.get_path_info(path_set=my_path_set, link_table=my_link)
    my_path_set = path.path_cost(path_set=my_path_set, miu_in=miu_in, miu_out=miu_out, lamda_0_transit=lamda_0_transit, theta_1=theta_1)
    num_path = len(list(my_path_set['path_id']))
    print(list(my_path_set['path_id']))
    print(list(my_path_set['mode']))
    
    # initializing path flow
    my_path_set['path_flow'] = my_demand['demand'].sum() / len(my_path_set) # average assignment
    my_path_set['I'] = 0 # add initial iteration number

    # 1.2 generate mode set
    my_mode_set = mode.get_mode_set(paths=my_path_set,theta_1=theta_1,theta_2=theta_2)
    my_mode_set['I'] = 0 # add initial iteration number
    num_mode = len(list(my_mode_set['mode']))
    # print(my_mode_set['mode_logit'].sum())

    # 1.3 get demand-based flow
    new_paths = mode.get_y_flow(mode_set=my_mode_set, path_set=my_path_set, demand=my_demand)
    new_paths['I'] = 0 # add initial iteration number
    new_paths['path_flow'] = my_path_set['path_flow']

    ######################################################################################
    # iteration
    maximum_iter = maximum_iter
    acceptable_gap = 0.01
    
    # 1. initialize a list to store the result of each iteration
    iteration = []
    res_link_flow = my_link.copy()
    res_path_flow = new_paths.copy()
    res_path_set = my_path_set.copy()
    res_mode_set = my_mode_set.copy()
    idle_ride_hailing = [[0, N_hailing]]

    for I in range(1, maximum_iter+1):
        # 2.1 cheak the convergence
        MSE = mean_squared_error(new_paths['path_flow'].values, new_paths['y_flow'].values)
        RMSE = np.sqrt(MSE)
        print('Iteration = {0}, gap = {1},'.format(I, RMSE))

        if RMSE < acceptable_gap:
            break

        # 2.2 update path flow
        new_paths['path_flow'] = new_paths['path_flow'] + (1 / I) * (new_paths['y_flow'] - new_paths['path_flow'])
        path_flow = new_paths['path_flow'].values

        # 2.3 update link flow
        my_link_set = PATH2LINK.update_link_flow(path_set=new_paths, link_table=my_link)

        # 2.4 compute idle ride-hailing vehicle number
        n_idle_hailing = RIDE_HAILING.compute_idle_vehile(link_table=my_link, N_hailing=N_hailing)
        print(f'the number of idle_hailing:{n_idle_hailing}')

        # 2.5 update link cost
        my_link_set = LINK.compute_link_time(link_table= my_link_set,
                                             n_idle= n_idle_hailing,
                                             A = A,
                                             bus_cap = bus_cap,
                                             lamda_0_auto = lamda_0_auto,
                                             lamda_0_hailing= lamda_0_hailing,
                                             lamda_0_PR= lamda_0_PR)
        my_link_set['I'] = I # add iteration number in link_set
        # record wait time

        # 2.6 re-compute path information
        my_path_set = PATH.get_path_info(path_set= my_path_set, link_table= my_link_set)
        my_path_set = PATH.path_cost(path_set= my_path_set, miu_in= miu_in, miu_out= miu_out, lamda_0_transit= lamda_0_transit, theta_1= theta_1)
        my_path_set['I'] = I # add initial iteration number

        # 2.8 re-generate mode set
        my_mode_set = MODE.get_mode_set(paths=my_path_set, theta_1=theta_1, theta_2=theta_2)
        my_mode_set['I'] = I # add iteration number in mode_set
        #print(my_mode_set['mode_logit'].sum())

        # 2.9 re-generate y_flow
        new_paths = MODE.get_y_flow(mode_set=my_mode_set,path_set=my_path_set, demand=my_demand)
        new_paths['path_flow'] = path_flow # Update path flow for the next iteration based on MSA updating method 
        new_paths['I'] = I # add iteration number

        # 2.13 store the result of each iteration
            # 2.13.1 iteration number and gap
        iteration.append([I, RMSE])
            # 2.13.2 link_set
        res_link_flow = pd.concat([res_link_flow, my_link_set], ignore_index=True)
            # 2.13.3 path_set
        res_path_set = pd.concat([res_path_set, my_path_set], ignore_index=True)
        res_path_flow = pd.concat([res_path_flow, new_paths], ignore_index=True)
            # 2.13.4 mode_set
        res_mode_set = pd.concat([res_mode_set, my_mode_set], ignore_index=True)
            # 2.13.5 n_idle
        idle_ride_hailing.append([I, n_idle_hailing])

        # 3. transform the iteration to dataframe
    iteration = pd.DataFrame(iteration, columns=['I', 'RMSE'])
    idle_ride_hailing = pd.DataFrame(idle_ride_hailing, columns=['I', 'n_idle'])
    idle_ride_hailing['wait_time'] = idle_ride_hailing['n_idle'].apply(lambda x: (A / (1 + 0.15*x**0.5)) * 60)

    return iteration, res_link_flow, res_path_flow, res_path_set, res_mode_set, idle_ride_hailing, num_path, num_mode