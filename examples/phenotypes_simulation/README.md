# Phenotypes Simulation
For the phenotype simulation, HPO terms related to rare diseases, along with the complete set of HPO terms, are selected from the HPO database. Three scenarios can then be simulated for HPO term selection: 

(1) Using all HPO terms associated with the disease

(2) Randomly choosing i rare disease-related HPO terms

(3) N rare disease-related HPO terms adding m HPO terms from the entire HPO database to introduce some noise.

## Examples for phenotypes simulation

### For case-based simulation
```bash
./RDSim.sh --case_phenotypes --n 20 --m 20 --hpo_i 5 --hpo_n 3 --hpo_m 2
```
### For pairs-based simulation
```bash
./RDSim.sh --pairs_phenotypes --n 20 --m 20 --hpo_i 5 --hpo_n 3 --hpo_m 2
```

### For case-based simulation
```bash
./RDSim.sh --pathway_phenotyes --n 30 --m 30 --hpo_i 5 --hpo_n 3 --hpo_m 2
```
### Parameters
- `--n`: Number of AD
- `--m`: Number of AR
- `--hpo_i`: Number of rare disease-related HPO terms simulating scenarios (2) randomly choosing i rare disease-related HPO terms.
- `--hpo_n`: Number of rare disease-related HPO terms simulating scenarios (3) n rare disease-related HPO terms adding m HPO terms from the entire HPO database to introduce some noise.
- `--hpo_m`: Number of rare disease-unrelated HPO terms simulating scenarios (3) n rare disease-related HPO terms adding m HPO terms from the entire HPO database to introduce some noise.

### Outputs
For case-based simulation
- `case_phenotypes.csv`: Contains the rare diseases and hpo information for each sample.
- `case_hpo.csv`: Contains the simulated HPO terms of three scenarios for each sample.
For pairs-based simulation
- `pairs_phenotypes.csv`: Contains the rare diseases and hpo information for each sample.
- `pairs_hpo.csv`: Contains the simulated HPO terms of three scenarios for each sample.
For pathway-based simulation
- `pathway_phenotypes.csv`: Contains the rare diseases and hpo information for each sample.
- `pathway_hpo.csv`: Contains the simulated HPO terms of three scenarios for each sample.
