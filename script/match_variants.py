#!/usr/bin/env python3

"""
match_variants.py

Add AC/AN → match rare variant distribution with gnomAD.

Example:
./match_variants.py \
    --input exome_genome.vcf.gz \
    --output exome_genome_matched.vcf.gz \
    --gnomad gnomad.exomes.r2.1.1.sites.vcf.bgz
"""

from cyvcf2 import VCF, Writer
import pysam
import random
from tqdm import tqdm
import argparse
import os

# =====================================================
# ARGUMENT PARSER
# =====================================================
def parse_args():
    parser = argparse.ArgumentParser(
        description="Match simulated variant distribution to gnomAD"
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Input simulated VCF (.vcf.gz)"
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Output matched VCF (.vcf.gz)"
    )

    parser.add_argument(
        "--gnomad",
        default="gnomad.exomes.r2.1.1.sites.vcf.bgz",
        help="gnomAD sites VCF (default: gnomad.exomes.r2.1.1.sites.vcf.bgz)"
    )

    return parser.parse_args()


# =====================================================
# ADD AC / AN
# =====================================================
def add_ac_an(input_vcf, tmp_vcf):

    print("\n[Step 1] Calculating AC/AN...")

    vcf = VCF(input_vcf)

    vcf.add_info_to_header({
        'ID': 'AC',
        'Description': 'Alternate allele count',
        'Type': 'Integer',
        'Number': 'A'
    })

    vcf.add_info_to_header({
        'ID': 'AN',
        'Description': 'Total allele number',
        'Type': 'Integer',
        'Number': '1'
    })

    writer = Writer(tmp_vcf, vcf)

    for var in tqdm(vcf, desc="Computing AC/AN"):

        AC, AN = 0, 0

        for gt in var.genotypes:
            a1, a2 = gt[0], gt[1]
            if a1 is None or a2 is None:
                continue
            AN += 2
            AC += a1 + a2

        var.INFO["AC"] = AC
        var.INFO["AN"] = AN

        writer.write_record(var)

    writer.close()
    vcf.close()


# =====================================================
# MAC BINNING
# =====================================================
def get_bin(AC, AN):

    if isinstance(AC, (tuple, list)):
        AC = AC[0]
    if isinstance(AN, (tuple, list)):
        AN = AN[0]

    if AC is None or AN == 0:
        return None

    maf = AC / AN

    if AC == 1:
        return "singleton"
    if maf <= 0.01:
        return "MAC21-MAF1"
    return "MAF>1"


# =====================================================
# COMPUTE TARGET DIFFERENCE
# =====================================================
def compute_targets(sim_vcf, gnomad_vcf):

    def count_bins(path, label):

        counts = {"singleton": 0, "MAC21-MAF1": 0}

        vcf = pysam.VariantFile(path)

        for rec in tqdm(vcf, desc=f"Scanning {label}"):
            b = get_bin(rec.info.get("AC"), rec.info.get("AN"))
            if b in counts:
                counts[b] += 1

        return counts

    print("\n[Step 2] Computing distribution differences...")

    sim_counts = count_bins(sim_vcf, "Simulated")
    gnomad_counts = count_bins(gnomad_vcf, "gnomAD")

    ADD_SINGLETONS = max(
        0, gnomad_counts["singleton"] - sim_counts["singleton"]
    )

    ADD_MAC21 = max(
        0, gnomad_counts["MAC21-MAF1"] - sim_counts["MAC21-MAF1"]
    )

    PRUNE_COMMON = ADD_SINGLETONS + ADD_MAC21

    print("\nTargets:")
    print("ADD_SINGLETONS =", ADD_SINGLETONS)
    print("ADD_MAC21 =", ADD_MAC21)
    print("PRUNE_COMMON =", PRUNE_COMMON)

    return ADD_SINGLETONS, ADD_MAC21, PRUNE_COMMON


# =====================================================
# HELPERS
# =====================================================
def assign_genotypes(rec, AC, samples):

    n = len(samples)
    rec.info["AC"] = AC
    rec.info["AN"] = n * 2

    chosen = random.sample(range(n), min(n, AC))

    for i, s in enumerate(samples):
        rec.samples[s]["GT"] = (0, 1) if i in chosen else (0, 0)


def make_variant(template, header, samples, offset, target):

    rec = header.new_record(
        contig=template.chrom,
        start=template.pos + offset,
        stop=template.pos + offset + len(template.ref),
        alleles=template.alleles,
    )

    AC = 1 if target == "singleton" else max(21, int(len(samples)*0.02))

    assign_genotypes(rec, AC, samples)

    return rec


# =====================================================
# MATCH DISTRIBUTION
# =====================================================
def match_distribution(tmp_vcf, gnomad_vcf, output_vcf):

    ADD_SINGLETONS, ADD_MAC21, PRUNE_COMMON = compute_targets(
        tmp_vcf, gnomad_vcf
    )

    sim = pysam.VariantFile(tmp_vcf)
    samples = list(sim.header.samples)

    variants, common = [], []

    print("\nReading simulated VCF...")
    for rec in tqdm(sim):
        b = get_bin(rec.info.get("AC"), rec.info.get("AN"))
        if b == "MAF>1":
            common.append(rec)
        else:
            variants.append(rec)

    # prune
    remove = random.sample(common, min(PRUNE_COMMON, len(common)))
    variants.extend([r for r in common if r not in remove])

    print("\nLoading gnomAD templates...")
    gnomad = pysam.VariantFile(gnomad_vcf)

    singletons, mac21 = [], []

    for rec in tqdm(gnomad):
        b = get_bin(rec.info.get("AC"), rec.info.get("AN"))
        if b == "singleton":
            singletons.append(rec)
        elif b == "MAC21-MAF1":
            mac21.append(rec)

    print("\nAdding singleton variants...")
    for i in tqdm(range(ADD_SINGLETONS)):
        variants.append(
            make_variant(random.choice(singletons),
                         sim.header, samples, i+1_000_000, "singleton")
        )

    print("\nAdding MAC21 variants...")
    for i in tqdm(range(ADD_MAC21)):
        variants.append(
            make_variant(random.choice(mac21),
                         sim.header, samples, i+2_000_000, "MAC21-MAF1")
        )

    print("\nWriting output...")
    out = pysam.VariantFile(output_vcf, "w", header=sim.header)

    for rec in tqdm(variants):
        out.write(rec)

    out.close()

    print("\n✅ Finished:", output_vcf)


# =====================================================
# MAIN
# =====================================================
def main():

    args = parse_args()

    input_vcf = args.input
    output_vcf = args.output
    gnomad_vcf = args.gnomad

    tmp_vcf = os.path.splitext(output_vcf)[0] + ".with_AC_AN.vcf.gz"

    add_ac_an(input_vcf, tmp_vcf)
    match_distribution(tmp_vcf, gnomad_vcf, output_vcf)


if __name__ == "__main__":
    main()