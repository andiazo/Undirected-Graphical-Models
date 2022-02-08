from msilib.schema import Error
import numpy as np
import random 

class MarkovChain():

    def __init__(self, states=None, trans_matrix = None):
        """
        Inicializa una instancia de una Cadena de Markov

        Parametros
        ----------
        states: Lista de estados de la cadena
        trans_matrix: Matriz de transiciones, sus componentes deben sumar 1
        """
        self.states = states

        # Verificar que la matriz sea de probabilidades
        if (int(np.sum(np.array(trans_matrix))) == np.shape(np.array(trans_matrix))[0]):
            self.trans_matrix = np.array(trans_matrix)
        else: 
            raise Exception('Value Input', 'Trans_Matrix tiene que ser matriz de probabilidades')