# generate a Graph
import networkx as nx
def get_graph(link_table, node_table):
    """
    generate a network based on link information and node information
    input: link_table and node table
    output: a graph

    Args:
        link_table ([pd.DataFrame]): [link table]
        node_table ([pd.DataFrame]): [node table]

    Returns:
        [graph]: [a graph for network]
    """

    # add eages from link table 
    G = nx.from_pandas_edgelist(df = link_table, 
                            edge_key= "link_id",
                            source = "from", 
                            target = "to", 
                            edge_attr=['name','link_id','type', 'attribute'], 
                            create_using=nx.MultiDiGraph())

    # add node attributes                       
    node_attributes = node_table.set_index('name').to_dict('index') # generate a node attributes dictionary 
    nx.set_node_attributes(G, node_attributes)

    return G