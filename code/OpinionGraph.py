import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from copy import deepcopy

class OpinionGraph(object):
    def __init__(self, internal_graph, n_opinion, simple_graph):
        """
        Initialize an OpinionGraph. Assign the opinions randomly to the nodes and set the bookkeeping.
        
        Parameters
        ----------
        internal_graph : networkx.Graph or networkx.MultiGraph
            The internal graph.
        n_opinion : int
            The number of opinions to assign.
        simple_graph : bool
            If True, the internal Graph is a networkx.Graph, otherwise it is a networkx.MultiGraph
        
        """
        self.simple_graph = simple_graph
        self.internal_graph = internal_graph
        
        if n_opinion is None:
            n_opinion = len(self.internal_graph)
        opinions = np.random.choice(n_opinion, len(self.internal_graph))
        
        # set opiniions
        nx.set_node_attributes(internal_graph, values=dict(zip(range(len(self.internal_graph)), opinions)), name='opinion')
        
        self.node_with_opinion = []
        #Generate opinion lists
        for opinion in range(n_opinion):
            self.node_with_opinion.append([n for n, attr in self.internal_graph.nodes(data=True) if attr['opinion']==opinion])

        #Generate local consensus lists
        self.conL = [12345]*len(self.internal_graph)
        for n, attr in self.internal_graph.nodes(data=True):
            current_opinion = attr['opinion']
            neighbors = list(self.internal_graph.neighbors(n))
            self.conL[n] = self.localConsensus(current_opinion, neighbors)
            
    def get_random_choice(self, choice_list):
        """ 
        Return a random element in choice_list
        """
        l = len(choice_list)
        i = np.random.randint(0, l)
        return choice_list[i]    
    
    def average_clustering(self):
        """
        Return the average clustering coefficient for the internal graph.
        
        """
        return nx.average_clustering(self.internal_graph)

    def plot(self, layout=None, axis=False):
        """
        Plot the internal graph with a color gradient representing the different opinions. The nodes are labelled by their number.
        Parameters
        ----------
        layout : dict, optional
            A dictionary of positions keyed by node
        axis : bool, optional
            If True, plots a box around the graph
        
        """
        
        if layout==None:
            layout=nx.spring_layout(self.internal_graph)

        plt.figure()
        op = list(nx.get_node_attributes(self.internal_graph, 'opinion').values())
        ax = nx.draw_networkx(self.internal_graph, pos=layout, with_labels=True, node_color=op, font_color='w')
        if not axis:
            plt.axis('off')

    def Components(self):
        """
        Returns a list of the componenets of the graph.
        
        """
        return list(nx.connected_components(self.internal_graph))

    def NComponents(self):
        """
        Returns the number of componenets of the graph.
        
        """
        return len(self.Components())

    def CountComponents(self):
        """
        Returns a Counter with the number of componenets of the graph for each component size.
        
        """
        return Counter([len(comp) for comp in self.Components()])

    def ConsensusState(self, withnodes=False):
        """
        Parameters
        ----------
        withnodes : bool, optional
            if True, returns also the number of nodes which are in each component

        Returns
        -------
        Returns a list of booleans. Each entry correspond to a component of the graph and is True if it is in consensus. If 'withnodes' is True, it also returns the number of nodes in each component
        
        """
        consensus = []
        n_nodes = []
        #get the opinion of all nodes in the graph
        opinions = np.array(list(nx.get_node_attributes(self.internal_graph, 'opinion').values()))
        for comp in nx.connected_components(self.internal_graph): #for each component of the graph
            comp_opinions = opinions[list(comp)]
            consensus.append((comp_opinions == comp_opinions[0]).all()) #store True if all nodes have same opinion
            n_nodes.append(len(comp_opinions)) #store the number of nodes in the component
        if withnodes:
            return np.array(consensus), np.array(n_nodes)
        else:
            return np.array(consensus)
        
    def ConsensusReached(self):
        """
        Returns a boolean which is True if all componenets of the graph are in consensus (i.e. with all nodes having the same opinion)
        
        """
        return sum(self.conL) == 0

    def PercentageNodesConsensusState(self):
        """
        Returns the percentage of nodes that are in compenents which are in consensus (i.e. with all nodes having the same opinion).
        
        """
        consensus, nodes = self.ConsensusState(withnodes=True)
        return nodes[consensus].sum()/nodes.sum()

    def summary(self):
        """
        Prints a summary of the graph: total number of components, their sizes, if they are all in consensus and the share of nodes that are in componenets that are in consensus

        """
        # Total number of components
        print('Total number of components: {0}'.format(self.NComponents()))
        #Components size of the graph
        print('Components size: {{size: number}}={0}'.format(dict(self.CountComponents())))
        # Bool for consensus state in each component
        print('All components in consensus: {0}'.format(self.ConsensusState().all()))
        # percentage nodes in consensus components
        print('Percentage of nodes in components in consensus state: {0}'.format(self.PercentageNodesConsensusState()))
        
    def localConsensus(self, opinion, neighbors, verbose=False): 
        """
        Compute the local consensus of a node, i.e. the number of neighbouring nodes that have a different opinion than the central node. If it returns 0, the central node is in local consensus, i.e. surounded by like-minded people.

        Parameters
        ----------
        opinion : int
            opinion of the "central" node 
        neighbors : list
            list of neighbours of the "central" node
        verbose : bool, optional
            if it is True, prints detailed information about the local consensus

        Returns
        -------
        lcons: the number of entries in 'neighbors' that have a different opinion than 'opinion'

        """
        #at most all of the neighbours of the central node have a different opinion
        lcons = len(neighbors)
        
        if verbose:
            print("Number of neighbors :", lcons, "; My opinion :", opinion)
            
        for neigh in neighbors: #for each neighbour, if it has the same opinion as the central node, reduce the local consensus by one 
            if verbose:
                print("Neighbor ", neigh, "with opinion ", self.internal_graph.node[neigh]['opinion'])
            if self.internal_graph.node[neigh]['opinion'] == opinion:
                lcons-=1
        if verbose:
            print("Final = ", lcons)
        return lcons
    
    #limitations: can form acquaintance with itself or 'double' existing acquaintance
    def Step1(self, node_i, verbose):
        """
        Perform the Step 1 of the Holme-Newman model. It represents the formation of new acquaintances between people of similar opinions. An edge between $node_i$ and a randomly selected neighbour is moved to a node with the same opinion as $node_i$

        Parameters
        ----------
        node_i : int
            the node on which Step 1 is performed 
        verbose : bool
            if it is True, prints detailed information about the step

        Returns
        -------
        Nothing
        """
        #store opinion of node_i
        opinion_gi = self.internal_graph.nodes[node_i]['opinion']

        #Compute neighbours of node_i (can have itself, and many occurence of same neighbour if the interal_graph is a multi-graph)
        neighbors = list(self.internal_graph.neighbors(node_i))

        if verbose:
            print('Neighbors of node_i : {0}'.format(neighbors))

        #Select random neighbor.
        node_j = self.get_random_choice(neighbors)
        
        if verbose:
            print('Selected node_j : {0}'.format(node_j))

        #copy the list of nodes with the same opinion as node_i
        nodes_with_gi = deepcopy(self.node_with_opinion[opinion_gi])
        
        if self.simple_graph: #if it is a simple graph, exclude the neighbours and itself from the possible new acquaintances
            exclude_list = deepcopy(neighbors)
            exclude_list.append(node_i)
            nodes_with_gi = [e for e in nodes_with_gi if e not in exclude_list]
            if len(nodes_with_gi)==0: #if impossible to have new acquaintance, do nothing
                return
        else:
            if len(nodes_with_gi)==1: #if it is a multi-graph and there is only one node with the same opinion (i.e. itself), do nothing
                return
            nodes_with_gi.remove(node_i) #if it is a multi-graph remove itself from the possible new acquaintances
        
        if verbose:
            print('Nodes with opinion g_i : {0}'.format(nodes_with_gi))

        #Select randomly the new aquaintance
        node_j_prime = self.get_random_choice(nodes_with_gi)

        if verbose:
            print('Selected node_j_prime : {0}'.format(node_j_prime))
            
        #remove the 'old' edge
        self.internal_graph.remove_edge(node_i, node_j)
        #add the 'new' edge
        self.internal_graph.add_edge(node_i, node_j_prime)
        if verbose:
            print('Edge moved from ({0},{1}) to ({0},{2})'.format(node_i, node_j, node_j_prime))

        #update local consensus
        if self.simple_graph:
            neighOp = self.internal_graph.node[node_j]['opinion']
            if neighOp != opinion_gi:
                self.conL[node_i] -= 1
                self.conL[node_j] -= 1
        else: #if it is a multi-graph, there can be multi-edges between nodes, hence deleting one does not affect the local-consensus in the same way as it does for a simple graph. The only way is to recompute fully the local consensus.
            neighbors.remove(node_j)
            self.conL[node_i] = self.localConsensus(opinion_gi, neighbors)
            self.conL[node_j] = self.localConsensus(opinion_gi, list(self.internal_graph.neighbors(node_j)))
        return

       
    def Step2(self, node_i, verbose):
        """
        Perform the Step 2 of the Holme-Newman model. It represents the influence of acquaintances on one another; opinions becoming similar as a result of acquaintance. The opinion of $node_i$ is changed to the one of a randomly selected neighbour.

        Parameters
        ----------
        node_i : int
            the node on which Step 2 is performed 
        verbose : bool
            if it is True, prints detailed information about the step

        Returns
        -------
        Nothing
        """
        #If all the neighbours of node_i have the same opinion as node_i do nothing
        if self.conL[node_i]==0:
            return

        #store opinion of node_i before the step
        previous_opinion = self.internal_graph.node[node_i]['opinion']
        
        #Compute neighbours of node_i (can have itself, and many occurence of same neighbour if it is a multi-graph)
        neighbors = list(self.internal_graph.neighbors(node_i))

        if verbose:
            print('Neighbors of node_i : {0}'.format(neighbors))

        #Select random neighbour. If no neighbour do nothing
        if len(neighbors)==0:
            return #If no neighbour do nothing
        else:
            node_j = self.get_random_choice(neighbors)
            
        if verbose:
            print('Selected node_j : {0}'.format(node_j))

        #Change opinion of node_i to the one of node_j
        new_opinion = self.internal_graph.node[node_j]['opinion']
        
        #if new opinion different from previous, update the internal_graph and the bookkeping of local consensus
        if new_opinion!=previous_opinion:       
            self.internal_graph.node[node_i]['opinion'] = new_opinion

            #update opinion list
            self.node_with_opinion[previous_opinion].remove(node_i)
            self.node_with_opinion[new_opinion].append(node_i)

            #update local consensus of node_i
            self.conL[node_i] = self.localConsensus(new_opinion,neighbors)
            
            #update local consensus of neighbours of node_i
            for neigh in neighbors:
                neighOp = self.internal_graph.node[neigh]['opinion']
                if neighOp!=previous_opinion:
                    self.conL[neigh]-=1                   
                if neighOp!=new_opinion:
                    self.conL[neigh]+=1

            if verbose:
                print('Opinion of node {0} changed from {1} to {2}'.format(node_i, previous_opinion, self.internal_graph.node[node_i]['opinion']))

        return 
    
