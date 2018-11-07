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
    
    n = 3200
    m = 6400
    gamma = 10
    n_opinion = int(n/gamma)
    output_path = '/cluster/home/buchsr/output'
    #output_path = '/Users/romainbuchs/Documents/ETHZ/Modelling and Simulating Social Systems/output'
    scratch_path = '/scratch/buchsr'
    
    if rank==0:
        print('----------- Graph, n={0}, m={1}, gamma={2} ------------'.format(m,n,gamma))
        print('----------------------- Phi={0} -----------------------'.format(phi))
        print('We will perform {0} iterations'.format(n_iter))
        os.makedirs(scratch_path)
    
    iterations = np.arange(n_iter)
    print("Rank {0} assigned {1} iterations".format(rank, len(iterations[rank::size])))
    
    for i in iterations[rank::size]:
        #Create random graph
        G = OpinionGraph.CreateRandom(n, m, n_opinion)
        if verbose:
            log(global_t0, 'Random graph created')
            OpinionGraph.summary(G)
        #iterate
        n_steps = OpinionAlgorithm.SimulationEndConsensus(G, phi, verbose=False, checkconsensus=1000)
        if verbose:
            log(global_t0, 'Consensus found')
            OpinionGraph.summary(G)

        comp = OpinionGraph.CountComponents(G)
        comp = dict(comp)

        components_num = np.zeros(n)
        components_num[list(comp.keys())] = list(comp.values())

        np.save('{0}/ComponentsSize_phi_{1}_{2}.npy'.format(scratch_path, phi, i), components_num)
    
    
    
    comm.Barrier()
    if rank==0:
        all_results = []
        for i in range(n_iter):
            all_results.append(np.load('{0}/ComponentsSize_phi_{1}_{2}.npy'.format(scratch_path, phi, i)))   
        all_results = np.array(all_results)
        
        np.save('{0}/ComponentsSize_phi_{1}.npy'.format(output_path, phi), all_results)

        try:
            shutil.rmtree(scratch_path)
        except OSError as e:
            print ("Error: {0} - {1}.".format(e.filename, e.strerror))

        log(global_t0, '************ Job completed ************')

if __name__ == '__main__':
    
    verbose = False
    phi = float(sys.argv[1])
    n_iter = int(sys.argv[2])
    
    main()

