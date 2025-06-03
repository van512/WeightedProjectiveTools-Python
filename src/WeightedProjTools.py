import numpy as np # type: ignore
from sympy.solvers.diophantine import diophantine # type: ignore
from sympy import symbols, solve, parse_expr # type: ignore
from sympy.utilities.lambdify import lambdify # type: ignore
from functools import lru_cache
from itertools import combinations
from numpy.typing import NDArray # type: ignore
from scipy.special import comb # type: ignore
#import time


"""Provides some functions and classes to perform calculations in the context of weighted projective space."""


def dimrec(a: list, d: int) -> int:
    """
    Optimized recursive function with memoization to calculate dim C_a[X]_d.
    """

    @lru_cache(maxsize=None)
    def helper(i: int, remaining: int) -> int:
        if i == len(a):
            return 1 if remaining == 0 else 0
        
        total = 0
        # Try all multiples of a[i] that do not exceed 'remaining'
        for k in range(0, remaining + 1, a[i]):
            total += helper(i + 1, remaining - k)
        
        return total

    return helper(0, d)


def uniquebi(a:int, s:int, d:int, verbose=False):
    """Solves the Diophantine equation d = b_i(d)a_i+c_i(d)s_i with the notation of the thesis
    Input Variables :
    a=a_i, s=s_i, d=degree
    Returns :
    The unique b=b_i(d) such that 0<=b<s
    """
    # Define symbols for b, c, x integers
    b, c, x = symbols("b, c, x", integer=True)
    syms = (b, c)

    # Define the Diophantine equation to solve: a*b + s*c = d
    equ = a * b + s * c - d
    
    # Solve the equation for b and c, getting a solution with a symbolic parameter
    solutions, = diophantine(equ, syms=(b, c))

    # Extract and define the symbolic parameter (usually t_0) from the solution
    parameters = set().union(*(s.free_symbols for s in solutions))
    param_t = symbols(str(list(parameters)[0]))

    # Extract expressions for b and c from the solution tuple
    expr_b = str(list(solutions)[0])
    expr_c = str(list(solutions)[1])

    # Parse b and c expressions into usable SymPy expressions
    parsed_b = parse_expr(expr_b, transformations="all")
    parsed_c = parse_expr(expr_c, transformations="all")

    # Solve the expression for b in terms of the parameter t
    sol_t = solve(parsed_b, param_t)[0]
    
    # Create a lambda function to evaluate t using NumPy
    lambd_t = lambdify(x, sol_t * x, 'numpy')
    t_val = int(lambd_t(1))  # Get the integer value of t

    # Substitute t_val into the expression for b
    b_val = parsed_b.subs({param_t: t_val})
    
    # Adjust t_val to ensure 0 <= b < s by incrementing/decrementing t
    i = 0
    while b_val >= s or b_val < 0:
        t_val = t_val - 1 * (i - 1) + 2 * i  # Alternate decrement and increment
        b_val = parsed_b.subs({param_t: t_val})
        i += 1

    # Calculate the corresponding c value
    c_val = parsed_c.subs({param_t: t_val})

    # Debug prints 
    if verbose == True:
      print(f"{d}={b_val}*{a}+{c_val}*{s}={b_val*a+c_val*s}")
      print(b_val < s)
      print(b_val >= 0)

    # Return the valid b value
    return b_val


def reduce_arr(func, arr: list) -> list:
    """
    Applies a reduction function to the array with each element individually removed.
    
    Parameters:
    func: A function with a 'reduce' method (e.g., numpy's ufuncs like np.gcd, np.lcm).
    arr (list): Input list of numbers.
    
    Returns:
    output: A list where each entry is the result of applying 'func' to the array with one element left out.
    """
    
    output = []
    
    # Loop through each index of the array
    for i in range(len(arr)):
        # Create a new array with the i-th element removed
        arrhat = np.concatenate((arr[:i], arr[i+1:])).astype(int)
        
        # Apply the reduction function to the modified array and store the result
        output.append(func.reduce(arrhat))
    
    # Return the list of results
    return output


def very_ample_bound(weights:NDArray[np.int32]):
    # G(Q), G(a) for us

    # Function to calculate LCM of a list using numpy's np.lcm.reduce
    @lru_cache(None)  # Memoize this function to avoid recomputing the same sublist
    def memoized_lcm(weights_sublist):
        return np.lcm.reduce(weights_sublist)

    def sum_lcms(nu): #nu = length of weights_sublist
        total_lcm_sum = 0
        for weights_sublist in combinations(weights, nu):
            # Sum the LCM of the elements of the sublist of weights
            total_lcm_sum += memoized_lcm(weights_sublist)
        return total_lcm_sum

    r = len(weights)-1 
    if r==0:
        return -weights[0]
    elif r>0:
        temp_sum = 0
        for nu in range(2,r+1+1):
            temp_sum += sum_lcms(nu)/comb(r-1,nu-2)
        return -weights.sum() + temp_sum/r




