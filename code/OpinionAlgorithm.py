import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import time
import OpinionGraph


def SimulationBeginEnd(graph, phi, n_step, verbose=False):
    
    layout=None
    if verbose:
        layout=nx.spring_layout(graph)
        print('------------- Initial graph ------------')
        OpinionGraph.Plot(graph, layout)
        plt.show()
        
    for i in range(n_step):
        graph = OneStep(graph, phi, layout=layout, verbose=False)
        
    if verbose:
        print('------------- Final graph ------------')
        print('**** Same layout **** ')
        OpinionGraph.Plot(graph, layout)
        plt.show()
        print('**** New layout **** ')
        OpinionGraph.Plot(graph)
        plt.show()

def SimulationEndConsensus(graph, phi, verbose=False):
    t0 = time.time()  
    consensus = OpinionGraph.ConsensusState(graph).all()
    n_step = 0
    
    while not consensus:
        graph = OpinionAlgorithm.OneStep(graph, phi)
        n_step += 1
        if (n_step%1000 == 0) and (verbose==True):
            log(t0, 'Step {0}'.format(n_step))
            print('Number of components', OpinionGraph.NComponents(graph))
            print('Number of components in consensus', OpinionGraph.ConsensusState(graph).sum())
            print('Percentage nodes in consensus', OpinionGraph.PercentageNodesConsensusState(graph))
        consensus = OpinionGraph.ConsensusState(graph).all()
        
    if verbose==True:    
        log(t0, 'Total nuber of steps : {0}'.format(n_step))
    return n_step

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
    
    if (verbose==True) and (layout==None):
        layout=nx.spring_layout(graph)
    
    node_i = int(np.random.choice(graph.nodes(), 1))
    if verbose:
        print('Selected node_i : {0}'.format(node_i))
        
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
        #limitations: can form acquaintance with itself or 'double' existing acquaintance
def Step1(graph, node_i, verbose):
    #take opinion of node_i
    opinion_gi = graph.nodes[node_i]['opinion']
    
    #Compute neighbours of node_i (can have itself, and many occurence of same neighbour)
    neighbors = list(graph.neighbors(node_i))
    if verbose:
        print('Neighbors of node_i : {0}'.format(neighbors))
    
    #Select random neighbor. This aquaintance will be deleted. (tend to delete more easily the ''mulit-aquaintances'
    #or multi-self-loop')
    node_j = int(np.random.choice(neighbors, 1))
    if verbose:
        print('Selected node_j : {0}'.format(node_j))
    
    #Compute all nodes with opinion of node_i
    nodes_with_gi = [n for n, attr in graph.nodes(data=True) if attr['opinion']==opinion_gi]
    if verbose:
        print('Nodes with opinion g_i : {0}'.format(nodes_with_gi))
        
    #Select randomly the new aquaintance
    node_j_prime = int(np.random.choice(nodes_with_gi, 1))
    if verbose:
        print('Selected node_j_prime : {0}'.format(node_j_prime))

    graph.remove_edge(node_i, node_j)
    graph.add_edge(node_i, node_j_prime)
    if verbose:
        print('Edge moved from ({0},{1}) to ({0},{2})'.format(node_i, node_j, node_j_prime))
    return graph

#Step 2 represents the influence of acquaintances on one another, opinions becoming similar as a result of acquaintance.
def Step2(graph, node_i, verbose):
    
    #Compute neighbours of node_i (can have itself, and many occurence of same neighbour)
    neighbors = list(graph.neighbors(node_i))
    if verbose:
        print('Neighbors of node_i : {0}'.format(neighbors))
        
    #Select random neighbor.
    node_j = int(np.random.choice(neighbors, 1))
    if verbose:
        print('Selected node_j : {0}'.format(node_j))
    
    #Opinion of node_i
    previous_opinion = graph.node[node_i]['opinion']
    #Change opinion of node_i to the one of node_j
    graph.node[node_i]['opinion'] = graph.node[node_j]['opinion']
    if verbose:
        print('Opinion of node {0} changed from {1} to {2}'.format(node_i, previous_opinion, graph.node[node_i]['opinion']))
    return graph

def log(t0, text):
    print(time.time()-t0, text)