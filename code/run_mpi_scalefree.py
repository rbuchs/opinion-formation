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
    #output_path = '/Users/romainbuchs/Documents/ETHZ/Modelling and Simulating Social Systems/output'
    #scratch_path = '/Users/romainbuchs/Documents/ETHZ/Modelling and Simulating Social Systems/scratch'
    output_path = '/cluster/home/buchsr/output'
    scratch_path = '/scratch/buchsr'
    
    if rank==0:
        print('----------- Graph, n={0}, m={1}, gamma={2} ------------'.format(m,n,gamma))
        print('----------------------- Phi={0} -----------------------'.format(phi))
        print('We will perform {0} iterations'.format(n_iter))
        if not os.path.exists(scratch_path):
            os.makedirs(scratch_path)
    
    iterations = np.arange(n_iter)
    print("Rank {0} assigned {1} iterations".format(rank, len(iterations[rank::size])))
    
    for i in iterations[rank::size]:
        initial_clustering = []
        final_clustering = []
        for p_value in p:
            #Create random graph
            G = OpinionGraph.CreatePowerlawCluster(n, m, p_value, n_opinion, True)
            initial_clustering.append(G.average_clustering())
            if verbose:
                log(global_t0, 'Random graph created')
                G.summary()
            #iterate
            n_steps = OpinionAlgorithm.SimulationEndConsensus(G, phi, verbose=False, checkconsensus=1000)
            if verbose:
                log(global_t0, 'Consensus found')
                G.summary()
                
            final_clustering.append(G.average_clustering())
            comp = G.CountComponents()
            comp = dict(comp)

            components_num = np.zeros(n+1)
            components_num[list(comp.keys())] = list(comp.values())
            np.save('{0}/ComponentsSize_{3}_phi_{1}_{4}_{2}.npy'.format(scratch_path, phi, i, tag, p_value), components_num)
        
        np.save('{0}/Initial_clustering_{3}_phi_{1}_{2}.npy'.format(scratch_path, phi, i, tag), np.array(initial_clustering)) 
        np.save('{0}/Final_clustering_{3}_phi_{1}_{2}.npy'.format(scratch_path, phi, i, tag), np.array(final_clustering))
    
    comm.Barrier()
    if rank==0:
        initial_clustering = []
        final_clustering = []
        for i in range(n_iter):
            initial_clustering.append(np.load('{0}/Initial_clustering_{3}_phi_{1}_{2}.npy'.format(scratch_path, phi, i, tag)))
            final_clustering.append(np.load('{0}/Final_clustering_{3}_phi_{1}_{2}.npy'.format(scratch_path, phi, i, tag)))   
        np.save('{0}/Initial_clustering_{1}_n{2}_m{3}_gamma{4}_niter{5}_phi_{6}.npy'.format(output_path, tag, n, m, gamma, n_iter, phi), np.array(initial_clustering))
        np.save('{0}/Final_clustering_{1}_n{2}_m{3}_gamma{4}_niter{5}_phi_{6}.npy'.format(output_path, tag, n, m, gamma, n_iter, phi), np.array(final_clustering))

        
        for p_value in p:
            all_results = []
            for i in range(n_iter):
                all_results.append(np.load('{0}/ComponentsSize_{3}_phi_{1}_{4}_{2}.npy'.format(scratch_path, phi, i, tag, p_value)))   
            all_results = np.array(all_results)

            np.save('{0}/ComponentsSize_{1}_n{2}_m{3}_gamma{4}_niter{5}_p_{7}_phi_{6}.npy'.format(output_path, tag, n, m, gamma, n_iter, phi, p_value), all_results)

        try:
            shutil.rmtree(scratch_path)
        except OSError as e:
            print ("Error: {0} - {1}.".format(e.filename, e.strerror))

        log(global_t0, '************ Job completed ************')

if __name__ == '__main__':
    
    verbose = True
    #p = np.arange(0,1.2, 0.2)
    p = [0.2]
    
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

