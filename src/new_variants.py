#!/usr/bin/env python3
import pandas as pd
import argparse
import numpy as np
import random
import os

# Build the path to the data folder dynamically
script_dir = os.path.dirname(__file__)  # Directory of the current script

def new_variants(v, n, m, i):
    """
    Extract rows and columns from 'variants_new_vcf.csv' and add extra columns efficiently.

    Args:
        v (int): number of rows per disease block to select (1-3)
        n (int): number of top diseases (first 9+n columns)
        m (int): number of bottom diseases (last m columns)
        i (int): number of extra columns with all values set to "0/0"

    Returns:
        pd.DataFrame: extracted dataset with extra columns
    """
    # Read the file into a DataFrame
    data_file = os.path.join(script_dir, "../data/variants_new_vcf.csv")
    data_file = os.path.abspath(data_file)
    df = pd.read_csv(data_file)

    # Ensure n and m are within reasonable limits
    n = min(n, 814)
    m = min(m, 694)
    
    # Each disease has 3 rows
    disease_rows = 3
    total_diseases = len(df) // disease_rows
    
    # -------------------------
    # Step 1: select rows
    # -------------------------
    top_rows = [d * disease_rows + r for d in range(n) for r in range(v)]
    bottom_rows = [d * disease_rows + r for d in range(total_diseases - m, total_diseases) for r in range(v)]
    
    selected_rows = top_rows + bottom_rows
    df_rows_selected = df.loc[selected_rows].reset_index(drop=True)
    
    # -------------------------
    # Step 2: select columns
    # -------------------------
    df_first = df_rows_selected.iloc[:, :9+n].copy()  # first 9+n columns
    df_last = df_rows_selected.iloc[:, -m:].copy()    # last m columns
    
    # Combine first and last columns
    df_final = pd.concat([df_first, df_last], axis=1)
    
    # -------------------------
    # Step 3: add i extra columns with "0/0" efficiently
    # -------------------------
    if i > 0:
        new_cols = pd.DataFrame("0/0", index=df_final.index, columns=[f'new_col_{j+1}' for j in range(i)])
        df_final = pd.concat([df_final, new_cols], axis=1)
    
    # -------------------------
    # Step 4: save results
    # -------------------------
    df_final.to_csv('new_variants.txt', sep='\t', index=False, header=False)
    
    # Extract CHROM and POS columns
    chrom_pos_columns = df_final[['CHROM', 'POS']]
    chrom_pos_columns.to_csv("new_chrom_pos.txt", index=False, header=False, sep='\t')
    
    return df_final

# -------------------------
# Command-line interface
# -------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract variants and add extra columns.")
    parser.add_argument("--v", type=int, required=True, help="Number of rows per disease block (1-3)")
    parser.add_argument("--n", type=int, required=True, help="Number of top diseases")
    parser.add_argument("--m", type=int, required=True, help="Number of bottom diseases")
    parser.add_argument("--i", type=int, required=True, help="Number of extra columns with '0/0'")
    
    args = parser.parse_args()
    
    new_variants(args.v, args.n, args.m, args.i)
    print(f"Finished generating new_variants.txt and new_chrom_pos.txt with v={args.v}, n={args.n}, m={args.m}, i={args.i}")