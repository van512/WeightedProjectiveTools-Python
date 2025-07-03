from weighted_proj_tools import Weights, TwistedSheaf, dimrec

class LinearSystem:
    def __init__(self, W: Weights, degree: int):
        self.sheaf = TwistedSheaf(W, degree)
        self.calculate_dimension()  # Calculate the dimension of the twisted sheaf  

    def calculate_dimension(self):
        """
        Computes the dimension of the linear system.
        """
        # Computes the dimension on the normalized weights and degree (normalized = reduced + well-formed)
        if self.sheaf.wellformed_degree is not None:
            self.dimension = dimrec(self.sheaf.W.wellformed_weights, self.sheaf.wellformed_degree)-1
        else :
            self.dimension = dimrec(self.sheaf.W.weights, self.sheaf.degree)-1
            
        return self.dimension