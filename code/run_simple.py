#Import the relevant modules
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import yaml
import time
import sys

import OpinionGraph
import OpinionAlgorithm

def log(t0, text):
    print('GLOBAL:', time.time()-t0, text)

def main():
    global_t0 = time.time()
    
    verbose = False
    n = 3200
    m = 6400
    gamma = 10
    n_opinion = int(n/gamma)
    #output_path = '/cluster/home/buchsr/output'
    output_path = '/Users/romainbuchs/Documents/ETHZ/Modelling and Simulating Social Systems/output'
    
    print('----------- Graph, n={0}, m={1}, gamma={2} ------------'.format(m,n,gamma))
    print('----------------------- Phi={0} -----------------------'.format(phi))
    
    #Create random graph
    G = OpinionGraph.CreateRandom(n, m, n_opinion)
    log(global_t0, 'Random graph created')
    # Summary
    G.summary()
    #iterate
    n_steps = OpinionAlgorithm.SimulationEndConsensus(G, phi, verbose=verbose, checkconsensus=1)
    log(global_t0, 'Consensus found')
    # Summary
    G.summary()
    
    comp = G.CountComponents()
    comp = dict(comp)
    
    components_num = np.zeros(n)
    components_num[list(comp.keys())] = list(comp.values())
    
    np.save('{0}/RunSimple_phi{1}.npy'.format(output_path, phi), components_num)

if __name__ == '__main__':
    
    phi = float(sys.argv[1])
    
    main()

