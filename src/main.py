ALGORITMOS = ['ALGO1', 'ALGO2', 'ALGO3']

def algo0():
    print('Algoritmo 0')

def algo1():
    print('Algoritmo 1')

def algo2():
    print('Algoritmo 2')

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