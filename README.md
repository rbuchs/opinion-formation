# Modeling and Simulation of Social Systems Fall 2018

> * Group Name: OpinionFormation
> * Group participants names: Romain Buchs and Nicolas Habisreutinger
> * Project Title: Opinion formation in networks of acquaintances
> * Programming language: Python

The aim of this project is to reproduce the results of Holme and Newman (2006). For details on the project, the model used, the implementation and the results, see `/report/report.pdf`.

*P. Holme and M. E. J. Newman. Nonequilibrium phase transition in the coevolution of networks and opinions. Phys. Rev. E 74, 056108, November 2006*

# Reproducibility

Dependencies: <br>
  * `numpy` <br>
  * `matplotlib` <br>
  * `networkx` <br>

To install any of those packages, run `pip install <package name>`. The two first packages are probably already installed. For more information on the installation of the `networkx` package, see https://networkx.github.io/documentation/stable/install.html.

## Light test

If you want to reproduce a simpler version of our results and get a sense of how the model works and is implemented, do the following:

1. In the terminal, do `git clone https://github.com/rbuchs/opinion-formation.git`

2. If you know what a jupyter notebook is and have it installed, go directly to step 3. If you don't: type `jupyter notebook` in the terminal. If it says `jupyter: command not found`, go to step 2.1.; if some lines containing `The Jupyter Notebook is running at...` appear, go to step 2.2. <br>   
   2.1. To install the jupyter notebook first run `pip install --upgrade pip` to ensure that you have the latest pip and then run `pip install jupyter`. For more information on this installation, see https://jupyter.readthedocs.io/en/latest/install.html. <br>   
   2.2. You have jupyter installed and a notebook is now runing. A window of your browser should have opened. If it is not the case, copy the url that poped-up in the terminal and paste it in a browser. Then open the file located at `/other/Tutorial.ipynb`. <br>
 3. Open a jupyter notebook and open the file located at `/other/Tutorial.ipynb`.

## Full test

The code is set up to run on the ETH euler cluster. The shell scripts used to produce the results presented in the report are located at `/code/OF_batch_job_n#.sh` where`#` should be replaced with the number of nodes. Those script run `/code/run_mpi.py` which takes as first argument a configuration file containing various parameters and as second parameter the number of realizations to perform. The configuration files are located in `/cfg_files`. 

For the results with the scale free graph, the shell script is `/code/OF_batch_job_scalefree.sh` and the structure is similar as the one mention above but the script runs `/code/run_scalefree.py`.
