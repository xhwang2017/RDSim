import argparse
from case_functions import case_variants, case_genes

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description='Run case functions with specified parameters.')

    # Add arguments
    parser.add_argument('--n', type=int, help='Number of AD', required=True)
    parser.add_argument('--m', type=int, help='Number of AR', required=True)
    parser.add_argument('--i', type=int, help='Number of controls', required=False, default=0)  # Default to 0 if not provided

    # Parse the arguments
    args = parser.parse_args()

    # Call the functions with arguments from the command line
    case_variants(args.n, args.m, args.i)
    case_genes(args.n, args.m)

if __name__ == "__main__":
    main()