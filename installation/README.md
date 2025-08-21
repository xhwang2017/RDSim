# Installation
RDSim is a tool for simulating rare disease patient genotypes and phenotypes. It provides a user-facing bash script (script/RDSim.sh) to run different simulation workflows. Before installing RDSim, make sure ProxyTyper is installed (https://github.com/harmancilab/ProxyTyper/tree/main/installation), as it is required for simulating sample genotypes.

# Option 1: Steps to Install and Run RDSim Using Docker
## Step 1: Clone the repository

```bash
git clone https://github.com/xhwang2017/RDSim.git
cd RDSim
```

## Step 2: Build the Docker Image

```bash
docker build -t rdsim .
```
This tool requires Python, PLINK 2, and BCFtools to be installed. 

## Step 3: Run the Docker Container and Define the Container Name as rdsim_container

```bash
docker run -it --name rdsim_container rdsim bash
```

```bash
docker start -ai rdsim_container
```
This command line is used to open the rdism_container container.

## Step 4: Navigate to the Script Directory

```bash
cd script
```

## Step5: Run RDSim Commands
The main RDSim commands and options include:

| Option                 | Description                                                      |
| ---------------------- | ---------------------------------------------------------------- |
| `--genome_sim`         | Simulate genomic genotypes for each chromosome of rare disease samples|
| `--genome_merge`       | Merge all chromosomes (chr1–chr22) into a single PLINK file      |
| `--exome_sim`          | Simulate exome genotypes for rare disease samples                |
| `--rd_sim`             | Simulate rare disease patients genotypes by adding causative variants|
| `--case_genotypes`     | Generate genotypes for case patients                             |
| `--case_phenotypes`    | Generate phenotypes for case patients                            |
| `--pairs_genotypes`    | Simulate genotypes for paired patient                            |
| `--pairs_phenotypes`   | Simulate phenotype for paired patient                            |
| `--pathway_genotypes`  | Simulate genotypes based on pathway-level variants               |
| `--pathway_phenotypes` | Simulate phenotypes based on pathway-level variants              |

# Option 2: Steps to Install and Run RDSim Without Using Docker
## Step 1: Install the required dependencies
Before you can use the tool, you need to make sure you have the required dependencies installed:
- Python (3.6 or higher)
- NumPy
- Pandas
- ProxyTyper
- PLINK2
- Bcftools (optional)
  
ProxyTyper installation link: (https://github.com/harmancilab/ProxyTyper/tree/main/installation)

PLINK2 isntallation link: (https://www.cog-genomics.org/plink/2.0/)

BCFtools (optional) can be installed by conda

```bash
conda install -c bioconda bcftools
```

## Step 2: Clone the repository

```bash
git clone https://github.com/xhwang2017/RDSim.git
cd RDSim
```

## Step 3: Navigate to the Script Directory

```bash
cd RDSim
cd script
```
## Step4: Run RDSim Commands Shown Above
