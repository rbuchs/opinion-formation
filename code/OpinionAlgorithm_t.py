import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import time

#checkconsensus speeds computation by not checking at everytime if we reached consensus (may end up doing more steps than needed though)
def SimulationEndConsensus(graph, phi, verbose=False, checkconsensus=1):
    t0 = time.time()  
    consensus = graph.ConsensusReached()
    n_step = 0
    s = 0
    
    #Compute the picked node and which step (1/2) will be taken at each iteration. Compute for first 1e6 iterations
    n_iter_batch = int(1e6)
    nodes = np.random.choice(graph.internal_graph.nodes(), n_iter_batch)
    bool_step = np.random.choice(np.array([True, False]), size=n_iter_batch, p=np.array([phi, 1-phi]))
    
    while not consensus:
        graph = OneIteration(graph, nodes[s], bool_step[s])
        if (s%1000 == 0) and (verbose==True):
            log(t0, 'Iteration {0}'.format(n_step+s))
            print('Number of components', graph.NComponents())
            print('Number of components in consensus', graph.ConsensusState().sum())
            print('Percentage nodes in consensus', graph.PercentageNodesConsensusState())
        s += 1
        if (s%(n_iter_batch) == 0):
            nodes = np.random.choice(graph.internal_graph.nodes(), n_iter_batch)
            bool_step = np.random.choice(np.array([True, False]), size=n_iter_batch, p=np.array([phi, 1-phi]))
            n_step += n_iter_batch
            s = 0
        if (n_step%checkconsensus == 0):
            consensus = graph.ConsensusReached()
    n_step += s
    if verbose==True:    
        log(t0, 'Total nuber of steps : {0}'.format(n_step))
    return n_step

def Simulation(graph, phi, n_step, verbose=False, verboseBeginEnd=False):
    
    layout = None
    if verbose or verboseBeginEnd:
        layout = nx.spring_layout(graph.internal_graph)
        print('------------- Initial graph ------------')
        graph.plot(layout)
        plt.show()
        
    #Compute the picked node and which step (1/2) will be taken at each iteration
    nodes = np.random.choice(graph.internal_graph.nodes(), int(n_step))
    bool_step = np.random.choice(np.array([True, False]), size=int(n_step), p=np.array([phi, 1-phi]))
    
    for i in range(n_step):
        if verbose:
            print('------------- Step {0} ------------'.format(i))
        graph = OneIteration(graph, nodes[i], bool_step[i], layout=layout, verbose=verbose)
        
    if verboseBeginEnd:
        print('------------- Final graph -------------')
        print('**** Same layout **** ')
        graph.plot(layout)
        plt.show()
        print('**** New layout **** ')
        graph.plot()
        plt.show()

#Do one step of the model
def OneIteration(graph, node_i, bool_step, layout=None, verbose=False):
    
    if (verbose==True) and (layout==None):
        layout=nx.spring_layout(graph.internal_graph)
        
    if verbose:
        print('Selected node_i : {0}'.format(node_i))
        
    if graph.internal_graph.degree[node_i] == 0:
        if verbose:
            print('Degree of node i is 0.')
        return graph
    else:
        if bool_step:
            if verbose:
                print('DOING STEP 1')
            graph.Step1(node_i, verbose=verbose)
        else:
            if verbose:
                print('DOING STEP 2')
            graph.Step2(node_i, verbose=verbose)
    if verbose:
        graph.plot(layout)
        plt.show()
    return graph

def log(t0, text):
    print(time.time()-t0, text)
