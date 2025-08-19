#!/bin/bash

# RDSim.sh: Wrapper script for RDSim simulation tools
# Usage examples:
#   ./RDSim.sh --genome_sim --n 2000
#   ./RDSim.sh --genome_merge
#   ./RDSim.sh --exome_sim --input genome --output exome
#   ./RDSim.sh --case_genotypes --n 1000 --m 1000
#   ./RDSim.sh --case_phenotypes --n 20 --m 20 --hpo_i 5 --hpo_n 3 --hpo_m 2
#   ./RDSim.sh --rd_sim --chrom_pos case_chrom_pos.txt --input exome --variants case_variants.txt --output case_exome.vcf
#   ./RDSim.sh --pairs_genotypes --n 500 --m 200
#   ./RDSim.sh --pairs_phenotypes --n 30 --m 30 --hpo_i 2 --hpo_n 3 --hpo_m 1
#   ./RDSim.sh --pathway_genotypes --n 1000 --m 100
#   ./RDSim.sh --pathway_phenotypes --n 40 --m 40 --hpo_i 4 --hpo_n 5 --hpo_m 2

# Path to src folder
SRC_DIR="$(dirname "$0")/../src"

usage() {
    echo "Usage: $0 [--genome_sim | --genome_merge | --exome_sim |"
    echo "           --case_genotypes | --case_phenotypes | --rd_sim |"
    echo "           --pairs_genotypes | --pairs_phenotypes |"
    echo "           --pathway_genotypes | --pathway_phenotypes] [options]"
    exit 1
}

if [ $# -lt 1 ]; then
    usage
fi

COMMAND="$1"
shift

case $COMMAND in
    --genome_sim)
        bash "$SRC_DIR/genome_sim.sh" "$@"
        ;;
    --genome_merge)
        bash "$SRC_DIR/genome_merge.sh" "$@"
        ;;
    --exome_sim)
        bash "$SRC_DIR/exome_sim.sh" "$@"
        ;;
    --case_genotypes)
        python "$SRC_DIR/case_genotypes.py" "$@"
        ;;
    --case_phenotypes)
        python "$SRC_DIR/case_phenotypes.py" "$@"
        ;;
    --rd_sim)
        bash "$SRC_DIR/rd_sim.sh" "$@"
        ;;
    --pairs_genotypes)
        python "$SRC_DIR/pairs_genotypes.py" "$@"
        ;;
    --pairs_phenotypes)
        python "$SRC_DIR/pairs_phenotypes.py" "$@"
        ;;
    --pathway_genotypes)
        python "$SRC_DIR/pathway_genotypes.py" "$@"
        ;;
    --pathway_phenotypes)
        python "$SRC_DIR/pathway_phenotypes.py" "$@"
        ;;
    *)
        echo "❌ Error: Unknown command $COMMAND"
        usage
        ;;
esac

