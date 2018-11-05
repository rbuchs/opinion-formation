#Import the relevant modules
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import yaml
import time
import sys 


def main():
    global_t0 = time.time()
    
    n = 3200
    m = 6400
    gamma = 10
    n_opinion = int(n/gamma)
    output_path = '/cluster/home/buchsr/output'
    
    print('----------- Graph, n={0}, m={1}, gamma={2} ------------'.format(m,n,gamma))
    print('Phi={0}'.format(phi))
    
    n_steps = []
    components_number = np.array([])
    for i in range(n_iter):
        log(global_t0, '******** N_ITER {0} *******'.format(i))
        G = OpinionGraph.CreateRandom(n, m, n_opinion)
        log(global_t0, 'Random graph created')
        # Number of components
        print('Components counter', OpinionGraph.CountComponents(G))
        print('Percentage nodes in componenets in consensus state', OpinionGraph.PercentageNodesConsensusState(G))
        n_steps.append(SimulationEndConsensus(G, phi))
        comp = OpinionGraph.CountComponents(current_graph)
        print('Components', comp)
        comp = dict(comp)
        print('All component in consensus state: ', np.array(OpinionGraph.ConsensusState(current_graph)).all())
        components_num = np.zeros(2000)
        components_num[list(comp.keys())] = list(comp.values())
        components_number = np.concatenate((components_number, components_num), axis=1)
    
    n_steps = np.array(n_steps)
    np.save('{0}/n_steps_phi{1}.npy'.format(output_path, phi), n_steps)
    np.save('{0}/componenents_number_phi{1}.npy'.format(output_path, phi), components_number)
    
    
if __name__ == '__main__':
    
    phi = sys.argv[1]
    n_iter = sys.argv[2]
    
    #cfgfile = sys.argv[1]
    #with open(cfgfile, 'r') as fp:
    #    cfg = yaml.load(fp)
    
    main()

def log(t0, text):
    print('GLOBAL:', time.time()-t0, text)