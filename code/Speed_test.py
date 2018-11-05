{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Measure time to run the algorithm"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Import the relevant modules\n",
    "import networkx as nx\n",
    "import matplotlib.pyplot as plt\n",
    "import numpy as np\n",
    "import time \n",
    "\n",
    "import OpinionGraph\n",
    "import OpinionAlgorithm"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "n = 3200\n",
    "m = 6400\n",
    "gamma = 10\n",
    "n_opinion = int(n/gamma)\n",
    "G = OpinionGraph.CreateRandom(n, m, n_opinion)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "68.1 ms ± 538 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)\n"
     ]
    }
   ],
   "source": [
    "#Create random graph\n",
    "%timeit G = OpinionGraph.CreateRandom(n, m, n_opinion)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Case $\\phi=0$"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "phi=0"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "305 µs ± 9.6 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)\n"
     ]
    }
   ],
   "source": [
    "%timeit OpinionAlgorithm.OneStep(G,phi)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {
    "scrolled": false
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "302 µs ± 5.6 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)\n"
     ]
    }
   ],
   "source": [
    "%timeit OpinionAlgorithm.Simulation(G, phi, 1)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Case $\\phi=1$"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "phi=1"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "570 µs ± 14 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)\n"
     ]
    }
   ],
   "source": [
    "%timeit OpinionAlgorithm.OneStep(G,phi)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "571 µs ± 26.6 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)\n"
     ]
    }
   ],
   "source": [
    "%timeit OpinionAlgorithm.Simulation(G, phi, 1)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Overal computation time\n",
    "If $\\phi=1$, for a graph with $N =3200$, we expect $\\tau=24$ where $\\tau$ is the number of updates per vertex needed to reach consensus. Thus, would need $24\\cdot3200=76800$ steps."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [],
   "source": [
    "OneStepTime = (302e-6 + 571e-6)/2\n",
    "NStep = 76800\n",
    "Totat_time = OneStepTime*NStep"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "This should take (in sec)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "33.5232"
      ]
     },
     "execution_count": 14,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "Totat_time"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
