#BSUB -J "Opinion-formation-fig2-[1-3]"
#BSUB -oo '/cluster/home/buchsr/output/OpinionFormation_fig2_%I.log'
#BSUB -n 10

mpirun python /cluster/home/buchsr/opinion-formation/code/run_mpi.py /cluster/home/buchsr/opinion-formation/cfg_files/Run_fig2_n500_m1000_gamma10_niter100_${LSB_JOBINDEX}.cfg
