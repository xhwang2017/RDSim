import argparse
from pairs_functions import pairs_variants, pairs_genes

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description='Run pair functions with specified parameters.')

    # Add arguments
    parser.add_argument('--n', type=int, help='Number of AD', required=True)
    parser.add_argument('--m', type=int, help='Number of AR', required=True)

    # Parse the arguments
    args = parser.parse_args()

    # Call the functions with arguments from the command line
    pairs_variants(args.n, args.m)
    pairs_genes(args.n, args.m)

if __name__ == "__main__":
    main()