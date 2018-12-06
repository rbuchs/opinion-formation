#BSUB -J "Opinion-formation-fig3-batch-n400-[1-101]%30"
#BSUB -oo '/cluster/home/buchsr/output/OpinionFormation_fig3_batch_n400_%I.log'
#BSUB -n 10
#BSUB -W 150

mpirun python /cluster/home/buchsr/opinion-formation/code/run_mpi.py /cluster/home/buchsr/opinion-formation/cfg_files/Run_fig3_n400_m800_gamma10_${LSB_JOBINDEX}.cfg 1000
