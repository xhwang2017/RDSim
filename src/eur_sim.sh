#!/bin/bash

# Download and extract the 1000 Genomes genotypes data
wget https://mathgen.stats.ox.ac.uk/impute/ALL_1000G_phase1integrated_v3_impute.tgz 
tar ALL_1000G_phase1integrated_v3_impute.tgz

# Decompress chromosome-specific haplotype and legend files
for chr in $(seq 1 22);
	gunzip ALL_1000G_phase1integrated_v3_chr${chr}_impute.hap.gz
	gunzip ALL_1000G_phase1integrated_v3_chr${chr}_impute.legend.gz
done

# Extract European population genotypes
for chr in $(seq 1 22); do
        cut -f 2-182,359,397-402,405-497,996-1093 -d " " ALL_1000G_phase1integrated_v3_chr${chr}_impute.hap \
        > chr${chr}.eur_subset.hap 
done

# Default value for n (optional)
n_param=""

# Parse the command-line arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        --n)
        n_param="$2"
        shift # Shift past the value
        shift # Shift past the argument
        ;;
        *)
        echo "Unknown argument: $1"
        echo "Usage: $0 --n <integer>"
        exit 1
        ;;
    esac
done

# Validate that n_param is provided and is a valid integer
if [[ -z "$n_param" || ! "$n_param" =~ ^[0-9]+$ ]]; then
    echo "Error: Missing or invalid value for --n."
    echo "Usage: $0 --n <integer>"
    exit 1
fi


# Genotype simulation for eur via Hapgen2
for chr in $(seq 1 22); do
        dummyDL=$(sed -n '2p' "ALL_1000G_phase1integrated_v3_chr${chr}_impute.legend" | cut -d ' ' -f 2)
        nohup hapgen2 -m genetic_map_chr${chr}_combined_b37.txt \
            -l ALL_1000G_phase1integrated_v3_chr${chr}_impute.legend \
            -h chr${chr}.eur_subset.hap \
            -o eur_genotypes_chr${chr}_hapgen \
            -n "$n_param" 0 \
            -dl "$dummyDL" 0 0 0 \
            -no_haps_output &
        sleep 2
done

# Convert hap file to PLINK bed format using plink2
for chr in $(seq 1 22); do
         plink2 --data eur_genotypes_chr${chr}_hapgen 'ref-first' \
                --oxford-single-chr ${chr} \
                --make-bed \
                --out eur_genotypes_chr${chr}_hapgen
done

# Merge all the chromsomes into a single genome dataset
for chr in $(seq 1 22); do
        plink2 --bfile eur_genotypes_chr${chr}_hapgen --make-pgen --out eur_genotypes_chr${chr}_hapgen
done

for chr in $(seq 2 22); do
    if [ $chr -eq 2 ]; then
        plink2 --bfile eur_genotypes_chr1_hapgen --pmerge eur_genotypes_chr${chr}_hapgen --make-bed --out eur_genome
    else
        plink2 --bfile eur_genome --pmerge eur_genotypes_chr${chr}_hapgen --make-bed --out eur_genome
    fi
done

