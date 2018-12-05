#BSUB -J "Opinion-formation-scalefree-n200-[1-101]%30"
#BSUB -oo '/cluster/home/buchsr/output/OpinionFormation_scalefree_batch_n200_%I.log'
#BSUB -n 10
#BSUB -W 4:00

mpirun python /cluster/home/buchsr/opinion-formation/code/run_mpi_scalefree.py /cluster/home/buchsr/opinion-formation/cfg_files/Run_scalefree_cluster_n200_m3_gamma10_${LSB_JOBINDEX}.cfg 100
