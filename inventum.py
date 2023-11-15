import pandas as pd
from constraints import Constraint
from oracle import Oracle
from tqdm import tqdm
import time
from ortools.linear_solver import pywraplp

RANDOM_POINTS_NUM = 10
DIFF_THRESHOLD_FACTOR = 0.1

DELTA = 0.000001

class Inventum:
    def __init__(self, data_frame, oracle: Oracle, eps = 0.1, criterion="LP", negative_attributes = []):
        """
        Initialize the Inventum class with a pandas DataFrame and an Oracle instance.

        Args:
        - data_frame (pandas DataFrame): Input DataFrame with numeric columns.
        - Oracle (Oracle instance): Instance of the Oracle class.

        Attributes:
        - data_frame (pandas DataFrame): Input DataFrame with numeric columns.
        - Oracle (Oracle instance): Instance of the Oracle class.
        - max_row (int): Class variable initialized to 0, representing the row number.
        - constraints (list): List to store constraints information.
        """
        # Check if all columns in the DataFrame have numeric data types
        if not all(data_frame[col].dtype in (int, float) for col in data_frame.columns):
            raise ValueError("All columns in the DataFrame must have numeric data types")
        
        if len(oracle.utility) != len(data_frame.columns):
            raise ValueError("Utility dimension of the Oracle does not match DataFrame's dimension")

        self.data_frame = data_frame
        self.oracle = oracle
        self.max_row_ind = 0
        self.constraints = []
        self.constraints.append(Constraint([1 for i in range(self.oracle.dimension)], -1, 1))
        self.variable_names = data_frame.columns.tolist()
        self.eps = eps
        self.criterion = criterion
        self.negative_attributes = negative_attributes

        # self.or_variables = dict()
        # self.solver = pywraplp.Solver.CreateSolver("GLOP")
        # if not solver:
        #     raise Exception("Could not initialize the LP Solver")
        # for var in self.variable_names:
        #     self.or_variables[var] = solver.NumVar(0, 1, var) # create a OR variable 

    
    def search(self):
        """
        Search for the tuple that the Oracle prefers the most.

        Iterates through each row of the DataFrame, calling decideQuery for each row.
        """
        # We treat each row as a function
        max_func = self.data_frame.iloc[self.max_row_ind].tolist()
        for idx, func in tqdm(self.data_frame.iterrows(), total=len(self.data_frame), desc="Processing Rows"):
            if idx == 0:
                continue
            curr_func = func.tolist()
            res = self.decideQuery(curr_func, idx, self.criterion)  # Placeholder function to determine if we need to query
            if res == 2:
                # curr_func is greater than the max_func for all points in the feasible. Update the max without asking the user
                self.max_row_ind = idx
                max_func = curr_func
                
            elif res == 1:
                # curr_func is significantly greater than the max_func (at least (1+self.eps*max_func))at some point in feasible region, but not all points
                # curr_func intersects with max_fun 
                oracle_result = self.oracle.query(max_func, curr_func)
                if oracle_result == 0:
                    # the user still prefers the current max_func, hence the feasible region shrinks to points where max_func >= curr_func + DELTA
                    if self.criterion == "LP":
                        self.constraints.append(Constraint(subtract(max_func, curr_func), DELTA, None))
                elif oracle_result == 1:
                    # the user prefers the curr_func over max_func. Feasible region shrinks to points where curr_func >= max_func
                    max_func = curr_func
                    self.max_row_ind = idx
                    if self.criterion == "LP":
                        self.constraints.append(Constraint(subtract(max_func, curr_func), None, DELTA)) 
                else:
                    raise Exception("Invalid Oracle Query Result")
            elif res == 0:
                # the user prefers max_func over curr_func on all feasible points, so we can ignore this row.
                continue
            else:
                raise Exception("Invalid decideQuery Result")
        
        # print(self.constraints)
        print("Number of Queries: ", self.oracle.counter)
        print("Favorite Tuple Index:", self.max_row_ind)
        print("Favorite Tuple:", self.data_frame.iloc[self.max_row_ind])
        print("Favorite Tuple Utilify:", self.oracle._get_exact_utility(max_func))

    def decideQuery(self, curr_func, curr_idx, criterion = "LP"):
        """
        Function to decide whether to query the oracle.

        Args:
        - row (pandas Series): Input row from the DataFrame.

        Returns:
        - int: Indicator the result of the query.
            Return 0: current_is below the max for all points 
        """
        max_func = self.data_frame.iloc[self.max_row_ind].tolist()
        if criterion == "bruteforce":
            return 1
        elif criterion == "LP":
            # We have to test feasibility of following two LPs
            # LP #1: Is there a point in feasible region where curr_func > (1+eps)*max_func?
            result1 = feasible(self.oracle.dimension, 
                               self.constraints + [Constraint(subtract(mult(max_func, 1 + self.eps), curr_func), None, -DELTA)],
                               self.negative_attributes)

            if result1 == False:
                # the value will not increase too much, so we can keep the current max_func
                return 0
            
            # LP #2: Is there a point in feasible region where curr_func < max_func?
            result2 = feasible(self.oracle.dimension, 
                               self.constraints + [Constraint(subtract(max_func, curr_func), DELTA, None)],
                               self.negative_attributes)
            if result2 == False:
                # we can just consider that the current function is bigger everywhere in the feasible region
                # print("Res 2")
                return 2
            else: # result2 == True:
                # we need the query
                # print("Res 1")
                return 1

            
        # elif criterion == "Minimal":
        #     ## The idea is to first find RANDOM_POINTS_NUM number of random points in the feasible region. 
        #     ## We will then compute the average absolute value difference between the utility over curr_func and max_func for these points
        #     ## If this (average distance)/(average over value curr max) is too low (< DIFF_THRESHOLD_FACTOR), then we will ignore this row as it is "too near" the current max

        #     rand_points = find_random_points(self.constraints, RANDOM_POINTS_NUM)


        else:
            raise ValueError("Unknown criterion for deciding whether to query is given")


#-- Helper Functions --#

# def find_random_points(self, )
def feasible(dimension, constraints, negative_attributes):
    # each constraint in the input set is a Constraint type object, which is a linear function represened using only coefficients.
    # Let us create a google OR solver
    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        raise Exception("Could not instantiate the LP Solver")
    var_dict = {i: solver.NumVar(-1, -DELTA, "x"+str(i)) if negative_attributes.count(i) > 0 else solver.NumVar(DELTA,1, "x"+str(i))for i in range(dimension)}
    for i in range(len(constraints)):
        cons = constraints[i]
        # print("Counter", i, cons)
        # print("Here Cons:", cons)
        expression = sum([cons.coeffs[i]*var_dict[i] for i in range(dimension)])
        # expr = " + ".join([str(cons.coeffs[i]) + "x_" + str(i) for i in range(dimension)])
        # print("expr")
        if cons.lb is not None:
            # print(expr, "-->=-- ", cons.lb)
            solver.Add(expression >= cons.lb)
        if cons.ub is not None:
            solver.Add(expression <= cons.ub)
            # print(expr, "--<=-- ", cons.ub)
    
    status = solver.Solve()
    # print(solver)
    if status == pywraplp.Solver.INFEASIBLE:
        return False
    else:
        # for v in var_dict.values():
            # print(v, "=", v.solution_value())
        return True

def add(lst1, lst2):
    assert(len(lst1) == len(lst2))
    return [lst1[i] + lst2[i] for i in range(len(lst1))]

def mult(lst: list, scalar: float):
    return [v*scalar for v in lst]

def subtract(lst1, lst2):
    return add(lst1, mult(lst2, -1))