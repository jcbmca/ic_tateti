# -*- coding: utf-8 -*-
"""
Created on Abril 5, 2022
version: 0.2

@author: jc
@author: ss
"""

import random
import os
import csv


def clear():
    _ = os.system( ('clear', 'cls')[os.name == 'nt'])
#    if os.name == 'nt':
#        _ = os.system('cls')
#    else:
#        _ = os.system('clear')

class Tablero():
    # tablero 
    __cuadros = { 1 : None, 2: None, 3: None,
                  4 : None, 5: None, 6: None,
                  7 : None, 8: None, 9: None }
    # regal de juegos ganados, esto pude ser una base de dato
    # que se actualiza en cada jugada que pierde o que gana, (entrenamiento)
    __jugadas_ok = (
                    ( 1, 2, 3,),
                    ( 1, 4, 7,),
                    ( 1, 5, 9,),
                    ( 2, 5, 8,),
                    ( 3, 6, 9,),
                    ( 3, 7, 5 ),
                    ( 4, 5, 6,),
                    ( 7, 8, 9,), )

    def __init__(self) -> None:
        print ("NUEVO TABLERO")
    
    def reset(self):
        for c in __class__.__cuadros:
            __class__.__cuadros[c] = None

    def marcarCelda(self, posicion, jugador : str):
        lista_jugadores = ( "X", "x", "O", "o" )
        if len(jugador) == 1:
            if jugador in lista_jugadores:
                jugador = jugador.upper()
                __class__.__cuadros[posicion] = jugador
    
    def leerCelda(self, posicion):
        return ' ' if __class__.__cuadros[posicion]==None else __class__.__cuadros[posicion]

    def leerCeldasDelJugador(self, jugador: str):
        celdas = list()
        for key in __class__.__cuadros.keys():
            if __class__.__cuadros[key] != None:
                if __class__.__cuadros[key] == jugador:
                    celdas.append(key)
        return celdas

    def estadoDelJugador(self, jugador: str):
        celdas = self.leerCeldasDelJugador(jugador)
        for i in range(8):
            if(set(__class__.__jugadas_ok[i]).issubset(set(celdas))):
                return True    
        return False
        
    def celdasDisponiblesParaJugar(self):
        celdasDisponibles = list()
        for key in __class__.__cuadros.keys():
            if __class__.__cuadros[key] == None:
                celdasDisponibles.append(key)
        return celdasDisponibles

    def __str__(self) -> str:
        salida = (
            ' {} ' + '\u2502' + ' {} ' + '\u2502' + ' {} \n' +
            '\u2500'*3 + '\u253C' + '\u2500'*3 + '\u253C' + '\u2500'*3 + '\n' +
            ' {} ' + '\u2502' + ' {} ' + '\u2502' + ' {}\n' +
            '\u2500'*3 + '\u253C' + '\u2500'*3 + '\u253C' + '\u2500'*3 + '\n' +            
            ' {} ' + '\u2502' + ' {} ' + '\u2502' +  ' {}\n' ).format(
            self.leerCelda(7),self.leerCelda(8),self.leerCelda(9),
            self.leerCelda(4),self.leerCelda(5),self.leerCelda(6),
            self.leerCelda(1),self.leerCelda(2),self.leerCelda(3))
        return salida

class Agente:
    def __init__(self) -> None:
        pass
    
    def juegoEstocastico(self, lugares: list):
        index = random.randrange(0, len(lugares), 1)
        return lugares[index]


class Jugador(Agente):
    __tablero = None

    def __init__(self, tablero: Tablero, mostrar_mensajes: bool, retornar_valor: bool) -> None:
        super().__init__()
        __class__.__tablero = tablero
        self.__mostar_mensajes = mostrar_mensajes
        self.__retornar_valor = retornar_valor

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, nombre):
        if self.__mostar_mensajes:
            print(f"Mi nombre es: {nombre}")
        self.__nombre = nombre

    def juegarEbrio(self):
        if self.__mostar_mensajes:
            print("Voy a jugar ebrio")
        celdas = __class__.__tablero.celdasDisponiblesParaJugar()
        celda = self.juegoEstocastico(celdas)
        __class__.__tablero.marcarCelda(celda, self.__nombre)
        if self.__retornar_valor:
            return celda, self.__nombre
    
    def soyGanador(self):
        ok = __class__.__tablero.estadoDelJugador(self.__nombre)
        return ok
        
    def mostrarEstadoJugada(self):
        ok = __class__.__tablero.estadoDelJugador(self.__nombre)
        print(f"Soy el jugador: {self.__nombre}. ¿Gane la partida?: {'Si' if ok else 'No'}")


    def mostrarJugada(self):
        if self.__mostar_mensajes:
            print("Esta es mi jugada")
        print ( __class__.__tablero )
        
        

clear()



tab_uno = Tablero()
#print( tab_uno )

ag1 = Jugador(tab_uno, False, True)
ag1.nombre = "X"

ag2 = Jugador(tab_uno, False, True)
ag2.nombre = "O"

resultados = list()
N = 20000
for n in range(N):
    tab_uno.reset()
    
    fin = False


    for j in range(4):

        ag1.juegarEbrio() 
        #ag1.mostrarJugada()

        if j > 1:
            fin = ag1.soyGanador()
            if fin:
                break

        ag2.juegarEbrio()
        #ag2.mostrarJugada()

        if j > 1:
            fin = ag2.soyGanador()
            if fin:
                break
        j += 1
            
    # esta linea realiza la ultima jugada
    if fin == False:
        ag1.juegarEbrio()
        #ag1.mostrarJugada()

    #ag1.mostrarEstadoJugada()
    #ag2.mostrarEstadoJugada()

    if ag1.soyGanador():
        r = [ag1.nombre, "G" ]
    elif ag2.soyGanador():
        r = [ag2.nombre, "G" ]
    else:
        r = [f"{ag1.nombre}/{ag2.nombre}", "E" ]

    resultados.append(r)
    #print(n)

jugadores = list()
for r in resultados:
    jugadores.append(r[0])
    
unique_jugadores = list(dict.fromkeys(jugadores))
#print(unique_jugadores)
    
salida = list()

for uj in unique_jugadores:
    acumulador = 0
    for r in resultados:
        if uj == r[0]:
            acumulador += 1
    porcent = f"( {100*acumulador/N} % )"
    salida.append([uj, acumulador, porcent])

for s in salida:
    print(s)

print("")


