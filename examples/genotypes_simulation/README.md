# Genotypes Simulation
For genotype simulation, the process begins by simulating genotypes for a specified number of individuals using the 1000 Genomes Project Phase 3 as the reference dataset, employing tools such as ProxyTyper and PLINK. Subsequently, rare disease mutations are identified using the ClinVar and Orphanet databases. We identified 1,508 rare diseases, including 694 autosomal dominant (AD) and 814 autosomal recessive (AR) conditions from ClinVar and Orphanet databases.After that, an additional mutation is introduced into one of these individuals to generate the simulated genotypes for rare disease patients.

# Step 1: Determine the total number of individuals to simulate
RDSim used the resample function of ProxyTyper to simulate the sample genotypes. Refer "https://github.com/harmancilab/ProxyTyper/tree/main/examples/2_Resampling_Panels".
Make sure ProxyTyper is installed (https://github.com/harmancilab/ProxyTyper/tree/main/installation), as it is required for simulating patient genotypes.

(1) After install ProxyTyper follow the instruction, run this command line to test if it succefully installed. test the script by:

```bash
./ProxyTyper.sh
```
(2) Copy the genome_sim.sh into the same directory with ProxyTyper.sh, run this code to generate 
for example to simulate 1000 

```bash
./genome_sim.sh --n 1000 --m 1000
```

This command line generates an output .vcf.gz file, like "geno_chr1_unique_resampled.vcf.gz" which simulates the whole genome genotypes for chromosomes 1 to 22. 

(3) Mount all the .vcf.gz files simulated genotypes using ProxyTyper into the docker container

```bash
docker run -it -v /path/to/*.vcf.gz:/app/script/*.vcf.gz rdsim bash
```



