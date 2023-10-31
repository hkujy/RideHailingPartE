"""compute mode possibility 
"""
import math
import pandas as pd

def get_mode_set(paths, theta_1, theta_2):
    """generate a mode set for the netwerork and calculate the mode choice probability.

    Args:
        paths ([pd.DataFrame]): [path set]
        theta_1 ([float]): [logit parameter for path]
        theta_2 ([float]): [logit parameter for mode]

    Returns:
        [pd.DataFrame]: [mode set information]
    """

    # computing the log-sum term for mode
    def get_log_sum(x):
        return (1/theta_1) * math.log(sum(x)+1)
    
    mode_set = pd.DataFrame(paths.groupby(by=['mode'], as_index=False)['path_exp'].apply(get_log_sum))
    mode_set.columns =['mode', 'path_logsum']

    # computing the negative unity term
    mode_set['exp_logsum'] = theta_2 * mode_set['path_logsum']
    mode_set['mode_logit'] = mode_set['exp_logsum'].apply(math.exp) / mode_set['exp_logsum'].apply(math.exp).sum()

    return mode_set

####################################################################################################################
def get_y_flow(mode_set, path_set, demand):
    """
    computing y_flow based on nested logit model
    Args:
        mode_set ([pd.DataFrame]): [mode set]
        path_set ([pd.DataFrame]): [path set]
        demand ([pd.DataFrame]): [trip demand between origin and destination]

    Returns:
        [pd.DataFrame]: [path set after computing 'y_flow' and 'path_prob']
    """

    # compute logit probability for path
    def logit_prob(x):
        return x / sum(x)
    
    # generate mode probability dictionary and demand dictionary
    mode_prob_dict = {mode_set['mode'][i] : mode_set['mode_logit'][i] for i in range(len(mode_set))}
    demand_dict = {demand['OD_pair'][i]:demand['demand'][i] for i in range(len(demand))}
    
    # map mode probability and demand to paths
    path_set['mode_logit'] = path_set['mode'].map(mode_prob_dict)
    path_set['demand'] = path_set['OD_pair'].map(demand_dict)
    
    # compute the mode flow
    path_set['mode_flow'] = path_set['demand'] * path_set['mode_logit']

    # compute logit probability for path
    path_set['path_logit'] = path_set.groupby(by=['mode'], as_index=False)['path_exp'].transform(logit_prob)

    # compute based-logit-probability flow (mode_flow * logit_prob_path)
    path_set['y_flow'] = path_set['mode_flow'] * path_set['path_logit']

    # compute based-flow probability
    #path_set['path_prob'] = path_set['path_flow'] / path_set['mode_flow']

    return path_set[['OD_pair','demand', 'path_id', 'name_sque','attribute_set', 'path_length','path_duration','path_cost',
                    'mode','mode_logit','mode_flow','path_logit','y_flow']]