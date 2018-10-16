import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

#Create a random graph with n_nodes and m_edges. n_opinion is the number of possible opinions, stored in the 
#'opinion' attribut of the node. If not given n_opinion=n_nodes. The opinions are integers in [0, n_opinion]
def CreateRandom(n_nodes, m_edges, n_opinion=None):
    if n_opinion is None:
        n_opinion = n_nodes
    opinions = np.random.choice(n_opinion, n_nodes)
    
    graph = nx.gnm_random_graph(n_nodes, m_edges)
    
    # set opinions
    for n, o in zip(graph, opinions):
        graph.nodes[n]['opinion'] = o
    
    return graph

def Plot(graph, layout=None, axis=False):
    if layout==None:
        layout=nx.spring_layout(graph)
        
    plt.figure()
    op = list(nx.get_node_attributes(graph, 'opinion').values())
    ax = nx.draw_networkx(graph, pos=layout, with_labels=True, node_color=op, font_color='w')
    if not axis:
        plt.axis('off')