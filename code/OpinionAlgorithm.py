import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import OpinionGraph


def SimulationBeginEnd(graph, phi, n_step):
    
    layout=nx.spring_layout(graph)
    
    print('------------- Initial graph ------------')
    OpinionGraph.Plot(graph, layout)
    plt.show()
        
    for i in range(n_step):
        graph = OneStep(graph, phi, layout=layout, verbose=False)
    
    print('------------- Final graph ------------')
    OpinionGraph.Plot(graph, layout)
    plt.show()


def Simulation(graph, phi, n_step, verbose=False):
    
    layout=nx.spring_layout(graph)

    if verbose:
        print('------------- Initial graph ------------')
        OpinionGraph.Plot(graph, layout)
        plt.show()
        
    for i in range(n_step):
        if verbose:
            print('------------- Step {0} ------------'.format(i))
        OneStep(graph, phi, layout=layout, verbose=verbose) 

#Do one step of the model
def OneStep(graph, phi, layout=None, verbose=False):
    
    if layout==None:
        layout=nx.spring_layout(graph)
    
    node_i = int(np.random.choice(graph.nodes(), 1))
    if verbose:
        print('Node i selected : {0}'.format(node_i))
        
    if graph.degree[node_i] == 0:
        if verbose:
            print('Degree of node i is 0.')
        return graph
    else:
        bool_step = np.random.choice(np.array([True, False]), size=1, p=np.array([phi, 1-phi]))
        if bool_step:
            if verbose:
                print('DOING STEP 1')
            graph = Step1(graph, node_i, verbose=verbose)
        else:
            if verbose:
                print('DOING STEP 2')
            graph = Step2(graph, node_i, verbose=verbose)
    if verbose:
        OpinionGraph.Plot(graph, layout)
        plt.show()
    return graph

# Step 1 represents the formation of new acquaintances between people of similar opinions.
def Step1(graph, node_i, verbose):
    opinion_gi = graph.nodes[node_i]['opinion']
    
    edges_list = list(graph.edges(nbunch=node_i))
    edge_selected = int(np.random.choice(len(edges_list), 1))
    node_j = edges_list[edge_selected][1]
    
    nodes_with_gi = [n for n, attr in graph.nodes(data=True) if attr['opinion']==opinion_gi]
    node_j_prime = int(np.random.choice(nodes_with_gi, 1))

    graph.remove_edge(node_i, node_j)
    graph.add_edge(node_i, node_j_prime)
    if verbose:
        print('Edge moved from node {0} to node {1}'.format(node_j, node_j_prime))
    return graph

#Step 2 represents the influence of acquaintances on one another, opinions becoming similar as a result of acquaintance.
def Step2(graph, node_i, verbose):
    neighbours = list(graph[node_i])
    node_j = int(np.random.choice(neighbours, 1))
    previous_opinion = graph.node[node_i]['opinion']
    graph.node[node_i]['opinion'] = graph.node[node_j]['opinion']
    if verbose:
        print('Opinion of node {0} changed from {1} to {2}'.format(node_i, previous_opinion, graph.node[node_i]['opinion']))
    return graph