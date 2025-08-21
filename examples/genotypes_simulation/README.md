# Genotypes Simulation
To simulate genotypes, we start by generating genotypes for a specified number of individuals using the 1000 Genomes Project Phase 3 (https://ftp-trace.ncbi.nih.gov/1000genomes/ftp/release/20130502/) as the reference dataset, leveraging tools such as ProxyTyper and PLINK. Rare disease mutations are then identified using the ClinVar and Orphanet databases. In total, 1,508 rare diseases were identified, including 694 autosomal dominant (AD) and 814 autosomal recessive (AR) conditions. Additional mutations are introduced into selected individuals to generate simulated genotypes for rare disease patients.

# Step 1: Determine the Number of Individuals to Simulate
RDSim uses ProxyTyper’s resampling function to simulate sample genotypes.
- Reference ProxyTyper Resampling Examples: "https://github.com/harmancilab/ProxyTyper/tree/main/examples/2_Resampling_Panels"
- Ensure ProxyTyper is installed, Installation Guide: "https://github.com/harmancilab/ProxyTyper/tree/main/installation"

## 1. Test ProxyTyper Installation
After installing ProxyTyper, run the following command to verify it is working:

```bash
./ProxyTyper.sh
```
## 2. Simulate Genotypes
Copy `genome_sim.sh` into the same directory as `ProxyTyper.sh`. For example, to simulate 2,000 individuals:

```bash
./genome_sim.sh --n 2000
```
- `--n`: The number of simulated individuals.

This generates a folder `output_vcfs` containing `.vcf.gz` files, e.g., `geno_chr1_unique_resampled.vcf.gz`, simulating whole-genome genotypes for chromosomes 1–22.

# Step 2: Integrate Simulated Genotypes with RDSim
## Option 1: Using Docker
## 1. Build the Docker Image (if not built yet):

```bash
docker build -t rdsim .
```
Ensure Python, PLINK 2, and BCFtools are installed in the image.

## 2. Run the Docker container, naming it `rdsim_container` (if it isn’t already named):

```bash
docker run -it --name rdsim_container rdsim bash
```
This command line is used to open the rdism_container container.
```bash
docker start -ai rdsim_container
```

## 3. Mount Simulated Genotypes into Docker:
Mount all simulated genotype `.vcf.gz` files into the Docker container `rdsim_container`, placing them in the same directory as `RDSim.sh`.

```bash
for f in /path/to/RDSim/output_vcfs/*; do
  docker cp "$f" rdsim_container:/app/script/
done
```
## Option 2: Without Using Docker
Copy the simulated genotypes `.vcf.gz` files into the same directory as `RDSim.sh` in the local folder.

```bash
cp /path/to/RDSim/output_vcfs/* /path/to/RDSim/script
```

# Step 3: Merge Simulated Genotypes for Chromosomes 1–22

## 1. Navigate to the Script Directory

Using Docker
```bash
docker start -ai rdsim_container
cd script
```
## 2. Merge Genotypes Using RDSim

```bash
./RDSim --genome_merge
```
This generates PLINK files (genome.bim, genome.fam, and genome.bed) containing the merged genomic genotypes for all simulated individuals.
The simulated genomic dataset contains 77,818,264 variants.

# Step 4: Extract exome genotypes from the simulated genomic data

```bash
./RDSim.sh --exome_sim --input genome --output exome
```
### Parameters
- `--input`: Specify the PLINK binary file containing the whole genome genotypes.
- `--output`: Specify the filtered PLINK binary file with genotypes in exon regions.
  
### Outputs
This generates PLINK files (exome.bim, exome.fam, and exome.bed) containing the merged exome genotypes for all simulated individuals.
The simulated exome genotypes contains 4,416,858 variants.

# Step 5: Dertemine the simulation type to generate causative variants

## 1. Case-based simulation
The simulation covers 1,508 rare diseases, including 694 autosomal dominant (AD) and 814 autosomal recessive (AR) conditions. Each rare disease patient has a mutation associated with a specific rare disease.

For example, simulating 2000 individuals, including 694 with autosomal dominant (AD) rare diseases, 814 with autosomal recessive (AR) rare diseases, and the remaining 492 serving as healthy controls.

```bash
./RDSim.sh --case_genotypes --n 694 --m 814 --i 492
```
### Parameters
- `--n`: Number of AD (maximum 694)
- `--m`: Number of AR (maximum 814)
- `--i`: Number of case controls

### Outputs
- `case_variants.txt`: Contains the simulated causative variants for each sample
- `case_chrom_pos.txt`: Contains the chromosome and position information for the causative variants
- `case_genes.csv`: Contains the simulated causative genes for each sample  

## 2. Pairs-based simulation
This tool allows for simulating 1,297 pairs of rare diseases (592 AD and 705 AR). Each pair is assigned the same Orphanet Code, with an associated variant added for each patient. In other words, the two patients in one pair will have different variants, all of which are causal for the disease. This simulated data can be used to match similar patients and identify genes associated with those matches. 

For example, simulating 2,594 individuals, including 1,184 individuals (592 pairs) with autosomal dominant (AD) rare diseases and 1,410 individuals (705 pairs)  with autosomal recessive (AR) rare diseases.

```bash
./RDSim.sh --pairs_genotypes --n 1184 --m 1410
```
### Parameters
- `--n`: Number of AD (maximum 1184)
- `--m`: Number of AR (maximum 1410)

### Outputs
- `pairs_variants.txt`: Contains the simulated causative variants for each sample
- `pairs_chrom_pos.txt`: Contains the chromosome and position information for the causative variants
- `pairs_genes.csv`: Contains the simulated causative genes for each sample

## 3. Pathway-based simulation
This tool allows the simulation of 736 pathway-based rare diseases (342 AD and 394 AR). Each rare disease involves three patients: two as in the pair simulations, and a third who has a mutation in a gene within the same pathway as the causal gene. This approach can be used to match similar patients and identify new mutations in different genes associated with a disease.
   
For example, simulating 2,208 individuals, including 1,026 individuals (342 pathway groups) with autosomal dominant (AD) rare diseases and 1,182 individuals (394 pathway groups) with autosomal recessive (AR) rare diseases.

```bash
python pairs_genotypes.py --n 1026 --m 1182
```
### Parameters
- `--n`: Number of AD (maximum 1026)
- `--m`: Number of AR (maximum 1182)

### Outputs
- `pathway_variants.txt`: Contains the simulated causative variants for each sample
- `pathway_chrom_pos.txt`: Contains the chromosome and position information for the causative variants
- `pathway_genes.csv`: Contains the simulated causative genes for each sample

# Sept 6: Add causative variants into the simulated genotypes

For case-based simulation
```bash
./RDSim.sh --rd_sim --chrom_pos case_chrom_pos.txt --input genome --variants case_variants.txt --output case_genome.vcf
```
For pairs-based simulation
```bash
./RDSim.sh --rd_sim --chrom_pos pairs_chrom_pos.txt --input genome --variants pairs_variants.txt --output pairs_genome.vcf
```
For case-based simulation
```bash
./RDSim.sh --rd_sim --chrom_pos pathway_chrom_pos.txt --input genome --variants pathway_variants.txt --output pathway_genome.vcf
```
### parameters
- `--chrom_pos`: The chromosome and position information for the causative variants
- `--input`: The simulated genotypes through ProxyTyper
- `--variants`: The simulated causative genes for each sample
- `--output`: The simulated genetypes for rare diseases

### Outputs
- `case_genome.vcf`: VCF file containing simulated genotypes for rare disease patients (case-based simulation)
- `pairs_genome.vcf`: VCF file containing simulated genotypes for rare disease patients (pairs-based simulation)
- `pathway_genome.vcf`: VCF file containing simulated genotypes for rare disease patients (pathway-based simulation)

# For simulated genotypes of rare diseases patients test using Exomiser
## 1. extract the genotypes for one sample

```bash
bcftools view -s SAMPLE_NAME case_exome.vcf -Ov -o case_exome_0001.vcf
```

## 2. extract 90,000 variants with the mutative variants included