class Weights:
    """
    Represents a list of weights and computes its reduced and well-formed equivalents
    """
    def __init__(self, weights: list):
        weights.sort() # sort the weights 
        self.weights = np.array(weights)
        
        # Compute the greatest common divisor (GCD) of all weights
        self.gcd = np.array(np.gcd.reduce(weights))
        
        # Compute the reduced weights by dividing each weight by the GCD
        self.reduced_weights = np.array((weights / self.gcd).astype(int))
        
        # Compute GCDs of the reduced weights with each element removed
        self.sub_gcd = np.array(reduce_arr(np.gcd, self.reduced_weights))   

        # Compute the least common multiples (LCM) of these GCDs
        self.sub_lcm_of_sub_gcd = np.array(reduce_arr(np.lcm, self.sub_gcd)) 
       
        # Calculate the well-formed weights
        self.wellformed_weights = np.array((self.reduced_weights / self.sub_lcm_of_sub_gcd).astype(int))
        
        # Compute the LCM of sub_gcd
        self.lcm_of_sub_gcd = np.array(np.lcm.reduce(self.sub_gcd))
       
        # lcm of the weights
        self.lcm = np.array(np.lcm.reduce(self.weights))
        #m = np.array(np.lcm.reduce(self.W.wellformed_weights))

    def is_reduced(self):
        """
        Check if the weights are reduced.
        """
        return self.weights == self.reduced_weights
    
    def is_wellformed(self):
        """
        Check if the weights are well-formed.
        """
        return self.weights == self.wellformed_weights
    

class TwistedSheaf:
    """
    Represents a twisted sheaf \Ocal_{P(a)}(deg) and reduces it when possible, calculates its dimension.
    """
    def __init__(self, W: Weights, degree: int):
        self.W = W  # Associated weight class
        self.degree = degree  # Original degree before weight reduction
        self.calculate_well_formed_degree()  # Calculate the well-formed degree if possible


    def is_deg_reducible(self):
        temp = self.degree / self.W.gcd # temporary reduced degree
        precision = 1e-10
        
        # Check if the reduced degree temp is effectively an integer
        if abs(temp - int(temp)) < precision:
            return True
        else:
            return False

    def calculate_well_formed_degree(self):
        """
        Computes the well-formed degree if the degree can be reduced.
        """
        if self.is_deg_reducible():

            # Set the reduced degree
            self.reduced_degree = int(self.degree / self.W.gcd)
            
            # Calculate unique bi values for each (ai, si) pair
            self.B = [uniquebi(ai, si, self.reduced_degree) for ai, si in zip(self.W.reduced_weights, self.W.sub_gcd)]
            
            # Compute the well-formed degree using the formula: phi(d) in the thesis
            self.wellformed_degree = (self.reduced_degree - np.dot(self.B, self.W.reduced_weights)) / self.W.lcm_of_sub_gcd
        
        else:
            self.wellformed_degree = None

    def is_ample(self):
        if self.degree == self.W.lcm:  #m, I think this works even if degree is not reduced or well-formed but not sure.
            return True
        else:
            return False

    def is_very_ample(self): # place holders for now
        """
        Check if the twisted sheaf is very ample.
        """
        if self.wellformed_degree is not None:
            if self.wellformed_degree: #.... check if deg=nm ie if m divides deg if yes then 
                n = 0
                if n > 0 and n > very_ample_bound(self.W.wellformed_weights)/self.W.lcm: #change lcm to wellformed-weights lcm
                    return True
                else:
                    return False
            else:
                return False
        else:
            return None #do again but with self.degree


   
class LinearSystem(TwistedSheaf):
    def __init__(self, degree: int, weights: Weights):
        super().__init__(weights, degree)
        self.calculate_dimension()  # Calculate the dimension of the twisted sheaf  

    def calculate_dimension(self):
        """
        Computes the dimension of the linear system.
        """
       # Calculate the well-formed degree if possible
        self.calculate_well_formed_degree()

        # Computes the dimension on the normalized weights and degree (normalized = reduced + well-formed)
        if self.wellformed_degree is not None:
            self.dimension = dimrec(self.W.wellformed_weights, self.wellformed_degree)-1
        else :
            self.dimension = dimrec(self.W.weights, self.degree)-1
    
 
class WeightedProjectiveSpace:
    
    def __init__(self, W:Weights):
        self.W = W # weights
        self.embedding_dimension = self.embeds_into()

    def embeds_into(self)->int: #improve this also
        m = np.array(np.lcm.reduce(self.W.wellformed_weights))
        G = very_ample_bound(self.W.wellformed_weights)
        n =  np.int64(np.ceil(G/m))
        self.m = m
        self.G = G
        self.nGm1 = G/m
        self.nGm = n
        print(n, G/m)
        if n < 1:
            deg_mn = m  # n = ceil(G/m) = 1
        else:
            deg_mn = n*m
        linsys = LinearSystem(Weights(self.W.wellformed_weights), np.array(np.int64(deg_mn)))
        self.embedding_linear_system = linsys
        N = linsys.dimension-1
        return N
        # return the dimension of the projective space in which it embeds into

