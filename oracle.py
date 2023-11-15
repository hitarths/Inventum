class Oracle:
    def __init__(self, utility):
        """
        Initialize the Oracle class with a utility list and set the dimension.

        Args:
        - utility (list of float): A list representing utilities for dimensions.

        Attributes:
        - utility (list of float): List containing utility (weight) values for dimensions.
        - dimension (int): Length of the utility list representing the dimension.
        - counter (int): Counter to keep track of the number of queries made.
        """
        self.utility = utility
        self.dimension = len(utility)
        self.counter = 0
    
    def query(self, p1, p2):
        """
        Compare two points based on their utility values and return the one with greater utility.

        Args:
        - p1 (list of float): First point to compare.
        - p2 (list of float): Second point to compare.

        Returns:
        - 0 if util(p1) > util(p2) else 1

        Raises:
        - ValueError: If input dimensions do not match the utility dimension.
        """
        # Check if the dimensions of the input points match the utility dimension
        if len(p1) != self.dimension or len(p2) != self.dimension:
            raise ValueError("Input dimensions do not match the utility dimension")
        
        # Increment the query counter by 1 for each query made
        self.counter += 1
        
        # Calculate the utility values for each point by performing pointwise multiplication with the utility list
        utility_p1 = sum([u * p for u, p in zip(self.utility, p1)])
        utility_p2 = sum([u * p for u, p in zip(self.utility, p2)])
        
        # Compare the utility values and return the point with greater utility
        if utility_p1 > utility_p2:
            # print("Prefer {} over {}".format(p1, p2))
            return 0
        else:
            # print("Prefer {} over {}".format(p2, p1))
            return 1
        
    def _get_exact_utility(self, p):
        return sum([u * p for u, p in zip(self.utility, p)])