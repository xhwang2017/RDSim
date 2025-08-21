#!/bin/bash

# Exit immediately if a command fails
set -e

# Start time
start_time=$(date +%s)


# Default resample size
n_resample_size=2000

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
  case $1 in
    --n)
      n_resample_size="$2"
      shift 2
      ;;
    *)
      echo "Unknown parameter: $1"
      exit 1
      ;;
  esac
done

# Directory to store genetic maps and output VCFs
mkdir -p genetic_maps output_vcfs

# Download BEAGLE genetic maps once
./ProxyTyper.sh -setup_BEAGLE_genetic_maps https://bochet.gcc.biostat.washington.edu/beagle/genetic_maps/plink.GRCh37.map.zip

# Loop over chromosomes 1 to 22
for chr in {1..22}; do
    echo "Processing chromosome ${chr}..."

    # Download reference VCF
    vcf_file="ALL.chr${chr}.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz"
    wget -c https://ftp-trace.ncbi.nih.gov/1000genomes/ftp/release/20130502/${vcf_file}

    # Step variables
    ref_VCF=${vcf_file}
    all_REF_panel_ID=geno_chr${chr}
    is_panel_phased=1
    update_variant_ID=1

    # Import VCF
    ./ProxyTyper.sh -import_VCF ${ref_VCF} ${is_panel_phased} ${update_variant_ID} ${all_REF_panel_ID}
    # Uniquefy panel variants

    ./ProxyTyper.sh -uniquefy_panel_variants ${all_REF_panel_ID} ${all_REF_panel_ID}_unique
    all_REF_panel_ID=${all_REF_panel_ID}_unique

    # Resample
    resampled_ID=${all_REF_panel_ID}_resampled
    ./ProxyTyper.sh -resample_panel ${all_REF_panel_ID} ${n_resample_size} ${resampled_ID}

    echo "Chromosome ${chr} resample processing complete."
done

# Export each chromosome to VCF
for chr in {1..22}; do
    # Define IDs for this chromosome
    all_REF_panel_ID="geno_chr${chr}_unique"
    resampled_ID="${all_REF_panel_ID}_resampled"

    # Export to VCF
    ./ProxyTyper.sh -export_VCF "${resampled_ID}" hg19 "${chr}" output_vcfs/"${resampled_ID}.vcf.gz"

    echo "Chromosome ${chr} export to VCF processing complete."
done

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
