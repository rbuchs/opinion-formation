import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

#Create a random graph with n_nodes and m_edges. n_opinion is the number of possible opinions, stored in the 
#'opinion' attribut of the node. If not given n_opinion=n_nodes. The opinions are integers in [0, n_opinion]
#The graph can have multiedges and self-loops. Nevertheless, it is created with no multiedges and no self-loops.
def CreateRandom(n_nodes, m_edges, n_opinion=None):
    if n_opinion is None:
        n_opinion = n_nodes
    opinions = np.random.choice(n_opinion, n_nodes)
    
    graph = nx.gnm_random_graph(n_nodes, m_edges)
    
    # set opinions
    for n, o in zip(graph, opinions):
        graph.nodes[n]['opinion'] = o
    
    graph = nx.MultiGraph(graph)
    return graph

def Plot(graph, layout=None, axis=False):
    if layout==None:
        layout=nx.spring_layout(graph)
        
    plt.figure()
    op = list(nx.get_node_attributes(graph, 'opinion').values())
    ax = nx.draw_networkx(graph, pos=layout, with_labels=True, node_color=op, font_color='w')
    if not axis:
        plt.axis('off')

def Components(graph):
    return list(nx.connected_components(graph))

def NComponents(graph):
    return len(Components(graph))

def CountComponents(graph):
    return Counter([len(comp) for comp in Components(graph)])

def ConsensusState(graph, withnodes=False):
    consensus = []
    n_nodes = []
    for comp in Components(graph):
        subgraph = graph.subgraph(list(comp))
        opinions = list(nx.get_node_attributes(subgraph, 'opinion').values())
        consensus.append((opinions == opinions[0]).all())
        n_nodes.append(len(subgraph.nodes()))
    if withnodes:
        return np.array(consensus), np.array(n_nodes)
    else:
        return np.array(consensus)

def PercentageNodesConsensusState(graph):
    consensus, nodes = ConsensusState(graph, withnodes=True)
    return nodes[consensus].sum()/nodes.sum()
    