def CreateRandom(n, m, n_opinion=None, simple_graph=False, seed=None):
    """
    Creates an OpinionGraph with an interal graph which is a $G_{n,m}$ random graph, with $n_opinions$ randomly assigned.

    In the $G_{n,m}$ model, a graph is chosen uniformly at random from the set
    of all graphs with $n$ nodes and $m$ edges.

    Parameters
    ----------
    n : int
        The number of nodes.
    m : int
        The number of edges.
    n_opinion : int, optional
        The number of opinions (default=None, which gives n_opinion=n).
    simple_graph : bool, optional
        True if the graph is simple (default=None).
    seed : int, optional
        Seed for random number generator (default=None).
    
    Returns
    -------
    G : OpinionGraph
    """
    
    internal_graph = nx.gnm_random_graph(n, m)

    if not simple_graph:
        internal_graph = nx.MultiGraph(internal_graph)
        
    graph = OpinionGraph(internal_graph, n_opinion, simple_graph)
    return graph

def CreateBarbasiAlbert(n, m, n_opinion=None, simple_graph=False, seed=None):
    """
    Creates an OpinionGraph with an interal graph which is a random graph according to the Barabási–Albert preferential
    attachment model.

    A graph of $n$ nodes is grown by attaching new nodes each with $m$
    edges that are preferentially attached to existing nodes with high degree.

    Parameters
    ----------
    n : int
        Number of nodes
    m : int
        Number of edges to attach from a new node to existing nodes
    n_opinion : int, optional
        The number of opinions (default=None, which gives n_opinion=n).
    simple_graph : bool, optional
        True if the graph is simple (default=None).
    seed : int, optional
        Seed for random number generator (default=None).

    Returns
    -------
    G : OpinionGraph
    """
    internal_graph = nx.barabasi_albert_graph(n, m, seed)

    if not simple_graph:
        internal_graph = nx.MultiGraph(internal_graph)
        
    graph = OpinionGraph(internal_graph, n_opinion, simple_graph)
    return graph

