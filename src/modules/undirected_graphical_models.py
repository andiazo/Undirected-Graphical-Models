class UndirectedGraphicalModels():
    
    def __init__(self) -> None:
        pass

    def algo1(self):
        '''
        -------------------------------------------------------------------
        Algorithm 19.1 A Modified Regression Algorithm for Estimation of an 
        Undirected Gaussian Graphical Model with Known Structure.
        -------------------------------------------------------------------
            1. Initialize W = S
            2. Repeat for j = 1,2,...,p,1,2,...,p... until convergence:
                a. Partition the matrix W into part 1: all but the jth row and
                column, and part 2: the jth row and column.
                b. Solve W_11*beta* - s_12* = 0 for the unconstrained edge parameters
                beta*, using the reduced system of equations as in (19.19). Obtain
                beta (beta gorro) by padding beta gorro * with zeros in appropiate 
                positions.
                c. Update w12 = W11 beta gorro
            3. In the final cycle (for each j) solve for teta_12 gorro = -beta gorro . teta gorro _22,
            with 1/tetagorro_22 = s22 - w.T_12 . beta gorro
        '''

    # def empirical_covariance_matrix():
    #     S = (1/N)*sum((x[i] - x_mean)*(x[i] - x_mean).T)
    #     return S

    def algo2(self):
        '''
        -------------------------------------------------------------------
        Algorithm 19.2 Graphical Lasso
        -------------------------------------------------------------------
        1. Initialize W = S + λI. The diagonal of W remains unchanged in
        what follows.
        2. Repeat for j = 1, 2, . . . p, 1, 2, . . . p, . . . until convergence:

        [CONTINUE...]

        '''
        pass

