from modules import rbm
import os
import csv

def file_reader(file_name):
    cwd = os.getcwd()
    data_dir = cwd + '\\' + file_name
    data = []
    with open(data_dir) as data_file:
        csv_reader = csv.reader(data_file, delimiter=',')
        for row in csv_reader:
            for i in range(0, len(row)):
                row[i] = int(row[i])
            data.append(row)
    print(data)
    return data

ALGORITMOS = ['ALGO1', 'ALGO2', 'ALGO3']

def algo0():
    print('Algoritmo 0')

def algo1():
    print('Algoritmo 1')

def algo2():
    print('Restricted Boltzman Machines')
    data = file_reader('data.txt')
    rbm.execute(data)

def intro():
    print('UNDIRECTED GRAPHICAL MODELS')
    for i, algo in enumerate(ALGORITMOS):
        print(i, algo)
    
def algoritmos():
    error = 'Ingrese la opción correcta'
    
    switch = {
        0: algo0,
        1: algo1,
        2: algo2,
        3: quit,
    }

    while True:
        opc = int(input('Ingrese su opción: '))
        switch.get(opc, error)()


def main():
    intro()
    algoritmos()


if __name__=='__main__':
    main() 
