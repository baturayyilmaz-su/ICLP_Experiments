# ICLP_Experiments
This repository contains the necessary files to repeat the experiments that we have conducted for ICLP25 in our paper "Generating Satisfiable Benchmark Instances for Stable Roommates Problems with Optimization". 

Requierements:
* Python 3.12.0
* CLINGO 5.4.0
* JDK 11.0.24

The existing benchmarks are taken directly from: https://github.com/mugefidan/SRTI
The Solvers/ChocoSolver/ is empty. You must download the corresponding solver (SRIToolKit) from: http://www.dcs.gla.ac.uk/˜pat/roommates/distribution/. After you put the "distribution/" folder in "Solvers/ChocoSolver" directory, the experiment script should work.
