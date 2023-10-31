"""
comupute idle ride-hailing vehiles 
"""

def compute_idle_vehile(link_table, N_hailing):
    """
    computing idle ride-hailing vehicles based on conservation equation
    conservation equation: N_ride-hailing = n_idle + q_comb (travel_time + waiting_hailing) 

    Args:
        link_table ([pd.DataFrame]): [link table after assigning flow]
        N_hailing ([int]): [all ride-hailing vehiles in the network]

    Returns:
        [int]: [idle ride-hailing vehiles]
    """
    hailing_link = link_table[link_table['attribute'].isin(['board_ride-hailing','ride-hailing'])]
    occupied_hailing = ((hailing_link['travel'] + hailing_link['walk'] +hailing_link['wait']) /60 * hailing_link['flow']).sum()
    return max(N_hailing-occupied_hailing, 0)