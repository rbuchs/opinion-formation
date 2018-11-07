from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD   # Defines the default communicator
size = comm.Get_size()  # Stores the number of processes in size.
rank = comm.Get_rank()  # Stores the rank (pid) of the current process

phi = np.linspace(0,100,1000)
print("Rank {0} assigned {1} files".format(rank, len(phi[rank::size])))
print(phi[rank::size])