#Import the relevant modules
from mpi4py import MPI
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import yaml
import time
import sys, os
import shutil

import OpinionGraph
import OpinionAlgorithm

def log(t0, text):
    print('GLOBAL:', time.time()-t0, text)

def main():
    global_t0 = time.time()
    
    comm = MPI.COMM_WORLD   # Defines the default communicator
    size = comm.Get_size()  # Stores the number of processes in size.
    rank = comm.Get_rank()  # Stores the rank (pid) of the current process
    
    n_opinion = int(n/gamma)
    #output_path = '/cluster/home/buchsr/output'
    output_path = '/Users/romainbuchs/Documents/ETHZ/Modelling and Simulating Social Systems/output'
    scratch_path = '/Users/romainbuchs/Documents/ETHZ/Modelling and Simulating Social Systems/scratch'fca
    #scratch_path = '/scratch/buchsr'
    
    if rank==0:
        print('----------- Graph, n={0}, m={1}, gamma={2} ------------'.format(m,n,gamma))
        print('----------------------- Phi={0} -----------------------'.format(phi))
        print('We will perform {0} iterations'.format(n_iter))
        if not os.path.exists(scratch_path):
            os.makedirs(scratch_path)
    
    iterations = np.arange(n_iter)
    print("Rank {0} assigned {1} iterations".format(rank, len(iterations[rank::size])))
    
    for i in iterations[rank::size]:
        #Create random graph
        G = OpinionGraph.CreateRandom(n, m, n_opinion)
        if verbose:
            log(global_t0, 'Random graph created')
            G.summary()
        #iterate
        n_steps = OpinionAlgorithm.SimulationEndConsensus(G, phi, verbose=False, checkconsensus=1000)
        if verbose:
            log(global_t0, 'Consensus found')
            G.summary()

        comp = G.CountComponents()
        comp = dict(comp)

        components_num = np.zeros(n)
        components_num[list(comp.keys())] = list(comp.values())

        np.save('{0}/ComponentsSize_{3}_phi_{1}_{2}.npy'.format(scratch_path, phi, i, tag), components_num) 
    
    comm.Barrier()
    if rank==0:
        all_results = []
        for i in range(n_iter):
            all_results.append(np.load('{0}/ComponentsSize_{3}_phi_{1}_{2}.npy'.format(scratch_path, phi, i, tag)))   
        all_results = np.array(all_results)
        
        np.save('{0}/ComponentsSize_{1}_n{2}_m{3}_gamma{4}_niter{5}_phi_{6}.npy'.format(output_path, tag, n, m, gamma, n_iter, phi), all_results)

        try:
            shutil.rmtree(scratch_path)
        except OSError as e:
            print ("Error: {0} - {1}.".format(e.filename, e.strerror))

        log(global_t0, '************ Job completed ************')

if __name__ == '__main__':
    
    verbose = True
    
    cfgfile = sys.argv[1]
    n_iter = int(sys.argv[2])
    
    with open(cfgfile, 'r') as fp:
        cfg = yaml.load(fp)
    
    n = int(cfg['n'])
    m = int(cfg['m'])
    gamma = int(cfg['gamma'])
    phi = float(cfg['phi'])
    tag = cfg['tag']
    
    main()

