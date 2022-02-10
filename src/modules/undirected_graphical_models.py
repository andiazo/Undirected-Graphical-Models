import numpy as np
from sklearn.linear_model import lars_path

class UndirectedGraphicalModels():
    
    def __init__(self) -> None:
        pass
        
    def graphical_lasso(self, data, alpha=0.01, max_iter = 100, convg_threshold=0.001 ):
        """ Esta función implementa el algoritmo 19.2
            
        Parametros:
            data: Los datos de entrada
            alpha: Coeficiente de penalización
            max_iter: Número máximo de iteraciones
            convg_threshold: Umbral de convergencia.
        """
        p_data = []
        for row in data:
            i_map = map(float, row)
            i_list = list(i_map)
            p_data.append(i_list)

        X = np.array(p_data) 
        
        if alpha == 0:
            return self.cov_estimator( X )
        n_features = X.shape[1]

        mle_estimate_ = self.cov_estimator(X)
        covariance_ = mle_estimate_.copy()
        precision_ = np.linalg.pinv( mle_estimate_ )
        indices = np.arange( n_features)
        for i in range( max_iter):
            for n in range( n_features ):
                sub_estimate = covariance_[ indices != n ].T[ indices != n ]
                row = mle_estimate_[ n, indices != n]
                # Soluciona el problema del Lasso
                _, _, coefs_ = lars_path( sub_estimate, row, Xy = row, Gram = sub_estimate, 
                                            alpha_min = alpha/(n_features-1.), copy_Gram = True,
                                            method = "lars")
                coefs_ = coefs_[:,-1] 
                
                # Actualiza la matriz de precisión.
                precision_[n,n] = 1./( covariance_[n,n] 
                                        - np.dot( covariance_[ indices != n, n ], coefs_  ))
                precision_[indices != n, n] = - precision_[n, n] * coefs_
                precision_[n, indices != n] = - precision_[n, n] * coefs_
                temp_coefs = np.dot( sub_estimate, coefs_)
                covariance_[ n, indices != n] = temp_coefs
                covariance_[ indices!=n, n ] = temp_coefs
        
            if np.abs( self._dual_gap( mle_estimate_, precision_, alpha ) )< convg_threshold:
                    break
        else:
            print("Alcanzo el numero máximo de iteraciones, el algoritmo no converge.")
        
        return covariance_, precision_
        
    def cov_estimator(self, X ):
        return np.cov( X.T) 

    def _dual_gap(self, emp_cov, precision_, alpha):
        gap = np.sum(emp_cov * precision_)
        gap -= precision_.shape[0]
        gap += alpha * (np.abs(precision_).sum()
                        - np.abs(np.diag(precision_)).sum())
        return gap 
