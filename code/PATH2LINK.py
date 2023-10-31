"""path flow to link flow 
"""
def update_link_flow(path_set, link_table):
    """
    1. generate a link set based on path set after traffic assignment
    2. merge the path flow on the same link by the same mode
    3. generate a link flow dictionary
    4. map the link flow to the link table before traffic assignment

    Args:
        path_set ([pd.DataFrame]): [path set after comuting y_flow]
        link_lable ([pd.DataFrame]): [link table]

    Returns:
        [pd.DataFrame]: [link table after updating link flow]
    """

    # explode according to the name_sque
    path_to_link = path_set.explode('name_sque', ignore_index=True)
    path_to_link = path_to_link[['name_sque', 'mode', 'path_flow']]

    # generate a dictionary of link_name and path_flow
    path_to_link = path_to_link.groupby(by=['name_sque'], as_index=False).sum()
    path_flow_dict = {path_to_link['name_sque'][i]:path_to_link['path_flow'][i] for i in range(len(path_to_link))}

    #link_flow_dict = {link_table['name'][i]:link_table['flow'][i] for i in range(len(link_table))}
    #link_flow_dict |= path_flow_dict # update original flow
    # update original flow
    link_flow_dict = {link_table['name'][i]: link_table['flow'][i]for i in range(len(link_table))} | path_flow_dict

    # map path_flow to original links table
    link_table['flow'] = link_table['name'].map(link_flow_dict)
    return link_table