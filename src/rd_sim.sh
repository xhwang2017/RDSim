#!/bin/bash

# Exit immediately if a command fails
set -e
set -u -o pipefail

# Start time
start_time=$(date +%s)

PLINK=/data_sys/internal/xwang34/plink2    # change if full path required

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        --chrom_pos)
        chrom_pos_file="$2"
        shift # past argument
        shift # past value
        ;;
        --input)
        input_file="$2"
        shift
        shift
        ;;
        --variants)
        variants_file="$2"
        shift
        shift
        ;;
        --output)
        output_file="$2"
        shift
        shift
        ;;
        *)
        echo "Unknown argument: $1"
        echo "Usage: $0 --chrom_pos <chrom_pos_file> --input <input_file> --variants <variants_file> --output <output_file>"
        exit 1
        ;;
    esac
done

# Validate required parameters
if [[ -z "$chrom_pos_file" || -z "$input_file" || -z "$variants_file" || -z "$output_file" ]]; then
    echo "Error: Missing required arguments."
    echo "Usage: $0 --chrom_pos <chrom_pos_file> --input <input_file> --variants <variants_file> --output <output_file>"
    exit 1
fi

# Step 1: Convert CHROM and POS values to PLINK range format
awk '{print $1, $2, $2}' "$chrom_pos_file" > rare_disease_snps.txt

# Step 2: Remove variants from BED file based on the list of CHROM and POS values
$PLINK --bfile "$input_file" --exclude range rare_disease_snps.txt --make-bed --out filtered_snps

# Step 3: Create a VCF file from the filtered PLINK binary files
$PLINK --bfile filtered_snps --recode vcf --out filtered_snps

echo "Format the simulated varants from rare disease."
# Step 4: Format the simulated variants from rare diseases
sed 's/ \+/\t/g' "$variants_file" > formatted_variants.txt

echo "Adding new variants into the simulated vcf file."
# Step 5: Add new variants to the filtered VCF file
cat filtered_snps.vcf formatted_variants.txt > rd_variants.vcf

echo "Sorting the vcf file by CHROM and POS"
# Step 6: Sort the VCF file by CHROM and POS
(grep "^#" rd_variants.vcf; grep -v "^#" rd_variants.vcf | sort -k1,1V -k2,2n) > "$output_file"

# Cleanup intermediate files
rm rare_disease_snps.txt filtered_snps* formatted_variants.txt rd_variants.vcf

# End time and duration
end_time=$(date +%s)
duration=$((end_time - start_time))

# Convert to hours, minutes, seconds
hours=$((duration / 3600))
minutes=$(((duration % 3600) / 60))
seconds=$((duration % 60))

echo "======================================"
echo "Total runtime: ${hours}h ${minutes}m ${seconds}s"
echo "======================================"
