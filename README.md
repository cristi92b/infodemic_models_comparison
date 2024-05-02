# Results repository for "Evaluation of Intermodel Equivalence for Misinformation Diffusion: Equation vs. Agent-Based Models"

## Introduction

We included 2 cases of the simulation results for 6 misinformation models: SI, SIS, SIR, SIRS, SEIR, SEIRS, detailed in the research paper under review.

## Repositiory contents

This repository contains the results obtained by running the NetLogo ABMs. Please find below the detailed folder structure of this repository:

 * **ABMs** : this folder contains the NetLogo ABM files
 * **ODE scripts** : this folder contains the python scripts used as a reference for the comparison with the ABM models
 * **Results** : this folder contains the actual results in **csv** format
    * **case1_results** : this folder contains the results in csv format for all 6 misinformation models SI, SIS, SIR, SIRS, SEIR and SEIRS
   * **case1_plots** : this folder contains the plots generated using the csv files in **case1_results** folder
    * **case2_results** : this folder contains the results in csv format for all 6 misinformation models SI, SIS, SIR, SIRS, SEIR and SEIRS
   * **case2_plots** : this folder contains the plots generated using the csv files in **case2_results** folder

## Software versions
* [NetLogo 6.3.0](https://ccl.northwestern.edu/netlogo/6.3.0/)
* [Python 3.11](https://www.python.org/downloads/release/python-3110/) , including the following packages:
  * [matplotlib      3.7.1](https://matplotlib.org/3.7.1/index.html)
  * [numpy           1.24.3](https://numpy.org/doc/1.24/index.html)
  * [pandas          2.0.1](https://pandas.pydata.org/pandas-docs/version/2.0.1/index.html)
  * [scikit-learn    1.2.2](https://scikit-learn.org/1.2/)
  * [scipy           1.10.1](https://docs.scipy.org/doc/scipy-1.10.1/index.html)

## NetLogo ABMs

### (1) Simple ABM

The **Simple ABM** includes the logic for all 6 models: SI, SIS, SIR, SIRS, SEIR and SEIRS.

The size of the environment for this ABM is 33 x 33 cells (patches).

### (2) Large ABM

The **Large ABM** follows the same rules as the simple ABM, the only difference between them being the size of the simulation environment.

The size of the environment for this ABM is 99 x 99 cells (patches).

### (3) Enhanced ABM

The **Enhanced ABM** is an enhanced variant of the **Large ABM**, and includes logic for posting and consuming information, and preferential attachment logic.

The size of the environment for this ABM is 99 x 99 cells (patches).

## Simulation parameters

For each of the 6 models we ran all the possible combination of &#946;, &#947;, &#963; and &#958; parameters, with 10 values in [0.1 , 1.0] interval. Please find below the list of all parameter values:

parameter_values = [ 0.1 , 0.2 , 0.3 , 0.4 , 0.5 , 0.6 , 0.7 , 0.8 , 0.9 , 1.0 ]

Please note that not all parameters apply for all models, as shown in the table below.

|              | **SI**             | **SIS**            | **SIR**            | **SIRS**           | **SEIR**           | **SEIRS**          |
|--------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|
| **&#946;**  | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| **&#947;** | :heavy_minus_sign: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| **&#963;** | :heavy_minus_sign: | :heavy_minus_sign: | :heavy_minus_sign: | :heavy_minus_sign: | :heavy_check_mark: | :heavy_check_mark: |
| **&#958;**    | :heavy_minus_sign: | :heavy_minus_sign: | :heavy_minus_sign: | :heavy_check_mark: | ::heavy_minus_sign: | :heavy_check_mark: |

For each parameter combination we ran a NetLogo simulation with simulation time maxtick = 2000.

Therefore, we ran for each of the 3 ABMs:
* 10 simulations for SI model
* 100 simulations for each of SIS and SIR models
* 1000 simulations for each of SIRS and SEIR models
* 10000 simulations for SEIRS model



## Experiment cases

We considered 2 experiment cases and we applied the same simulation parameters as defined in **Simulation parameters** section.
Experiment **case 1** has nonzero S<sub>0</sub> (initial susceptible population) and I<sub>0</sub> (initial infected population) and we used the same values for all 6 models. Experiment **case 2** has nonzero E<sub>0</sub> (initial exposed population) only for models that include exposed population (SEIR and SEIRS), and also has nonzero S<sub>0</sub> (initial susceptible population) and I<sub>0</sub> (initial infected population). We consider R<sub>0</sub> = 0 (zero initial recovered population) for all simulations.

Each result folder contains the XML file with the entire ABM parameter configuration used as an input for NetLogo.

### Experiment case 1 initial conditions

#### Small ABM

S<sub>0</sub> = 100

E<sub>0</sub> = 0

I<sub>0</sub> = 50


#### Large and Enhanced ABMs

S<sub>0</sub> = 900

E<sub>0</sub> = 0

I<sub>0</sub> = 450


### Experiment case 2  initial conditions

#### Small ABM

S<sub>0</sub> = 100

E<sub>0</sub> = 25

I<sub>0</sub> = 25


#### Large and Enhanced ABMs

S<sub>0</sub> = 900

E<sub>0</sub> = 225

I<sub>0</sub> = 225




