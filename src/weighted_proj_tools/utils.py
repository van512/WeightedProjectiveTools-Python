import numpy as np # type: ignore
from sympy.solvers.diophantine import diophantine # type: ignore
from sympy import symbols, solve, parse_expr # type: ignore
from sympy.utilities.lambdify import lambdify # type: ignore
from functools import lru_cache
from itertools import combinations
from numpy.typing import NDArray # type: ignore
from scipy.special import comb # type: ignore


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


#### the following are not used anymore, but kept for reference

def very_ample_bound_recursive(weights: NDArray[np.int32]) -> float: # slightly slower than the iterative version
    # Convert weights to tuple for hashing
    weights_tuple = tuple(sorted(weights))

    @lru_cache(maxsize=None)
    def _helper(w: tuple[int, ...]) -> float:
        r = len(w) - 1
        if r == 0:
            return -w[0]
        total = 0.0
        for i in range(r + 1):
            # Remove i-th element without recreating full array
            w_hat = w[:i] + w[i+1:]
            total += _helper(w_hat)
        m = np.lcm.reduce(np.array(w, dtype=int))
        return (total + m) / r

    return _helper(weights_tuple)


def reduce_arr(func, arr: list) -> list: #now obsolete
    """
    Applies a reduction function to the array with each element individually removed.
    
    Parameters:
    func: A function with a 'reduce' method (e.g., numpy's ufuncs like np.gcd, np.lcm).
    arr (list): Input list of numbers.
    
    Returns:
    output: A list where each entry is the result of applying 'func' to the array with one element left out.
    """
    if len(arr) <= 1:
        raise ValueError("Array must have more than one element to perform reduction.")

    arr = np.array(arr, dtype=int)
    return [func.reduce(np.delete(arr, i)) for i in range(len(arr))]