#!/usr/bin/env python
# coding: utf-8

# Integrantes:
# Ignacio Toledo
# Emilia Berwart
# Alfonso Pinto
# Pablo Gómez

# Se debe ejecutar el codigo con el archivo input.txt en la misma carpeta.

# Importamos librerías de python con las cuales trabajaremos
import sys
import numpy as np

# Aquí vamos a definir estaenlaberito
def estaEnLaberinto(tNodo, lLaberinto):
    n = len(lLaberinto) #Vamos a obtener la cantidad de filas
    m = len(lLaberinto[0]) #Vamos a obtener la cantidad de columnas
    return 0 <= tNodo[0] < n and 0 <= tNodo[1] < m
  #Entrega el return, comprueba los tnodo

#
# Función AEstrella: Función de recorrido del laberinto desde tInicio hasta tTermino utilizando técnica A*
# tInicio: recibe una tupla con la coordenada (fila, columna) del nodo de inicio del laberinto
# tTermino: recibe una tupla con la coordenada (fila, columna) del nodo de inicio del laberinto
# lLaberinto: recibe una matriz (lista n x m) con el laberinto a recorrer
# Retorna lCaminoSolucion: una lista de tuplas (fila, columna) con el camino solución
#   

def AEstrella(tInicio, tTermino, lLaberinto):
    # Metodo Best First SEARCH
    # Definir función heurística (puede ser la distancia Manhattan)
    def f_heuristica(nodo):
        return abs(nodo[0] - tTermino[0]) + abs(nodo[1] - tTermino[1])
    
    lista_abierta = [(tInicio, 0)]  # (nodo, costo acumulado)
    lista_cerrada = set()
    padres = {}
    
    while lista_abierta:
      # Seleccionar el nodo actual de la lista abierta que tiene el menor costo acumulado sumado la funcion heurística evaluada en ese punto.
        nodo_actual, costo_acumulado = min(lista_abierta, key=lambda x: x[1] + f_heuristica(x[0]))
      
        lista_abierta.remove((nodo_actual, costo_acumulado))
      
        lista_cerrada.add(nodo_actual)
        
        if nodo_actual == tTermino:
            # Reconstruir camino desde tInicio hasta tTermino
            camino = [nodo_actual]
            while nodo_actual != tInicio:
                nodo_actual = padres[nodo_actual]
                # Se añaden al principio de la lista camino los nodos previos del arreglo padres.
                camino.insert(0, nodo_actual)
            return camino
        
      # Generar los posibles sucesores (vecinos hacia todas las direcciones) del nodo actual 
        sucesores = [(nodo_actual[0] + x, nodo_actual[1] + y) for x, y in [(1, 0), (-1, 0), (0, 1), (0, -1)]]
        
        for sucesor in sucesores:
          # Verificar si el sucesor está fuera del laberinto o es un obstáculo (igual a 1)
            if not estaEnLaberinto(sucesor, lLaberinto) or lLaberinto[sucesor[0]][sucesor[1]] == 1:
                continue
            
            nuevo_costo = costo_acumulado + 1  # En este caso, todos los movimientos tienen un costo uniforme

            # Se chequea si el sucesor ya fue registrado en algun movimiento anterior.
            if sucesor in lista_cerrada:
                continue

            # Se revisa si el sucesor está en la lista abierta de posibles candidatos  
            if any(sucesor == x[0] for x in lista_abierta):
                continue
            
            # Actualizar información del sucesor
            padres[sucesor] = nodo_actual
            lista_abierta.append((sucesor, nuevo_costo))
    # Devuelve una lista vacia en caso de vaciarse la lista_abierta sin exito de llegar a tTermino.
    return []


#
# imprimeLaberinto: Imprime el laberinto base y el camino solución
# lLaberinto: recibe una matriz (lista n x m) con el laberinto a imprimir
# lCaminoSolucion (opcional): Si viene dibuja el camino solución, sino viene imprime caminos (0) y obstáculos (1)
#
def imprimeLaberinto(lLaberinto, lCaminoSolucion = None):
    # Imprime posiciones de columnas
    print(' ' * 3, end='')
    for nColumna in range(len(lLaberinto[0])):
        print(f'{nColumna} ', end='') # Imprime el número de columna seguido de un espacio
    print() # Cambia de línea después de imprimir las posiciones de columnas

    # Laberinto
    for nFila, lFila in enumerate(lLaberinto):
        print(f'{nFila} [', end='')
        for nColumna, nDatoLaberinto in enumerate(lFila):
            if lCaminoSolucion == None:
                print(nDatoLaberinto, end='')
            else:
                if (nFila, nColumna) in lCaminoSolucion:
                    print('X', end='') # Imprime 'X' para resaltar el camino solución
                else:
                    print(' ', end='')
            if nColumna != len(lFila) - 1:
                print(' ', end='')
        print(']')
      
if __name__ == '__main__':
  # Cargar el laberinto desde el archivo 'input.txt' como una matriz de enteros
    lLaberinto = np.loadtxt('input.txt', dtype=int).tolist()

  # Obtener el número de filas y columnas en el laberinto
    nFilas = len(lLaberinto)
    nColumnas = len(lLaberinto[1])

  # Encontrar la fila de inicio (donde el valor es 0) y crear la coordenada de inicio
    nFilaInicio = [nFila for nFila, lFila in enumerate(lLaberinto) if lFila[0] == 0][0]
    tInicio = (nFilaInicio, 0)
    lLaberinto[tInicio[0]][tInicio[1]] = 0
  # Encontrar la fila de término (donde el valor es 0 en la última columna) y crear la coordenada de término
    nFilaTermino = [nFila for nFila, lFila in enumerate(lLaberinto) if lFila[nColumnas - 1] == 0][0]
    print(nFilaTermino)
    tTermino = (nFilaTermino, nColumnas - 1)
    lLaberinto[tTermino[0]][tTermino[1]] = 0
    # Imprimir la información sobre el laberinto y los nodos de inicio y término
    print(f'Laberinto de {nFilas} filas x {nColumnas} columnas:')
    imprimeLaberinto(lLaberinto)
    print(f'\nInicio en: {tInicio}')
    print(f'Término en: {tTermino}')

   # Ejecutar el algoritmo para encontrar el camino solución
    lCaminoSolucion = AEstrella(tInicio, tTermino, lLaberinto) 

    #Aquí entregamos la solución gráfica con su respectivo viajecito
    print()
    if len(lCaminoSolucion) > 0:
        print(f'La solución tiene {len(lCaminoSolucion) - 1} pasos.')
        print(f'Es el siguiente camino: {lCaminoSolucion}')
        print()
        imprimeLaberinto(lLaberinto, lCaminoSolucion)
    else:
        print('No se ha encontrado una solución')
        print(f'El camino solucion es: {lCaminoSolucion}')
      
