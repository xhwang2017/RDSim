# RDSim
# Introduction
RDSim is a Python package designed to simulate the genotypes and phenotypes of rare disease patients. This package can be used by researchers and students to generate synthetic data for facilitating the evaluation of tools aimed at identifying the causal genes or mutations of rare diseases. 

For genotype simulation, the process begins by simulating genotypes for a specified number of individuals using the 1000 Genomes Project Phase III as the reference dataset, employing tools such as ProxyTyper and PLINK. Subsequently, rare disease mutations are identified using the ClinVar and Orphanet databases. After that, an additional mutation is introduced into one of these individuals to generate the simulated genotypes for rare disease patients.

For phenotype simulation, HPO terms related to rare diseases, along with the complete set of HPO terms, are selected from the HPO database. Three scenarios can then be simulated for HPO term selection: using all HPO terms associated with the disease, randomly choosing n HPO terms related to rare diseases, or adding m HPO terms from the entire HPO database to introduce some noise.

# RDSim Process
<img width="1417" alt="Screenshot 2025-01-17 at 11 12 07 AM" src="https://github.com/user-attachments/assets/79ed0938-f23e-4063-9d3a-ffce0e8a804d" />
![Figure1_JPEG](https://github.com/user-attachments/assets/cb87f159-b6bb-4b32-979b-56853298865b)
Fig. 1. Overview of the RDSim workflow and case study result. (a) Genotype simulation: Background genotypes were generated using the 1000 Genomes Project Phase 3 dataset as the reference panel and exome regions were subsequently extracted. Rare disease variants were curated from ClinVar and Orphanet, and an additional variant was introduced into selected individuals to produce the final simulated genotypes. (b) Phenotype simulation: rare disease-associated and global HPO terms were obtained from the HPO and Orphanet database. Three scenarios were implemented for phenotype selection: (i) inclusion of all HPO terms associated with the disease; (ii) random selection of n disease-related HPO terms; or (iii) random selection of n disease-related HPO terms supplemented with m additional terms from the full HPO set to introduce noise. (c) Case study result: A simulated patient carrying the pathogenic FGFR3 variant and phenotypes including hearing impairment (HP:0000365) and knee joint hypermobility (HP:0045086) was analyzed with Exomiser. Using the hiPHIVE prioritization algorithm, Exomiser ranked FGFR3 as the top candidate gene, with a phenotypic similarity score of 0.888 to achondroplasia associated with FGFR3.<img width="468" height="257" alt="image" src="https://github.com/user-attachments/assets/a8a58b36-fec5-469b-ba7c-fe1c48b328f1" />


# Functions
**1) Case-based simulation:** The simulation covers 1,508 rare diseases, including 694 autosomal dominant (AD) and 814 autosomal recessive (AR) conditions. Each rare disease patient has a mutation associated with a specific rare disease.

**2) Pair-based simulation:**  This allows for simulating 1,297 pairs of rare diseases (592 AD and 705 AR). Each pair is assigned the same Orphanet Code, with an associated variant added for each patient. In other words, the two patients in one pair will have different variants, all of which are causal for the disease. This simulated data can be used to match similar patients and identify genes associated with those matches.

**3) Pathway-based simlation:** This allows the simulation of 736 pathway-based rare diseases (342 AD and 394 AR). Each rare disease involves three patients: two as in the pair simulations, and a third who has a mutation in a gene within the same pathway as the causal gene. This approach can be used to match similar patients and identify new mutations in different genes associated with a disease.

# License
This project is licensed under the MIT License. See the LICENSE file for details.
