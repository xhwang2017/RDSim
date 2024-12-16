#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
import random
import os

# Build the path to the data folder dynamically
script_dir = os.path.dirname(__file__)  # Directory of the current script


def case_variants(n, m, i):
    """
    Simulate causative variants of samples for AD (Autosomal Dominant) and AR (Autosomal Recessive) inheritance.

    Args:
        n (int): A non-negative integer specifying the number of Autosomal Dominant (AD) samples to simulate.
        m (int): A non-negative integer specifying the number of Autosomal Recessive (AR) samples to simulate.
        i (int): A non-negative integer specifying the number of healthy samples to simulate.

    Returns:
        None: This function generates and saves two text files:
            1. `case_variants.txt`: Contains the simulated causative variants for each sample.
            2. `case_chrom_pos.txt`: Contains the chromosome and position information for the causative variants.

    """
    # Read the file into a DataFrame
    data_file = os.path.join(script_dir, "../data/variants_case_vcf.csv")
    data_file = os.path.abspath(data_file)
    df = pd.read_csv(data_file)
    
    # Ensure n and m are within the specified limits
    n = min(n, 814)
    m = min(m, 694)
      
    # Extract first n rows and last m rows
    rows_extracted = pd.concat([df.head(n).copy(), df.tail(m).copy()])
    
    # Extract first 5+n columns and last m columns
    columns_extracted = pd.concat([df.iloc[:, :5+n].copy(), df.iloc[:, -m:]].copy(), axis=1)
    
    # Combine extracted rows and columns
    extracted_df = rows_extracted[columns_extracted.columns].copy()   
    
    # Add `i` new columns with all values set to "0/0"
    for col_index in range(i):
        extracted_df[f'new_col_{col_index + 1}'] = "0/0"
    
    # Save the result to a txt file
    extracted_df.to_csv('case_variants.txt', sep='\t', index=False, header=False)
    
    # Extract the first two columns (CHROM and POS)
    chrom_pos_columns = extracted_df[['CHROM', 'POS']]

    # Save to a text file
    chrom_pos_columns.to_csv("case_chrom_pos.txt", index=False, header=False, sep='\t')
    
    return extracted_df



# Define the function to allow users to get the causative genes for the simulated patients.
def case_genes(n, m): 
    """
    Simulate causative genes of paired samples for AD (Autosomal Dominant) and AR (Autosomal Recessive) inheritance.

    Args:
        n (int): A non-negative integer specifying the number of Autosomal Dominant (AD) samples to simulate.
        m (int): A non-negative integer specifying the number of Autosomal Recessive (AR) samples to simulate.

    Returns:
        None: This function generates and saves a csv file:
        'case_genes.csv`: Contains the simulated causative genes for each sample.
        
    """    
    # Read the file into a DataFrame
    data_file = os.path.join(script_dir, "../data/case_variants_gene_orpha_inher.csv")
    data_file = os.path.abspath(data_file)
    df = pd.read_csv(data_file)
    
    # Ensure n and m are within the specified limits
    n = min(n, 814)
    m = min(m, 694)
    
    # Extract first n rows and last m rows
    extracted_df = pd.concat([df.head(n), df.tail(m)])
    
    # Save the result to a txt file
    extracted_df.to_csv('case_genes.csv', index=False)
    
    return extracted_df


# Define the function allowing users to get the phenotypes for the simulated patients.
def case_phenotypes(n, m):
    
    """
    Simulate phenotypes of paired samples for AD (Autosomal Dominant) and AR (Autosomal Recessive) inheritance.

    Args:
        n (int): A non-negative, even integer specifying the number of Autosomal Dominant (AD) samples to simulate.
        m (int): A non-negative, even integer specifying the number of Autosomal Recessive (AR) samples to simulate.

    Returns:
        None: This function generates and saves a csv file:
        `case_phenotypes.csv`: Contains the simulated phenotypes for each sample.
        
    """          
    # Read the file into a DataFrame
    data_file = os.path.join(script_dir, "../data/case_orphacode_hposet.csv")
    data_file = os.path.abspath(data_file)
    df = pd.read_csv(data_file)
    
    # Ensure n and m are within the specified limits
    n = min(n, 814)
    m = min(m, 694)
    
    # Extract first n rows and last m rows
    rows_extracted = pd.concat([df.head(n), df.tail(m)])
    
    # Save the result to a txt file
    rows_extracted.to_csv('case_phenotypes.csv', index=False)
    
    return rows_extracted


