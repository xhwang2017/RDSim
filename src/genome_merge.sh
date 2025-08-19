#!/bin/bash

# Exit immediately if a command fails
set -euo pipefail

# Start time
start_time=$(date +%s)

PLINK=/data_sys/internal/xwang34/plink2    # Full path to plink2 binary

# Step 1: Convert VCF files to PLINK binary format (.bed/.bim/.fam)
for chr in $(seq 1 22); do
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Converting chromosome $chr VCF to PLINK format..."
    $PLINK \
        --vcf geno_chr${chr}_unique_resampled.vcf.gz \
        --make-bed \
        --out geno_chr${chr}
done

echo "All chromosomes converted to PLINK1 format."

# Step 2: Rename sample IDs in .fam files to 0001, 0002, ...
for chr in $(seq 1 22); do
    fam="geno_chr${chr}.fam"
    echo "Renaming samples in $fam..."
    awk 'BEGIN {OFS="\t"} {print $1, sprintf("%04d", NR), $3, $4, $5, $6}' "$fam" > tmp && mv tmp "$fam"
done

echo "Sample IDs updated."

# Step 3: Convert each chromosome to PLINK2 format (.pgen/.psam/.pvar)
for chr in $(seq 1 22); do
    $PLINK --bfile geno_chr${chr} --make-pgen --out geno_chr${chr}
done

echo "All chromosomes converted to PLINK2 format."

# Step 4: Merge all chromosomes into one file
BASE="geno_chr1"
MERGED="$BASE"

for chr in $(seq 2 22); do
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Merging $MERGED with geno_chr${chr}..."
    OUT="${BASE}_chr${chr}"
    $PLINK --pfile $MERGED --pmerge geno_chr${chr} --make-pgen --out $OUT
    MERGED="$OUT"
done

# Step 5: Convert final merged PLINK2 file to PLINK1 binary
$PLINK --pfile "$MERGED" --make-bed --out genome

# remove the intermediate file
rm *.pgen
rm *.psam
rm *.pvar
rm *.log
rm *.vcf.gz
rm geno_chr*


# Step 6: Report runtime
end_time=$(date +%s)
duration=$((end_time - start_time))
hours=$((duration / 3600))
minutes=$(((duration % 3600) / 60))
seconds=$((duration % 60))

echo "======================================"
echo "Total runtime: ${hours}h ${minutes}m ${seconds}s"
echo "======================================"
