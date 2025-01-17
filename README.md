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

## Genotype simulations
### Step 1: Determine the total number of individuals to simulate
For example, simulating 50 European individuals.
```bash
./eur_sim.sh --n 50
```
- `--n`: The number of simulated individuals.

This command line generates an output BED file named `eur_genome`, which simulates the whole genome genotypes for chromosomes 1 to 22.

_* The exome genotypes can be generated through the exon_sim.sh function._
```bash
./exom_sim.sh --input eur_genome --output snps_in_exons
```
- `--input`: Specify the PLINK binary file containing the whole genome genotypes.
- `--output`: Specify the filtered PLINK binary file with genotypes in exon regions.

### Step 2: Dertemine the simulation type
1) Case-based simulation
For example, simulating 50 simulating 50 individuals, including 20 with autosomal dominant (AD) rare diseases, 20 with autosomal recessive (AR) rare diseases, and the remaining 10 serving as healthy controls.
```bash
python case_genotypes.py --n 20 --m --i 10
```
- `--n`: Number of AD
- `--m`: Number of AR
- `--i`: Number of case controls

The outputs of this command:

- `case_variants.txt`: Contains the simulated causative variants for each sample.
<img width="991" alt="Screenshot 2025-01-17 at 10 13 28 AM" src="https://github.com/user-attachments/assets/da6ac614-8ee6-48e1-8fd0-cb9cb5ea29f2" />
- `case_chrom_pos.txt`: Contains the chromosome and position information for the causative variants.
<img width="113" alt="Screenshot 2025-01-17 at 10 15 03 AM" src="https://github.com/user-attachments/assets/292909ff-54c1-4a08-b3d0-bba691f324e1" />
- `case_genes.csv`: Contains the simulated causative genes for each sample.
<img width="378" alt="Screenshot 2025-01-17 at 10 15 29 AM" src="https://github.com/user-attachments/assets/b3dc57f5-3e67-48f0-9d85-bfc9f7a18c70" />



# License
This project is licensed under the MIT License. See the LICENSE file for details.
