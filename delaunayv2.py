import sys
sys.setrecursionlimit(3000)
import os
from parte2 import *
from Utils import *
os.environ['SDL_VIDEO_CENTERED'] = '1'  # centrar pantalla

def main():
    ancho = 600
    alto = 600
    init(ancho, alto, "Delaunay")

    # Puntos con los cuales construir la triangulacion
    n= 300
    #puntos = mallaCircular()
    puntos = [Vector(40,30),Vector(60,40),Vector(70,30),Vector(90,50),Vector(90,70),Vector(50,70),Vector(30,60),Vector(60,90),Vector(70,90)]
    listaRestringidos = [[Vector(40,30),Vector(70,30)],
                         [Vector(70, 30), Vector(90, 50)],
                         [Vector(90, 50), Vector(90, 70)],
                         [Vector(90, 70), Vector(70, 90)],
                         [Vector(70, 90), Vector(40, 30)]]

    #puntos = [Vector(40,30),Vector(60,40),Vector(70,30),Vector(90,50),Vector(90,70),Vector(30,60),Vector(50,70),Vector(60,90),Vector(70,90)]

    #for i in listaTriangulos()

    # Genera lista de vertices del cuadrilatero que encierra los puntos
    esquina = esquinas(puntos, 20)

    # Genera los dos primeros triangulos de la triangulacion a partir del cuadrado
    t1 = Triangulo(esquina[0], esquina[2], esquina[3])
    t1 = anti(t1)
    t2 = Triangulo(esquina[0], esquina[1], esquina[2])
    t2 = anti(t2)

    # Genera matriz de triangulos con sus referencias de vecindad dentro de la matriz
    listaTriangulos = [[t1, [None, None, 1]],
                       [t2, [None, 0, None]]]

    ######### BUSQUEDA DEL PUNTO EN TRIANGULO############

    # Defino punto Q que servira de referencia para ubicar en que triangulo se ubica un punto dado
    Q = esquina[2]  # Este punto es el que esta mas a la derecha y arriba de la triangulacion

    # Lista que contiene todos los triangulos que tienen como una de sus vertices el punto Q
    listaQ = [t1, t2]

######### INSERCION DE PUNTOS EN LA MALLA #########

    for punto in puntos:
        agregar(punto,listaTriangulos,Q,listaQ)

    print(len(listaTriangulos))
    for arista in listaRestringidos:
        restringir(arista[0],arista[1],listaTriangulos)
    #restringir(Vector(60,90),Vector(90,50),listaTriangulos)
    #restringir(Vector(60, 90), Vector(60, 40), listaTriangulos)
    eliminarAntiHorario(listaRestringidos,listaTriangulos)
    #for i in listaTriangulos:
     #   i[0].imprimir()
     #   print(i[1])

    #lep1 = lepp(listaTriangulos[200][0],listaTriangulos,Triangulo(Vector(0,0),Vector(0,0),Vector(0,0)))
    #print(lep1[0].imprimir(),lep1[1].imprimir(),lep1[2],lep1[3])

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == QUIT: # cerrar ventanas
                run = False
                exit()


        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for t in listaTriangulos:
            if(t[0]!=None):
                t[0].dibujar()

        pygame.display.flip()  # actualizar pantalla
        pygame.time.wait(int(1000 / 30))  # ajusta a 30 fps

    pygame.quit()


main()




