import argparse
from pairs_functions import pairs_phenotypes, pairs_hpo

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description='Run pairs functions with specified parameters.')

    # Add arguments
    parser.add_argument('--n', type=int, help='Number of AD', required=True)
    parser.add_argument('--m', type=int, help='Number of AR', required=True)
    parser.add_argument('--hpo_i', type=int, help='Number of rare disease-related HPO terms to select, simulating scenarios where "i" rare disease-related HPO terms are randomly chosen for phenotype simulation', required=True)
    parser.add_argument('--hpo_n', type=int, help='Number of rare disease-related HPO terms to select, simulating scenarios where "n" rare disease-related HPO terms are randomly chosen. Additionally, "m" HPO terms are randomly selected from the entire set of HPO terms to introduce noise for phenotype simulation.', required=True)
    parser.add_argument('--hpo_m', type=int, help='Number of rare disease-unrelated HPO terms to select, simulating scenarios where "n" rare disease-related HPO terms are randomly chosen. Additionally, "m" HPO terms are randomly selected from the entire set of HPO terms to introduce noise for phenotype simulation.', required=True)

    # Parse the arguments
    args = parser.parse_args()

    # Call the functions with arguments from the command line
    pairs_phenotypes(args.n, args.m)
    pairs_hpo(args.hpo_i, args.hpo_n, args.hpo_m)  
    
if __name__ == "__main__":
    main()