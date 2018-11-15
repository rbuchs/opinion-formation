#BSUB -J "Opinion-formation-fig2-[1-3]"
#BSUB -oo '/cluster/home/buchsr/output/OpinionFormation_fig2_%I.log'
#BSUB -n 10
#BSUB -W

mpirun python /cluster/home/buchsr/opinion-formation/code/run_mpi.py /cluster/home/buchsr/opinion-formation/cfg_files/Run_fig2_n3200_m6400_gamma10_${LSB_JOBINDEX}.cfg 10
