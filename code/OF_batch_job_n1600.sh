#BSUB -J "Opinion-formation-fig3-batch-n1600-[1-101]%30"
#BSUB -oo '/cluster/home/buchsr/output/OpinionFormation_fig3_batch_n1600_%I.log'
#BSUB -n 20
#BSUB -W 24:00

mpirun python /cluster/home/buchsr/opinion-formation/code/run_mpi.py /cluster/home/buchsr/opinion-formation/cfg_files/Run_fig3_n1600_m3200_gamma10_${LSB_JOBINDEX}.cfg 20
