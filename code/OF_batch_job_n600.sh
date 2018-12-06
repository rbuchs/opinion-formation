#BSUB -J "Opinion-formation-fig3-batch-n600-[1-101]%30"
#BSUB -oo '/cluster/home/buchsr/output/OpinionFormation_fig3_batch_n600_%I.log'
#BSUB -n 20
#BSUB -W 4:00

mpirun python /cluster/home/buchsr/opinion-formation/code/run_mpi.py /cluster/home/buchsr/opinion-formation/cfg_files/Run_fig3_n600_m1200_gamma10_${LSB_JOBINDEX}.cfg 1000
