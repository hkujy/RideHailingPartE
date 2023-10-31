# compute different time for each link

def compute_t0(x, v_auto=60, v_hailing=40, v_transit=20): # minutes
    """comupute free flow time for different modes

    Args:
        x ([pd.DataFrame]): [link info]
        v_auto (int, optional): [auto speed]. Defaults to 60.
        v_hailing (int, optional): [ride-hailing speed]. Defaults to 40.
        v_transit (int, optional): [transit speed]. Defaults to 20.

    Returns:
        [pd.Series]: [t_0]
    """

    if x['attribute'] == 'auto':
        return (x['l_a'] / v_auto) * 60
    
    elif x['attribute'] == 'ride-hailing':
        return (x['l_a'] / v_hailing) *60
    
    elif x['attribute'] == 'transit':
        return (x['l_a'] / v_transit)*60
    
    elif x['attribute'] == 'P&R':
        return 5

    else:
        return 0

def compute_travel_time(x): # minutes
    """compute the travel time

    Args:
        x ([pd.DataFrame]): [link info]

    Returns:
        [pd.Series]: [travel time]
    """
    
    if x['attribute'] in ['auto', 'P&R']:
        return x['t_0'] * (1 + 0.15 * (x['flow'] / x['c_a']) ** 4) # BPR function

    elif x['attribute'] == 'transit':
        return x['t_0'] * x['f_bus']/x['f_bus'] # compute travel time based on bus frequency 

    else:
        return x['t_0'] # the travel time for other modes is same as the free flow time

def compute_walk_time(x, v_walk=5.6): # minutes
    """compute_walk_time

    Args:
        x ([pd.DataFrame]): [link info]
        v_walk (float, optional): [walk speed]. Defaults to 5.6.

    Returns:
        [pd.Series]: [walk speed]
    """
    
    if x['attribute'] in ['transit-transfer', 'board_transit', 'alight_transit']: #by bus or bus transfer 
        return (x['l_a'] / v_walk) * 60

    elif x['attribute'] in ['board_ride-hailing', 'R&T']: # by ride-hailing
        return 3
    
    elif x['attribute'] in ['P&R']: # auto transfer bus
        return 5
    
    else: # other modes
        return 0

def compute_wait_time(x, n_idle, A): # minutes
    """compute_wait_time

    Args:
        x ([pd.DataFrame]): [link info]
        n_idle ([int]): [the number of idle ride-hailing vehicles]

    Returns:
        [pd.Series]: [wait time]
    """

    if x['attribute'] in ['transit-transfer','P&R','R&T','board_transit']:
        return 60 / x['f_bus']
    
    elif x['attribute'] in ['board_ride-hailing']:
        #A = 2 # waiting time coefficient 
        return (A / (1 +(0.15*n_idle)**0.5)) * 60
    
    else:
        return 0

def compute_congestion_time(x, bus_cap): # minutes
    """compute_congestion_time for transit link

    Args:
        x ([pd.DataFrame]): [link info]

    Returns:
        [pd.Series]: [congestion time]
    """

    if x['attribute'] in ['transit']:
        return   60 * 0.2 * (1* x['flow'] / (bus_cap * x['f_bus']))**3
    
    else:
        return 0

def compute_penalty(x, penalty=12): # minutes
    """add a transfer penalty for transfer link

    Args:
        x ([pd.DataFrame]): [link info]
        penalty (int, optional): [transfer penalty]. Defaults to 12 minutes.

    Returns:
        [pd.Series]: [transfer penalty]
    """

    return penalty if x['attribute'] in ['transit-transfer','P&R','R&T'] else 0

def compute_lamda_0_auto(fuel_consumption=6.46, driving_speed=50, fuel_price=9.2): #rmb/min
    """compute_lamda_0_auto: compute auto fare rate for auto link

    Args:
        fuel_consumption (float, optional): [fuel consumuption per 100 km]. Defaults to 6.46.
        driving_speed (int, optional): [average auto speed]. Defaults to 50.
        fuel_price (float, optional): [fuel price]. Defaults to 9.2.

    Returns:
        [int]: [fare rate: RMB/min]
    """

    lamda_0_auto = round((0.01 * fuel_consumption * fuel_price * driving_speed) / 60, 4) # unit: RMB/MIN, fare rate for auto
    print(lamda_0_auto)
    return lamda_0_auto

def compute_fare(x, lamda_0_hailing, lamda_0_PR, lamda_0_auto): # rmb
    """compute fare for each link

    Args:
        x ([pd.DataFrame]): [link info]
        lamda_0_hailing ([int]): [fare rate for ride-hailing service]
        lamda_0_PR ([int]): [park charge for P&R]

    Returns:
        [pd.Series]: [computed_fare]
    """
    if x['attribute'] in ['auto']:
        return (lamda_0_auto + 2) * (x['travel']) # RMB/min * min
    
    elif x['attribute'] == 'ride-hailing':
        return lamda_0_hailing * x['travel']  # 1.8RMB/km * km + 0.5 RMB/min * min，v-hailing = 60 km/h = 1 km/min
    
    elif x['attribute'] == 'P&R':
        return lamda_0_PR # RMB
    
    else:
        return 0

def compute_link_time(link_table, A, bus_cap, n_idle, lamda_0_hailing, lamda_0_PR,lamda_0_auto):
    """compute link time

    Args:
        link_table ([pd.DataFrame]): [link info]
        n_idle ([int]): [idle ride-hailing vehiles]
        lamda_0_auto ([int]): [fare rate for auto link]
        lamda_0_hailing ([int]): [fare rate for ride-hailing link]
        lamda_0_PR ([int]): [fare rate for P&R link]

    Returns:
        [type]: [description]
    """
    
    link_table['t_0'] = link_table.apply(compute_t0, axis = 1)
    link_table['travel'] = link_table.apply(compute_travel_time, axis = 1)
    link_table['fare_rate'] = link_table.apply(compute_fare, 
                                               lamda_0_hailing=lamda_0_hailing, 
                                               lamda_0_PR=lamda_0_PR,
                                               lamda_0_auto=lamda_0_auto,
                                               axis = 1) # RMB
    link_table['walk'] = link_table.apply(compute_walk_time, axis = 1)
    link_table['wait'] = link_table.apply(compute_wait_time, n_idle = n_idle, A = A, axis = 1)
    link_table['congestion'] = link_table.apply(compute_congestion_time, bus_cap=bus_cap, axis = 1)
    link_table['penalty'] = link_table.apply(compute_penalty, axis = 1)

    return link_table

def bus_frequency(x, f_bus):
    if x['attribute'] in['P&R','R&T']:
        return f_bus
    elif x['attribute'] in['transit','board_transit']:
        return 10
    else:
        return 0