# Function to randomly select HPO terms to simulate different scenarios for phenotype simulation
def case_hpo(i, n, m):

    """
    Simulate user-defined scenarios by selecting a specified number of HPO terms related to rare diseases 
    for phenotype simulation.

    Args:
        i (int): A non-negative integer specifying the number of rare disease-related HPO terms to select, 
        simulating scenarios where 'i' rare disease-related HPO terms are randomly chosen for phenotype simulation.  
        
        n (int): A non-negative integer specifying the number of rare disease-related HPO terms to select, 
        simulating scenarios where 'n' rare disease-related HPO terms are randomly chosen. Additionally, 
        'm' HPO terms are randomly selected from the entire set of HPO terms to introduce noise for phenotype simulation.
        
        m (int): A non-negative integer specifying the number of rare disease-unrelated HPO terms to select, 
        simulating scenarios where 'n' rare disease-related HPO terms are randomly chosen. Additionally, 
        'm' HPO terms are randomly selected from the entire set of HPO terms to introduce noise for phenotype simulation.

    Returns:
        None: This function generates and saves a csv file:
        `case_hpo.csv`: Contains the simulated HPO terms user selected for each sample.
        
    """    
    
    # read the orphanet code and hpoid of case information
    data_file = os.path.join(script_dir, "case_phenotypes.csv")
    data_file = os.path.abspath(data_file)
    df_case_hposet = pd.read_csv(data_file)
    
    def random_hpo(hpo_str, i):
        # Split the HPO terms by "; " and randomly select n terms
        hpo_terms = hpo_str.split("; ")
        selected_terms = random.sample(hpo_terms, min(i, len(hpo_terms)))  # limit to available terms
        return "; ".join(selected_terms)
    
    # Function to select random HPO terms from a string
    def random_hpo_noise(hpo_str, num_terms):
        # Split the HPO terms by "; " and randomly select the specified number of terms
        hpo_terms = hpo_str.split("; ")
        selected_terms = random.sample(hpo_terms, min(num_terms, len(hpo_terms)))  # limit to available terms
        return selected_terms
    
    # read the orphanet code and hpoid of case information
    data_file = os.path.join(script_dir, "../data/hpo_id_all.csv")
    data_file = os.path.abspath(data_file)
    df_all_hpo = pd.read_csv(data_file)
    
    # Convert df_all_hpo 'hpo_id' column to a list of all HPO terms
    all_hpo_terms = df_all_hpo['hpo_id'].tolist()
    
    # Apply the function to create the HPO_NOISE column in df_case_hposet
    def combine_hpo_noise(row):
        # Select n terms from the HPO_ALL column in df_case_hposet
        selected_hpo_all = random_hpo_noise(row['HPO_ALL'], n)
        # Select m terms from the df_all_hpo HPO list
        selected_hpo_noise = random.sample(all_hpo_terms, min(m, len(all_hpo_terms)))
        # Combine and return as a single string with "; " delimiter
        return "; ".join(selected_hpo_all + selected_hpo_noise)

    # Apply the function to each row in df_case_hposet
    df_case_hposet[f'HPO_{i}'] = df_case_hposet['HPO_ALL'].apply(lambda x: random_hpo(x, i))    

    # Add the new column HPO_NOISE to df_case_hposet
    df_case_hposet['HPO_NOISE'] = df_case_hposet.apply(combine_hpo_noise, axis=1)
    
    # Save the result to a csv file
    df_case_hposet.to_csv('case_hpo.csv')

    return df_case_hposet


