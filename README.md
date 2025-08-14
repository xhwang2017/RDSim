# RDSim
# Introduction
RDSim is a Python package designed to simulate the genotypes and phenotypes of rare disease patients. This package can be used by researchers and students to generate synthetic data for facilitating the evaluation of tools aimed at identifying the causal genes or mutations of rare diseases. 

For genotype simulation, the process begins by simulating genotypes for a specified number of individuals using the 1000 Genomes Project Phase I as the reference dataset, employing tools such as HapGen2 and PLINK. Subsequently, rare disease mutations are identified using the ClinVar and Orphanet databases. After that, an additional mutation is introduced into one of these individuals to generate the simulated genotypes for rare disease patients.

For phenotype simulation, HPO terms related to rare diseases, along with the complete set of HPO terms, are selected from the HPO database. Three scenarios can then be simulated for HPO term selection: using all HPO terms associated with the disease, randomly choosing n HPO terms related to rare diseases, or adding m HPO terms from the entire HPO database to introduce some noise.

Additionally, this simulation tool can be used to simulate rare diseases for specific populations, including European (EUR), Asian (ASN), and African American (AFR).
# RDSim Process
<img width="1417" alt="Screenshot 2025-01-17 at 11 12 07 AM" src="https://github.com/user-attachments/assets/79ed0938-f23e-4063-9d3a-ffce0e8a804d" />

# Functions
**1) Case-based simulation:** The simulation covers 1,508 rare diseases, including 694 autosomal dominant (AD) and 814 autosomal recessive (AR) conditions. Each rare disease patient has a mutation associated with a specific rare disease.

**2) Pair-based simulation:**  This allows for simulating 1,297 pairs of rare diseases (592 AD and 705 AR). Each pair is assigned the same Orphanet Code, with an associated variant added for each patient. In other words, the two patients in one pair will have different variants, all of which are causal for the disease. This simulated data can be used to match similar patients and identify genes associated with those matches.

**3) Pathway-based simlation:** This allows the simulation of 736 pathway-based rare diseases (342 AD and 394 AR). Each rare disease involves three patients: two as in the pair simulations, and a third who has a mutation in a gene within the same pathway as the causal gene. This approach can be used to match similar patients and identify new mutations in different genes associated with a disease.

# Installation
Before you can use the tool, you need to make sure you have the required dependencies installed:

- Python (3.6 or higher)
- NumPy
- Pandas
- HapGen2
- PLINK

HapGen2 installation link: (https://mathgen.stats.ox.ac.uk/genetics_software/hapgen/hapgen2.html)

PLINK isntallation link: (https://www.cog-genomics.org/plink/2.0/)

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

### Step 2: Dertemine the simulation type to generate causative variants
1) Case-based simulation
   
For example, simulating 50 individuals, including 20 with autosomal dominant (AD) rare diseases, 20 with autosomal recessive (AR) rare diseases, and the remaining 10 serving as healthy controls.
```bash
python case_genotypes.py --n 20 --m --i 10
```
- `--n`: Number of AD
- `--m`: Number of AR
- `--i`: Number of case controls

The output fils of this command:

- `case_variants.txt`: Contains the simulated causative variants for each sample.
- `case_chrom_pos.txt`: Contains the chromosome and position information for the causative variants.
- `case_genes.csv`: Contains the simulated causative genes for each sample.

2) Pairs-based simulation
   
For example, simulating 40 individuals, including 10 pairs with autosomal dominant (AD) rare diseases and 10 pairs with autosomal recessive (AR) rare diseases.
```bash
python pairs_genotypes.py --n 20 --m 
```
- `--n`: Number of AD
- `--m`: Number of AR

The output fils of this command:

- `pairs_variants.txt`: Contains the simulated causative variants for each sample.
- `pairs_chrom_pos.txt`: Contains the chromosome and position information for the causative variants.
- `pairs_genes.csv`: Contains the simulated causative genes for each sample.

3) Pathway-based simulation
   
For example, simulating 60 individuals, including 30 with autosomal dominant (AD) rare diseases and 30 with autosomal recessive (AR) rare diseases.
```bash
python pairs_genotypes.py --n 30 --m 30
```
- `--n`: Number of AD
- `--m`: Number of AR

The output fils of this command:

- `pathway_variants.txt`: Contains the simulated causative variants for each sample.
- `pathway_chrom_pos.txt`: Contains the chromosome and position information for the causative variants.
- `pathway_genes.csv`: Contains the simulated causative genes for each sample.

### Sept 3: Add causative variants into the simulated genotypes

```bash
# For case-based simulation
./rd_sim.sh --chrom_pos case_chrom_pos.txt --input eur_genome --variants case_variants.txt --output case_genotypes.vcf
# For pairs-based simulation
./rd_sim.sh --chrom_pos pairs_chrom_pos.txt --input eur_genome --variants pairs_variants.txt --output pairs_genotypes.vcf
# For case-based simulation
./rd_sim.sh --chrom_pos pathway_chrom_pos.txt --input eur_genome --variants pathway_variants.txt --output pathway_genotypes.vcf
```
- `--chrom_pos`: The chromosome and position information for the causative variants.
- `--input`: The simulated genotypes through Hapgen2
- `--variants`: The simulated causative genes for each sample
- `--output`: The simulated genetypes for rare diseases

## Phenotype simulations
For the phenotype simulation, HPO terms related to rare diseases, along with the complete set of HPO terms, are selected from the HPO database. Three scenarios can then be simulated for HPO term selection: 

(1) Using all HPO terms associated with the disease

(2) Randomly choosing i rare disease-related HPO terms

(3) N rare disease-related HPO terms adding m HPO terms from the entire HPO database to introduce some noise.

```bash
# For case-based simulation
case_phenotypes.py --n 20 --m 20 --hpo_i 5 --hpo_n 3 --hpo_m 2
# For pairs-based simulation
pairs_phenotypes.py --n 20 --m 20 --hpo_i 5 --hpo_n 3 --hpo_m 2
# For case-based simulation
pathway_phenotyes.py --n 30 --m 30 --hpo_i 5 --hpo_n 3 --hpo_m 2
```
- `--n`: Number of AD
- `--m`: Number of AR
- `--hpo_i`: Number of rare disease-related HPO terms simulating scenarios (2) randomly choosing i rare disease-related HPO terms.
- `--hpo_n`: Number of rare disease-related HPO terms simulating scenarios (3) n rare disease-related HPO terms adding m HPO terms from the entire HPO database to introduce some noise.
- `--hpo_m`: Number of rare disease-unrelated HPO terms simulating scenarios (3) n rare disease-related HPO terms adding m HPO terms from the entire HPO database to introduce some noise.

The output fils of this command:
For case-based simulation
- `case_phenotypes.csv`: Contains the rare diseases and hpo information for each sample.
- `case_hpo.csv`: Contains the simulated HPO terms of three scenarios for each sample.
For pairs-based simulation
- `pairs_phenotypes.csv`: Contains the rare diseases and hpo information for each sample.
- `pairs_hpo.csv`: Contains the simulated HPO terms of three scenarios for each sample.
For pathway-based simulation
- `pathway_phenotypes.csv`: Contains the rare diseases and hpo information for each sample.
- `pathway_hpo.csv`: Contains the simulated HPO terms of three scenarios for each sample.

# License
This project is licensed under the MIT License. See the LICENSE file for details.
