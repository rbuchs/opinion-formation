import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from copy import deepcopy

#Create a random graph with n_nodes and m_edges. n_opinion is the number of possible opinions, stored in the 
#'opinion' attribut of the node. If not given n_opinion=n_nodes. The opinions are integers in [0, n_opinion]
#The graph can have multiedges and self-loops. Nevertheless, it is created with no multiedges and no self-loops.

class BaseOpinionGraph(object):
    def __init__(self, n_nodes, m_edges, n_opinion=None):
        if n_opinion is None:
            n_opinion = n_nodes
        opinions = np.random.choice(n_opinion, n_nodes)

        internal_graph = nx.gnm_random_graph(n_nodes, m_edges)
        
        # set opiniions
        nx.set_node_attributes(internal_graph, values=dict(zip(range(n_nodes), opinions)), name='opinion')
        
        self.internal_graph = nx.MultiGraph(internal_graph)
        
        self.node_with_opinion=[]
        #Generate opinion lists
        for opinion in range(n_opinion):
            self.node_with_opinion.append([n for n, attr in self.internal_graph.nodes(data=True) if attr['opinion']==opinion])

        #Generate local consensus lists
        self.conL = [12345]*n_nodes
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

    def plot(self, layout=None, axis=False):
        if layout==None:
            layout=nx.spring_layout(self.internal_graph)

        plt.figure()
        op = list(nx.get_node_attributes(self.internal_graph, 'opinion').values())
        ax = nx.draw_networkx(self.internal_graph, pos=layout, with_labels=True, node_color=op, font_color='w')
        if not axis:
            plt.axis('off')

    def Components(self):
        return list(nx.connected_components(self.internal_graph))

    def NComponents(self):
        return len(self.Components())

    def CountComponents(self):
        return Counter([len(comp) for comp in self.Components()])

    def ConsensusState(self, withnodes=False):
        consensus = []
        n_nodes = []
        opinions = np.array(list(nx.get_node_attributes(self.internal_graph, 'opinion').values()))
        for comp in nx.connected_components(self.internal_graph):
            comp_opinions = opinions[list(comp)]
            consensus.append((comp_opinions == comp_opinions[0]).all())
            n_nodes.append(len(comp_opinions))
        if withnodes:
            return np.array(consensus), np.array(n_nodes)
        else:
            return np.array(consensus)
        
    def ConsensusReached(self):
        return sum(self.conL) == 0

    def PercentageNodesConsensusState(self):
        consensus, nodes = self.ConsensusState(withnodes=True)
        return nodes[consensus].sum()/nodes.sum()

    def summary(self):
        # Total number of components
        print('Total number of components: {0}'.format(self.NComponents()))
        #Components size of the graph
        print('Components size: {0}'.format(self.CountComponents()))
        # Bool for consensus state in each component
        print('All components in consensus: {0}'.format(self.ConsensusState().all()))
        print('Consensus reached: {0}'.format(self.ConsensusReached()))
        # percentage nodes in consensus components
        print('Percentage of nodes in components in consensus state: {0}'.format(self.PercentageNodesConsensusState()))
        
    def localConsensus(self, opinion, neighbors, verbose=False): 
        """
        Return the number of entries in 'neighbors' that have a different opinion than 'opinion'$
        
        opinion : opinion of the "central" node
        neighbors : list of neighbouring nodes of the "central" node
        """
    
        lcons = len(neighbors)
        if verbose:
            print("Number of neighbors :", lcons, "; My opinion :", opinion)
        for neigh in neighbors:
            if verbose:
                print("Neighbor ", neigh, "with opinion ", self.internal_graph.node[neigh]['opinion'])
            if self.internal_graph.node[neigh]['opinion'] == opinion:
                lcons-=1
        if verbose:
            print("Final = ", lcons)
        return lcons
    
    #limitations: can form acquaintance with itself or 'double' existing acquaintance
    def Step1(self, node_i, verbose):
        #take opinion of node_i
        opinion_gi = self.internal_graph.nodes[node_i]['opinion']

        #Compute neighbours of node_i (can have itself, and many occurence of same neighbour)
        neighbors = list(self.internal_graph.neighbors(node_i))

        if verbose:
            print('Neighbors of node_i : {0}'.format(neighbors))

        #Select random neighbor. This aquaintance will be deleted. (tend to delete more easily the ''mulit-aquaintances'
        #or multi-self-loop')
        node_j = self.get_random_choice(neighbors)
        if verbose:
            print('Selected node_j : {0}'.format(node_j))

        #expensive
        nodes_with_gi = deepcopy(self.node_with_opinion[opinion_gi])
        if len(nodes_with_gi)==1:
            return
        nodes_with_gi.remove(node_i)

        if verbose:
            print('Nodes with opinion g_i : {0}'.format(nodes_with_gi))

        #Select randomly the new aquaintance
        node_j_prime = self.get_random_choice(nodes_with_gi)

        if verbose:
            print('Selected node_j_prime : {0}'.format(node_j_prime))

        self.internal_graph.remove_edge(node_i, node_j)
        self.internal_graph.add_edge(node_i, node_j_prime)
        if verbose:
            print('Edge moved from ({0},{1}) to ({0},{2})'.format(node_i, node_j, node_j_prime))


        #update local consensus
        neighbors.remove(node_j)
        self.conL[node_i] = self.localConsensus(opinion_gi, neighbors)
        self.conL[node_j] = self.localConsensus(opinion_gi, list(self.internal_graph.neighbors(node_j)))

        return

       
    #Step 2 represents the influence of acquaintances on one another, opinions becoming similar as a result of acquaintance.
    def Step2(self, node_i, verbose):
        if self.conL[node_i]==0:
            return

        previous_opinion = self.internal_graph.node[node_i]['opinion']
        #Compute neighbours of node_i (can have itself, and many occurence of same neighbour)
        neighbors = list(self.internal_graph.neighbors(node_i))

        #filter to remove itself and to keep only the neighbours with different opinion
        #neighbors = [n for n in graph.neighbors(node_i) if (graph.node[n]['opinion']!=previous_opinion and n!=node_i)]
        # Apparently it is even worse if we filter ... never converge
        if verbose:
            print('Neighbors of node_i : {0}'.format(neighbors))

        #Select random neighbor.
        if len(neighbors)==0:
            return 
        else:
            node_j = self.get_random_choice(neighbors)
        if verbose:
            print('Selected node_j : {0}'.format(node_j))

        #Change opinion of node_i to the one of node_j
        new_opinion = self.internal_graph.node[node_j]['opinion']
        if new_opinion!=previous_opinion:       
            self.internal_graph.node[node_i]['opinion'] = new_opinion

            #update opinion list
            self.node_with_opinion[previous_opinion].remove(node_i)
            self.node_with_opinion[new_opinion].append(node_i)

            #update local consensus
            self.conL[node_i] = self.localConsensus(new_opinion,neighbors)

            for neigh in neighbors:
                neighOp = self.internal_graph.node[neigh]['opinion']
                if neighOp!=previous_opinion:
                    self.conL[neigh]-=1                   
                if neighOp!=new_opinion:
                    self.conL[neigh]+=1

            if verbose:
                print('Opinion of node {0} changed from {1} to {2}'.format(node_i, previous_opinion, self.internal_graph.node[node_i]['opinion']))

        return 
    
def CreateRandom(n_nodes, m_edges, n_opinion=None):
    graph = BaseOpinionGraph(n_nodes, m_edges, n_opinion)
    return graph