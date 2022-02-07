from __future__ import print_function
import numpy as np

class rbm:
  
  def __init__(self, num_visible, num_hidden):
    self.num_hidden = num_hidden
    self.num_visible = num_visible
    self.debug_print = True

    # Inicializar el peso de la matriz cuyas dimensiones son: [num_vi, num_hi]
    # Se usa una distribucion uniforme de la forma :
    # 1) -sqrt(6. / (num_hidden + num_visible))
    # 2) sqrt(6. / (num_hidden + num_visible)).
    np_rng = np.random.RandomState(1234)

    self.weights = np.asarray(np_rng.uniform(
			low=-0.1 * np.sqrt(6. / (num_hidden + num_visible)),
                       	high=0.1 * np.sqrt(6. / (num_hidden + num_visible)),
                       	size=(num_visible, num_hidden)))


    # Insercion de los pesos a traves de unidades de sesgo
    # en la primera columna y fila.
    self.weights = np.insert(self.weights, 0, 0, axis = 0)
    self.weights = np.insert(self.weights, 0, 0, axis = 1)

  # Funcion de entranmiento para la red neuronal
  def train(self, data, max_epochs = 500, learning_rate = 0.1):
    """
    Parametros:
    1) data := Una matriz en la que cada fila es un ejemplo de entrenamiento que consiste en los estados de las unidades visibles.   
    2) max_epochs = Numero maximo de epocas, por defecto se usa 500
    3) learning_rate =  taza de aprendizaje, por defecto 0.1 
    """

    num_examples = data.shape[0]

    # Insertar unidades de sesgo con 1 la primera columna
    data = np.insert(data, 0, 1, axis = 1)

    for epoch in range(max_epochs):      
      # Mostras las unidades ocultas
      pos_hidden_activations = np.dot(data, self.weights)      
      pos_hidden_probs = self._logistic(pos_hidden_activations)
      pos_hidden_probs[:,0] = 1 
      pos_hidden_states = pos_hidden_probs > np.random.rand(num_examples, self.num_hidden + 1)
      
       #Se utilizando las probabilidades de activación de los estados ocultos, no los estados ocultos en sí, al calcular las asociaciones.
      
      pos_associations = np.dot(data.T, pos_hidden_probs)

      # Reconstruccion de las unidades visibles y tomar muestras de las unidades ocultas.

      neg_visible_activations = np.dot(pos_hidden_states, self.weights.T)
      neg_visible_probs = self._logistic(neg_visible_activations)
      neg_visible_probs[:,0] = 1 
      neg_hidden_activations = np.dot(neg_visible_probs, self.weights)
      neg_hidden_probs = self._logistic(neg_hidden_activations)
    
      neg_associations = np.dot(neg_visible_probs.T, neg_hidden_probs)

      # Actualizacion de pesos.
      self.weights += learning_rate * ((pos_associations - neg_associations) / num_examples)

      error = np.sum((data - neg_visible_probs) ** 2)
      if self.debug_print:
        print("Epoch %s: error is %s" % (epoch, error))

  def run_visible(self, data):
    """
   Despues ser entrenado se ejecuta la red en un conjunto de unidades visibles, para obtener una muestra de las unidades ocultas.
    Parametros
    
    1) data: Matriz en la que cada fila está formada por los estados de las unidades visibles.
    
    Retorna
    
    1) hidden_states: Matriz en la que cada fila está formada por las unidades ocultas activadas a partir de las unidades visibles en la matriz de datos introducida.
    """
    
    num_examples = data.shape[0]
    
    # Crear una matriz, donde cada fila será las unidades ocultas (más una unidad de sesgo) muestreadas de un ejemplo de entrenamiento.
    hidden_states = np.ones((num_examples, self.num_hidden + 1))
    
    # Insertar unidades de sesgo de 1 en la primera columna de datos.
    data = np.insert(data, 0, 1, axis = 1)

    # Calcular las activaciones de las unidades ocultas.
    hidden_activations = np.dot(data, self.weights)
    # Calcula las probabilidades de encender las unidades ocultas.
    hidden_probs = self._logistic(hidden_activations)
    # Enciender las unidades ocultas con sus probabilidades especificadas.Enciende las unidades ocultas con sus probabilidades especificadas.
    hidden_states[:,:] = hidden_probs > np.random.rand(num_examples, self.num_hidden + 1)

    hidden_states = hidden_states[:,1:]
    return hidden_states
    
  
  def run_hidden(self, data):
    """
    Despues de ser entrenado, ejecuta la red en un conjunto de unidades ocultas, para obtener una muestra de las unidades visible
    
    Parametros
   1) data: Matriz en la que cada fila está formada por los estados de las unidades visibles.
    
    Retorna
    
    1) visible_states: Matriz en la que cada fila está formada por las unidades visibles activadas a partir de las unidades ocultas en la matriz de datos introducida.
    """

    num_examples = data.shape[0]

    # Crear una matriz, en la que cada fila será las unidades visibles (más una unidad de sesgo) muestreadas de un ejemplo de entrenamiento.
    visible_states = np.ones((num_examples, self.num_visible + 1))
    data = np.insert(data, 0, 1, axis = 1)

    # Calcular las activaciones de las unidades visibles
    visible_activations = np.dot(data, self.weights.T)
    # Calcular las probabilidades de encender las unidades visibles.
    visible_probs = self._logistic(visible_activations)
    # Encender las unidades visibles con sus probabilidades especificadas
    visible_states[:,:] = visible_probs > np.random.rand(num_examples, self.num_visible + 1)
    
    visible_states = visible_states[:,1:]
    return visible_states
    
  def daydream(self, num_samples):
    """
    Inicializar aleatoriamente las unidades visibles una vez, y comenzar a ejecutar pasos de muestreo de Gibbs alternados (donde cada paso consiste en actualizar todas las unidades ocultas, y luego actualizar todas las unidades visibles), tomando una muestra de las unidades visibles en cada paso.
    
    Parametros
    1) num_samples: numero de muestras
    
    Retorna
    
    1) samples: Matriz donde cada fila es una muestra de las unidades visibles producidas mientras la red soñaba despierta.
    """

    samples = np.ones((num_samples, self.num_visible + 1))

    # Take the first sample from a uniform distribution.
    samples[0,1:] = np.random.rand(self.num_visible)

    # Iniciar el muestreo alternativo de Gibbs.
    for i in range(1, num_samples):
      visible = samples[i-1,:]

      # Calcular las activaciones de las unidades ocultas.
      hidden_activations = np.dot(visible, self.weights)      
      # Calcular las probabilidades de encender las unidades ocultas.
      hidden_probs = self._logistic(hidden_activations)
      # Encender las unidades ocultas con sus probabilidades especificadas.
      hidden_states = hidden_probs > np.random.rand(self.num_hidden + 1)
      hidden_states[0] = 1

      # Recalcular las probabilidades de que las unidades visibles estén encendidas.
      visible_activations = np.dot(hidden_states, self.weights.T)
      visible_probs = self._logistic(visible_activations)
      visible_states = visible_probs > np.random.rand(self.num_visible + 1)
      samples[i,:] = visible_states

    
    return samples[:,1:]        
      
  def _logistic(self, x):
    return 1.0 / (1 + np.exp(-x))

if __name__ == '__main__':
  r = rbm(num_visible = 6, num_hidden = 2)
  training_data = np.array([[1,1,1,0,0,0],[1,0,1,0,0,0],[1,1,1,0,0,0],[0,0,1,1,1,0], [0,0,1,1,0,0],[0,0,1,1,1,0]])
  r.train(training_data, max_epochs = 3000)
  print(r.weights)
  user = np.array([[0,0,0,1,1,0]])
  print(r.run_visible(user))
