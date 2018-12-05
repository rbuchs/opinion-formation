import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import time

def SimulationEndConsensus(graph, phi, verbose=False, checkconsensus=1):
    """
    Perform the simulation of the Holme-Newman model until the consensus is reached.

    Parameters
    ----------
    graph : OpinionGraph
        The OpinionGraph on which the Holme-Newman model is performed.
    phi : float
        The value of the parameter $\phi$.
    verbose : bool, optional
        If True, prints detailed information on the graph every 1000 iterations.
    checkconsensus : int, optional
        Deprecated; it was used to speed computation by not checking only every 'checkconsensus' iterations if the consensus was reached. Indeed, this consensus check was expensive in the previous implemenattaion.
    Returns
    -------
    n_step: the number of steps required to reach consensus.
    """
    
    t0 = time.time()  
    consensus = graph.ConsensusReached()
    n_step = 0
    s = 0
    
    #Compute the picked node and which step (1/2) will be taken at each iteration. Compute for first 1e6 iterations
    n_iter_batch = int(1e6)
    nodes = np.random.choice(graph.internal_graph.nodes(), n_iter_batch)
    bool_step = np.random.choice(np.array([True, False]), size=n_iter_batch, p=np.array([phi, 1-phi]))
    
    while not consensus: #performs iterations of the model until consensus is True
        graph = OneIteration(graph, nodes[s], bool_step[s]) #perform one iteration of the model
        if (s%1000 == 0) and (verbose==True): #prints information every 1000 iterations if verbose is True
            log(t0, 'Iteration {0}'.format(n_step+s))
            print('Number of components', graph.NComponents())
            print('Number of components in consensus', graph.ConsensusState().sum())
            print('Percentage nodes in consensus', graph.PercentageNodesConsensusState())
        s += 1
        if (s%(n_iter_batch) == 0): #Every 'n_iter_batch' recompute the picked node and which step (1/2) will be taken at each iteration for the next 'n_iter_batch' iterations
            nodes = np.random.choice(graph.internal_graph.nodes(), n_iter_batch)
            bool_step = np.random.choice(np.array([True, False]), size=n_iter_batch, p=np.array([phi, 1-phi]))
            n_step += n_iter_batch #add number of iterations in batch
            s = 0 #restart iterations counter of batch
        if (n_step%checkconsensus == 0): #Check if consensus is reached
            consensus = graph.ConsensusReached()
    n_step += s #add number of iterations in last batch
    if verbose==True:    
        log(t0, 'Total nuber of steps : {0}'.format(n_step))
    return n_step #total number of iterations (i.e. number of batches*'n_iter_batch' + number of iterations in last batch)

def Simulation(graph, phi, n_step, verbose=False, verboseBeginEnd=False):
    """
    Perform the simulation of the Holme-Newman model on a finite number of iterations 'n_step'.

    Parameters
    ----------
    graph : OpinionGraph
        The OpinionGraph on which the Holme-Newman model is performed.
    phi : float
        The value of the parameter $\phi$.
    n_step : int
        The number of iterations of the model to be performed.
    verbose : bool, optional
        If True, prints detailed information on all the steps performed.
    verboseBeginEnd : bool, optional
        If True, prints detailed information on the intial and final graph. Also plots the initial and final graph.
        
    Returns
    -------
    Nothing
    """
    
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

def OneIteration(graph, node_i, bool_step, layout=None, verbose=False):
    """
    Perform one iteration of the Holme-Newman model.

    Parameters
    ----------
    graph : OpinionGraph
        The OpinionGraph on which the Holme-Newman model is performed.
    node_i : int
        The node of the 'graph' on which the iteration is performed.
    bool_step : bool
        If True the Step 1 of the Holme-Newman model is performed otherwise it is the Step 2 that is performed.
    layout : dict, optional
        A dictionary of positions keyed by node. Used to plot the graph if verbose is True.
    verbose : bool, optional
        If True, prints detailed information on the step performed and plots the graph.
        
    Returns
    -------
    graph : The modified OpinionGraph after Step 1 or 2 is performed
    """
    
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
    """
    Prints the time elapsed since 't0' and some text.
    
    Parameters
    ----------
    t0 : float
        The original time.
    text : str
        A string to be printed

    """
    print(time.time()-t0, text)
