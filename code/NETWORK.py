# generate a Graph
import networkx as nx
import myclass as mc
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

def create_netx_graph(my_net:mc.GraphClass):
    """
        from my own network to create a graph
    """
    G = nx.Graph()
    # add nodes
    for n in my_net.nodes:
        G.add_node(n.name)
    # add edges
    for e in my_net.edges:
        G.add_edge(e.from_node, e.to_node)
        # TODO: need to set the cost based on the weight
        # if e.type..
        G.edges[e.from_node,e.to_node]['weight'] = e.cost.wt
        G.edges[e.from_node,e.to_node]['origin_weight'] = e.cost.wt
        G.edges[e.from_node,e.to_node]['type'] = e.type

    # print and check and verify the edge weight
    for e in G.edges(): 
        print("from={0},to={1},weight={2},type={3}".format(
            e[0],e[1], G.edges[e[0],e[1]]['weight'],
            G.edges[e[0],e[1]]['type']
        ))

    return G





