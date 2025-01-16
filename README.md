# RDSim
# Introduction
RDSim is a Python package designed to simulate the genotypes and phenotypes of rare disease patients. This package can be used by researchers and students to generate synthetic data for facilitating the evaluation of tools aimed at identifying the causal genes or mutations of rare diseases. 

For genotype simulation, the process begins by simulating genotypes for a specified number of individuals using the 1000 Genomes Project Phase I as the reference dataset, employing tools such as HapGen2 and PLINK. Subsequently, rare disease mutations are identified using the ClinVar and Orphanet databases. After that, an additional mutation is introduced into one of these individuals to generate the simulated genotypes for rare disease patients.

For the phenotype simulation, HPO terms related to rare diseases, along with the complete set of HPO terms, are selected from the HPO database. Three scenarios can then be simulated for HPO term selection: using all HPO terms associated with the disease, randomly choosing n HPO terms related to rare diseases, or adding m HPO terms from the entire HPO database to introduce some noise.

# Functions
1) Case-based simulation: 
2) Pair-based simulation: 
3) Pathway-based simlation: 

# Installation
To install RDSim, you’ll need Python 3.6 or higher. Install via pip:

bash\
Copy code\
pip install git+https://github.com/xhwang2017/RDSim.git

Alternatively, you can clone the repository and install it locally:

bash\
Copy code\
git clone https://github.com/xhwang2017/RDSim.git
cd RDSim\
pip install .

# Usage
After installation, you can start using the package to simulate genotype and phenotype data for rare disease patients.

# Example Usage

# License
This project is licensed under the MIT License. See the LICENSE file for details.
