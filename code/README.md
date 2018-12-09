# Code Folder 

The Holme-Newman model of opinion dynamics is implemented in `OpinionGraph.py` and in `OpinionAlgorithm.py`. The script used to produce the results presented in the report are `run_mpi.py`and `run_mpi_scalefree.py`. Those scripts are called by shell scripts that can be submitted to the batch farm with different configurations. The configuration files used are located in the `/cfg_files` folder. 

The notebooks `Fig2.ipynb` and `Fig3.ipynb` are used to reproduce Figures 2 and 3, respectively, of the Holme and Newman (2006) paper. `Scale-free_network.ipynb`is used to produce the figures for scale-free graphs. `Topologies.ipynb` shows the different initial topologies that an `OpinionGraph` can have. The `Test*.ipynb` files contain various tests, on the global functioning of the model implementation and on speed.   
