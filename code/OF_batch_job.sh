#BSUB -J "Opinion-formation-phi0"
#BSUB -oo 

module load python/3.6.1
module load open
python /cluster/home/buchsr/opinion-formation/code/run.py 0.04 10
