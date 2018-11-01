#BSUB -q medium
#BSUB -W 10
#BSUB -J "Opinion-formation-phi0"
#BSUB -oo //cluster/home/buchsr/output/Opinion-formation-phi0.log

python /cluster/home/buchsr/opinion-formation/code/run.py 0 10