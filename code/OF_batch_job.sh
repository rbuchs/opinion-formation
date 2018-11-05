#BSUB -W 100
#BSUB -J "Opinion-formation-phi0"
#BSUB -oo //cluster/home/buchsr/output/Opinion-formation-phi0.04.log

python /cluster/home/buchsr/opinion-formation/code/run.py 0.04 10
