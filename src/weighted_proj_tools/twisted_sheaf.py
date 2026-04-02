import numpy as np # type: ignore
from weighted_proj_tools import Weights, uniquebi, very_ample_bound


class TwistedSheaf:
    """
    Represents a twisted sheaf Ocal_{P(a)}(deg) and reduces it when possible, calculates its dimension.
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

        return self.wellformed_degree

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
            m = np.lcm.reduce(self.W.wellformed_weights)
            if self.wellformed_degree % m == 0: #.... check if deg=nm ie if m divides deg if yes then 
                G = very_ample_bound(self.W.wellformed_weights)
                #n = np.int32(np.ceil(G/m)) #by def n>G/m
                if self.wellformed_degree > 0 and self.wellformed_degree >= G: # check if degree is positive and at least G
                    return True
                else:
                    return False
            else:
                return False
        else:
            return None #do again but with self.degree
