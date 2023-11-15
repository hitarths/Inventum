import pickle, os
from inventum import Inventum
from oracle import Oracle
import argparse, random, ast


def main():
     # Create ArgumentParser object
    parser = argparse.ArgumentParser(description="Process command line arguments.")

    # Add arguments
    parser.add_argument("--database", type=str, required=True,
                        help="Specify database name as a string")
    parser.add_argument("--criterion", type=str, choices=["LP", "bruteforce"], required=False, default = "bruteforce",
                        help="Specify criterion: 'LP' or 'bruteforce'")
    parser.add_argument("--looseness", type=float, default=0.0,
                        help="Specify looseness as a float (default: 0). Guaranteed Regret Ratio < 1 - 1/(1+looseness)")
    parser.add_argument("--negative-attributes", type=str, default="",
                        help="List of natural number that are index of attribute that have negative coefficient as a string in the format '[1, 2, 5, ...]'")
    parser.add_argument("--utility-function", type=str, required=False, default = "",
                        help="List of floats as a string in the format '[1, 2, 3, ...]'")
    parser.add_argument("--cutoff", type=int, required=False, default=1000,
                        help="A cutoff for the database. We only consider first 'cutoff' many tuples")
    parser.add_argument("--notqdm", action="store_true", default=False,
                        help="Flag to disable tqdm (default: False)")


    # Parse arguments
    args = parser.parse_args()
    # Access parsed arguments
    criterion = args.criterion
    database = args.database
    epsilon = args.looseness
    utility_function_str = args.utility_function
    negative_attributes_str = args.negative_attributes
    cutoff = args.cutoff
    notqdm_flag = args.notqdm


    datadir = './real-life-datasets/'
    fdata = database + '.csv'
    loaded = pickle.load(open(datadir+database+'.pkl','rb'))
    df = loaded[0]
    if cutoff:
        df = df.head(cutoff)

    dimension = len(df.columns)

    if utility_function_str == "":
        # choose a random function
        utility = [random.random() for i in range(dimension)]
    else:
        try:
            utility = ast.literal_eval(utility_function_str)
            if not isinstance(utility, list) or not all(isinstance(item, int) or isinstance(item, float) for item in utility):
                raise ValueError("Invalid input. Please provide a valid list of float for utilty function.")
        except (ValueError, SyntaxError) as e:
            print("Error:", e)
            return
    
    if negative_attributes_str == "":
        # choose a random function
        negative_attributes = []
    else:
        try:
            negative_attributes = ast.literal_eval(negative_attributes_str)
            if not isinstance(negative_attributes, list) or not all(isinstance(item, int) for item in negative_attributes):
                raise ValueError("Invalid input. Please provide a valid list of natural for negative attribute index.")
        except (ValueError, SyntaxError) as e:
            print("Error:", e)
            return
        
    if len(utility) < dimension:
        extra = dimension - len(utility)
        for i in range(extra):
            utility.append(0)

    print("Utility Function: ", utility)
    oracle = Oracle(utility)
    inventum = Inventum(df,oracle,epsilon, criterion, negative_attributes, notqdm_flag)
    inventum.search()
    

if __name__ == "__main__":
    main()