import numpy as np # type: ignore
from weighted_proj_tools import Weights, LinearSystem, very_ample_bound

class WeightedProjectiveSpace:
    
    def __init__(self, W:Weights):
        self.W = W # weights
        self.calculate_embedding_dimension()

    def calculate_embedding_dimension(self)->int: #improve this also
        m = np.lcm.reduce(self.W.wellformed_weights)
        G = very_ample_bound(self.W.wellformed_weights)

        self.m = m
        self.G = G

        if G/m < 0: # n>0 and n>G/m is true for all n>=1
            n = 1
            deg_mn = m  
        else: # n>0 and n>G/m is true for all n>=ceil(G/m)
            n = np.int32(np.ceil(G/m))
            deg_mn = n*m

        linsys = LinearSystem(Weights(self.W.wellformed_weights), np.int32(deg_mn))
        self.embedding_linear_system = linsys
        N = linsys.dimension
        self.embedding_dimension = N  
        return N
        # return the dimension of the projective space in which it embeds into

