# RDSim
# Introduction
RDSim is a Python package designed to simulate the genotypes and phenotypes of rare disease patients. This package can be used by researchers and students to generate synthetic data for facilitating the evaluation of tools aimed at identifying the causal genes or mutations of rare diseases. 

For genotype simulation, the process begins by simulating genotypes for a specified number of individuals using the 1000 Genomes Project Phase I as the reference dataset, employing tools such as HapGen2 and PLINK. Subsequently, rare disease mutations are identified using the ClinVar and Orphanet databases. After that, an additional mutation is introduced into one of these individuals to generate the simulated genotypes for rare disease patients.

For phenotype simulation, HPO terms related to rare diseases, along with the complete set of HPO terms, are selected from the HPO database. Three scenarios can then be simulated for HPO term selection: using all HPO terms associated with the disease, randomly choosing n HPO terms related to rare diseases, or adding m HPO terms from the entire HPO database to introduce some noise.

Additionally, this simulation tool can be used to simulate rare diseases for specific populations, including European (EUR), Asian (ASN), and African American (AFR).

# Functions
**1) Case-based simulation:** The simulation covers 1,508 rare diseases, including 694 autosomal dominant (AD) and 814 autosomal recessive (AR) conditions. Each rare disease patient has a mutation associated with a specific rare disease.

**2) Pair-based simulation:**  This allows for simulating 1,297 pairs of rare diseases (705 AD and 592 AR). Each pair is assigned the same Orphanet Code, with an associated variant added for each patient. In other words, the two patients in one pair will have different variants, all of which are causal for the disease. This simulated data can be used to match similar patients and identify genes associated with those matches.

**3) Pathway-based simlation:** This allows the simulation of 736 pathway-based rare diseases (342 AD and 396 AR). Each rare disease involves three patients: two as in the pair simulations, and a third who has a mutation in a gene within the same pathway as the causal gene. This approach can be used to match similar patients and identify new mutations in different genes associated with a disease.

# Installation
Before you can use the tool, you need to make sure you have the required dependencies installed:

- Python (3.6 or higher)
- NumPy
- Pandas
- HapGen2
- PLINK

Install via pip:

```bash
pip install git+https://github.com/xhwang2017/RDSim.git
```

Alternatively, you can clone the repository and install it locally:

```bash
git clone https://github.com/xhwang2017/RDSim.git
cd RDSim
pip install .
```

# Usage
To use the RDSim Simulation Tool, follow these steps:

1. Open your terminal or command prompt.

2. Navigate to the `src` directory containing the python and bash script.

3. Run the script with the desired command-line arguments (explained below).

## Example Usage
1. Simulation of European population genotypes (e.g., simulating 2,000 European individuals)
```bash
./eur_sim.sh --n 2000
```
- `--n`: The number of simulated individuals.
 

# License
This project is licensed under the MIT License. See the LICENSE file for details.
