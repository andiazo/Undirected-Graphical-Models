import csv
import os
import numpy as np
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
    print(cov)
    print("------------\n",prec)

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
