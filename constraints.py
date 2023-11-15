class Constraint:
    def __init__(self, lst, lb, ub) -> None:
        """
        Initializes a Constraint object.

        Args:
        - lst (list): List of coefficients for the constraint.
        - lb (float): Lower bound value for the constraint.
        - ub (float): Upper bound value for the constraint.

        Stores the coefficients, lower bound, and upper bound for the constraint.
        """
        self.coeffs = lst  # Stores the coefficients for the constraint
        self.lb = lb  # Stores the lower bound for the constraint
        self.ub = ub  # Stores the upper bound for the constraint

    def __repr__(self) -> str:
        """
        Returns a string representation of the Constraint object.

        Returns:
        - str: String representation displaying the lower bound, coefficients, and upper bound.
        """
        return str(self.lb) + " <= " + str(self.coeffs) + " <= " + str(self.ub)
