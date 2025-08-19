import argparse
from pathway_functions import pathway_variants, pathway_genes

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description='Run pathway functions with specified parameters.')

    # Add arguments
    parser.add_argument('--n', type=int, help='Number of AD', required=True)
    parser.add_argument('--m', type=int, help='Number of AR', required=True)

    # Parse the arguments
    args = parser.parse_args()

    # Call the functions with arguments from the command line
    pathway_variants(args.n, args.m)
    pathway_genes(args.n, args.m)

if __name__ == "__main__":
    main()