import csv
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

ALGORITMOS = ['Graphical Lasso Algorithm', 'Modified Regression Algorithm', 'Markov Chain', 'Boltzman Machine']

def algo0():
    print(ALGORITMOS[0])

def algo1():
    print(ALGORITMOS[1])

def algo2():
    print(ALGORITMOS[2])

def algo3():
    print(ALGORITMOS[3])

def intro():
    cls()
    print('---------------------------\n',
    'UNDIRECTED GRAPHICAL MODELS\n',
    '---------------------------\n')
    for i, algo in enumerate(ALGORITMOS):
        print("\t", i, algo)
    print("\t" ,4, "Salir\n\n")

def switch_error():
    print('\nIngrese la opción correcta\n')

def exit():
    print('Adiós')
    quit()

def algoritmos():
    
    switch = {
        0: algo0,
        1: algo1,
        2: algo2,
        3: algo3,
        4: exit,
    }

    while True:
        opc = int(input('Ingrese su opción: '))
        switch.get(opc, switch_error)()


def file_reader(file_name):
    cwd = os.getcwd()
    data_dir = cwd + file_name
    data = []
    with open(data_dir) as data_file:
        csv_reader = csv.reader(data_file, delimiter=',')
        for row in csv_reader:
            data.append(row)
    return data


def main():
    intro()
    X = file_reader('\data.txt')
    algoritmos()
    
 

if __name__=='__main__':
    main() 