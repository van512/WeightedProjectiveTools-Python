import numpy as np # type: ignore

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
        self.sub_gcd = [np.gcd.reduce(np.delete(self.reduced_weights, i)) for i in range(len(self.reduced_weights))]

        # Compute the least common multiples (LCM) of these GCDs
        self.sub_lcm_of_sub_gcd = [np.lcm.reduce(np.delete(self.sub_gcd, i)) for i in range(len(self.sub_gcd))]
       
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
    