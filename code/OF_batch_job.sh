#BSUB -J "Opinion-formation-phi0.96"
#BSUB -oo '/cluster/home/buchsr/output/OpinionFormation_phi0.04.log'
#BSUB -n 10

mpirun python /cluster/home/buchsr/opinion-formation/code/run_mpi.py 0.96 1000
