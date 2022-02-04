import numpy as np
from sklearn.linear_model import lars_path

class UndirectedGraphicalModels():
    
    def __init__(self) -> None:
        pass
    
    # Grafos no dirigidos
    # Cadenas de Markov
        
        
    def modified_regression( X, alpha=0.01, max_iter = 100, convg_threshold=0.001 ):
        ''' This function computes the graphical lasso algorithm as outlined in Sparse inverse covariance estimation with the
            graphical lasso (2007).
            
        inputs:
            X: the data matrix, size (nxd)
            alpha: the coefficient of penalization, higher values means more sparseness.
            max_iter: maximum number of iterations
            convg_threshold: Stop the algorithm when the duality gap is below a certain threshold.
    
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
        
        if alpha == 0:
            return cov_estimator( X )
        n_features = X.shape[1]

        mle_estimate_ = cov_estimator(X)
        covariance_ = mle_estimate_.copy()
        precision_ = np.linalg.pinv( mle_estimate_ )
        indices = np.arange( n_features)
        for i in xrange( max_iter):
            for n in range( n_features ):
                sub_estimate = covariance_[ indices != n ].T[ indices != n ]
                row = mle_estimate_[ n, indices != n]
                #solve the lasso problem
                _, _, coefs_ = eq_19( sub_estimate, row, Xy = row, Gram = sub_estimate, 
                                            alpha_min = alpha/(n_features-1.), copy_Gram = True,
                                            method = "lars")
                coefs_ = coefs_[:,-1] #just the last please.
            #update the precision matrix.
                precision_[n,n] = 1./( covariance_[n,n] 
                                        - np.dot( covariance_[ indices != n, n ], coefs_  ))
                precision_[indices != n, n] = - precision_[n, n] * coefs_
                precision_[n, indices != n] = - precision_[n, n] * coefs_
                temp_coefs = np.dot( sub_estimate, coefs_)
                covariance_[ n, indices != n] = temp_coefs
                covariance_[ indices!=n, n ] = temp_coefs
            
            #if test_convergence( old_estimate_, new_estimate_, mle_estimate_, convg_threshold):
            if np.abs( _dual_gap( mle_estimate_, precision_, alpha ) )< convg_threshold:
                    break
        else:
            #this triggers if not break command occurs
            print("The algorithm did not coverge. Try increasing the max number of iterations.")
        
        return covariance_, precision_

    def eq_19(w,beta,s):
        '''
            soluciona W11 * Beta - s12 = 0
        '''
        return 0

    def cov_estimator(self, X ):
        return np.cov( X.T) 
        
    # Este metodo es igual al 19.1 pero solucionando otra ecuación
    def graphical_lasso( X, alpha=0.01, max_iter = 100, convg_threshold=0.001 ):
        """ This function computes the graphical lasso algorithm as outlined in Sparse inverse covariance estimation with the
            graphical lasso (2007).
            
        inputs:
            X: the data matrix, size (nxd)
            alpha: the coefficient of penalization, higher values means more sparseness.
            max_iter: maximum number of iterations
            convg_threshold: Stop the algorithm when the duality gap is below a certain threshold.
        """
        
        if alpha == 0:
            return cov_estimator( X )
        n_features = X.shape[1]

        mle_estimate_ = cov_estimator(X)
        covariance_ = mle_estimate_.copy()
        precision_ = np.linalg.pinv( mle_estimate_ )
        indices = np.arange( n_features)
        for i in xrange( max_iter):
            for n in range( n_features ):
                sub_estimate = covariance_[ indices != n ].T[ indices != n ]
                row = mle_estimate_[ n, indices != n]
                #solve the lasso problem
                _, _, coefs_ = lars_path( sub_estimate, row, Xy = row, Gram = sub_estimate, 
                                            alpha_min = alpha/(n_features-1.), copy_Gram = True,
                                            method = "lars")
                coefs_ = coefs_[:,-1] #just the last please.
            #update the precision matrix.
                precision_[n,n] = 1./( covariance_[n,n] 
                                        - np.dot( covariance_[ indices != n, n ], coefs_  ))
                precision_[indices != n, n] = - precision_[n, n] * coefs_
                precision_[n, indices != n] = - precision_[n, n] * coefs_
                temp_coefs = np.dot( sub_estimate, coefs_)
                covariance_[ n, indices != n] = temp_coefs
                covariance_[ indices!=n, n ] = temp_coefs
            
            #if test_convergence( old_estimate_, new_estimate_, mle_estimate_, convg_threshold):
            if np.abs( _dual_gap( mle_estimate_, precision_, alpha ) )< convg_threshold:
                    break
        else:
            #this triggers if not break command occurs
            print("The algorithm did not coverge. Try increasing the max number of iterations.")
        
        return covariance_, precision_
        
        
    def test_convergence(self, previous_W, new_W, S, t):
        d = S.shape[0]
        x = np.abs( previous_W - new_W ).mean()
        print(x - t*( np.abs(S).sum() + np.abs( S.diagonal() ).sum() )/(d*d-d))
        if np.abs( previous_W - new_W ).mean() < t*( np.abs(S).sum() + np.abs( S.diagonal() ).sum() )/(d*d-d):
            return True
        else:
            return False

    def _dual_gap(self, emp_cov, precision_, alpha):
        """Expression of the dual gap convergence criterion

        The specific definition is given in Duchi "Projected Subgradient Methods
        for Learning Sparse Gaussians".
        """
        gap = np.sum(emp_cov * precision_)
        gap -= precision_.shape[0]
        gap += alpha * (np.abs(precision_).sum()
                        - np.abs(np.diag(precision_)).sum())
        return gap 
