import csv
import os

from modules.rbm import rbm

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

ALGORITMOS = ['Graphical Lasso Algorithm', 'Restricted Boltzman Machine', 'Markov Network']

def algo0():
    print(ALGORITMOS[0])
    # Read data
    X = file_reader('\data.txt') 

def algo1():
    """
    Restricted Boltzman Machine
    """
    print(ALGORITMOS[1])
    data = file_reader('data.txt')
    data.pop(0)
    rbm.execute(data)
    
def algo2():
    """
    Markov Network
    """
    print(ALGORITMOS[2])
    X = file_reader('\data.txt')
    states = ['Dormir', 'Comer', 'Correr']
    trans_matrix = [[0.1,0.3,0.6],[0.2,0.3,0.5],[0.2,0.4,0.4]]



def menu():
    print('---------------------------\n',
    'UNDIRECTED GRAPHICAL MODELS\n',
    '---------------------------\n')
    for i, algo in enumerate(ALGORITMOS):
        print("\t", i, algo)
    print("\t", 3, "Salir\n")

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
        2: algo2,
        3: exit,
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
