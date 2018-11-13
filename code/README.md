# Code Folder 

We can use this place to write comment about the progress of the work 

28.10.18 Romain 

I have implemented a function that does the simulation while all the components are not in consensus.
That seems to work well when phi is 1 but not when phi is 0. It might just be a problem of number of time steps. Though it seems to need a huge number of it.

30.10.18

The code seems to work. Should now send with various phi and graphs to cluster to replicate paper results

01.11.18 Romain

Submittin job on cluster works. But takes way too much time

05.11.18 Romain

Apparently the code takes a lot of time. Some quatties are computed in `Speed_test.ipynb`. The bottleneck is the evaluation of the consensus state but even without that it is too slow if we want to average over 10^4 iterations...

13.11.18 Romain

Phi=0.04: more than 8h....
Phi=0.458: 5000-9800 sec per realization of n=3200, m=6400 (one realization run on one node)
Phi=0.96: 500-1000 sec per realization of n=3200, m=6400 (one realization run on one node)
