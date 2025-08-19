#!/bin/bash

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        --input)
        input_file="$2"
        shift # past argument
        shift # past value
        ;;
        --output)
        output_file="$2"
        shift
        shift
        ;;
        *)
        echo "Unknown argument: $1"
        echo "Usage: $0 --input <input_file> --output <output_file>"
        exit 1
        ;;
    esac
done

# Validate required parameters
if [[ -z "$input_file" || -z "$output_file" ]]; then
    echo "Error: Missing required arguments."
    echo "Usage: $0 --input <input_file> --output <output_file>"
    exit 1
fi

# Download the hg19 annotation file 
wget https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_45/GRCh37_mapping/gencode.v45lift37.annotation.gtf.gz
gunzip gencode.v45lift37.annotation.gtf

# Step 1: Extract rows with "exon" in the third column of the GTF file
awk '$3 == "exon"' gencode.v45lift37.annotation.gtf > extracted_exons.gtf

# Step 2: Convert the exon entries in the GTF file into a BED file format
awk -F'\t' '{if ($3 == "exon") print $1"\t"$4-1"\t"$5"\t"$9}' extracted_exons.gtf > exons.bed

# Step 3: Use PLINK2 to filter variants in the exon area
/data_sys/internal/xwang34/plink2 --bfile "$input_file" --extract range exons.bed --make-bed --out "$output_file"

# Cleanup intermediate files
rm extracted_exons.gtf exons.bed