def CreateNewmanWattsStrogatz(n, k, p, n_opinion=None, simple_graph=False, seed=None):
    """
    Creates an OpinionGraph with an interal graph which is a Newman–Watts–Strogatz small-world graph.

    Parameters
    ----------
    n : int
        The number of nodes.
    k : int
        Each node is joined with its `k` nearest neighbors in a ring
        topology.
    p : float
        The probability of adding a new edge for each edge.
    n_opinion : int, optional
        The number of opinions (default=None, which gives n_opinion=n).
    simple_graph : bool, optional
        True if the graph is simple (default=None).
    seed : int, optional
        The seed for the random number generator (the default is None).
        
    Returns
    -------
    G : OpinionGraph
    """
    
    internal_graph = nx.newman_watts_strogatz_graph(n, k, p, seed)

    if not simple_graph:
        internal_graph = nx.MultiGraph(internal_graph)
        
    graph = OpinionGraph(internal_graph, n_opinion, simple_graph)
    return graph

def CreatePowerlawCluster(n, m, p, n_opinion=None, simple_graph=False, seed=None):
    """
    Creates an OpinionGraph with an interal graph using the Holme and Kim algorithm for growing graphs with powerlaw
    degree distribution and approximate average clustering.

    Parameters
    ----------
    n : int
        the number of nodes
    m : int
        the number of random edges to add for each new node
    p : float,
        Probability of adding a triangle after adding a random edge
    n_opinion : int, optional
        The number of opinions (default=None, which gives n_opinion=n).
    simple_graph : bool, optional
        True if the graph is simple (default=None).
    seed : int, optional
        Seed for random number generator (default=None).
        
    Returns
    -------
    G : OpinionGraph
    """
    
    internal_graph = nx.powerlaw_cluster_graph(n, m, p, seed)

    if not simple_graph:
        internal_graph = nx.MultiGraph(internal_graph)
        
    graph = OpinionGraph(internal_graph, n_opinion, simple_graph)
    return graph

