import csv
import os
import numpy as np
import seaborn as sns
from sklearn.covariance import GraphicalLasso
from modules.rbm import rbm
from modules.undirected_graphical_models import UndirectedGraphicalModels

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

ALGORITMOS = ['Graphical Lasso Algorithm', 'Restricted Boltzman Machine']

def algo0():
    print(ALGORITMOS[0])
    # Read data
    data = file_reader('\data.txt') 
    data.pop(0)
    ugm = UndirectedGraphicalModels()
    cov, prec = UndirectedGraphicalModels.graphical_lasso(ugm, data)
    ax = sns.heatmap(cov, cmap="YlGnBu")
    fig = ax.get_figure()
    fig.savefig("imgs/covarianza.png") 

    ax = sns.heatmap(prec, cmap="YlGnBu")
    fig = ax.get_figure()
    fig.savefig("imgs/precision.png")
    print("Covarianza: ")
    print(cov)
    print("\nPrecisión: ")
    print(prec)

    # Se prueba 
    true_cov = np.array([[0.8, 0.0, 0.2, 0.0],[0.0, 0.4, 0.0, 0.0],[0.2, 0.0, 0.3, 0.1],[0.0, 0.0, 0.1, 0.7]])
    np.random.seed(0)
    X = np.random.multivariate_normal(mean=[0, 0, 0, 0],cov=true_cov,size=200)
    covsk = GraphicalLasso().fit(X)
    ax = sns.heatmap(covsk.covariance_, cmap="YlGnBu")
    fig = ax.get_figure()
    fig.savefig("imgs/covarianzasklearn.png")
    

def algo1():
    """
    Restricted Boltzman Machine
    """
    print(ALGORITMOS[1])
    data = file_reader('data.txt')
    data.pop(0)
    rbm.execute(data)

def menu():
    print('---------------------------\n',
    'UNDIRECTED GRAPHICAL MODELS\n',
    '---------------------------\n')
    for i, algo in enumerate(ALGORITMOS):
        print("\t", i, algo)
    print("\t", 2, "Salir\n")

def intro():
    # cls()
    menu()

def switch_error():
    print('\nIngrese la opción correcta\n')
    menu()

def exit():
    print('Adiós')
    quit()

def algoritmos():
    
    switch = {
        0: algo0,
        1: algo1,
        2: exit,
    }

    while True:
        opc = int(input('Ingrese su opción: '))
        switch.get(opc, switch_error)()


def file_reader(file_name):
    cwd = os.getcwd()
    data_dir = cwd + '/' + file_name
    data = []
    with open(data_dir) as data_file:
        csv_reader = csv.reader(data_file, delimiter=',')
        for row in csv_reader:
            data.append(row)
    return data


def main():
    intro()
    algoritmos()
    
 

if __name__=='__main__':
    main() 
