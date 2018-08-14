from Utils import *
from math import *
class Triangulo(Figura):
    def __init__(self,p1,p2,p3,pos=Vector(0.0,0.0),rgb = (1.0,1.0,1.0)):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        super().__init__(pos, rgb)

    def figura(self):
        glBegin(GL_LINE_LOOP)
        glColor3f(0,0,0)
        #glBegin(GL_TRIANGLES)
        #glColor3f(randint(1, 256) / 256.0, randint(1, 256) / 256.0, randint(1, 256) / 256.0)
        glVertex2f(self.p1.x,self.p1.y)
        glVertex2f(self.p2.x,self.p2.y)
        glVertex2f(self.p3.x,self.p3.y)
        glEnd()

    def imprimir(self):
        print(self.p1,self.p2,self.p3)

# funcion que encuentra la posicion de un triangulo en la lista de triangulos
def posicionTriangulo(triangulo, listaTriangulos):
    c = 0
    for i in listaTriangulos:
        if (triangulo == i[0]):
            break
        c += 1
    return c
#Funcion que verifica si un punto pertenece a uno de los vertices de un triangulo
def verticeEnTriangulo(vertice,triangulo):
    if(triangulo.p1 == vertice or triangulo.p2 == vertice or triangulo.p3 == vertice):
        return True
    return False
#funcion que retorna la posicion de un vertice en un Triangulo
def posVertice(vertice,t):
    if(t.p1==vertice):
        return 1
    elif(t.p2==vertice):
        return 2
    else:
        return 3

# Funcion que entrega +1 si un punto esta sobre un vector, -1 si esta bajo un vector,0 si esta colineal
def sentido(vector1, vector2):
    producto = (vector1.x * vector2.y) - (vector1.y * vector2.x)
    if (producto > 0):
        return 1
    elif (producto < 0):
        return -1
    else:
        return 0
#funcion que retorna el vertice restante (tercero) de un triangulo y dos de sus puntos
def verticeRestante(t,p1,p2):
    if((t.p1 == p1 and t.p2 == p2) or (t.p1 == p2 and t.p2 == p1)):
        return t.p3
    elif((t.p2 == p1 and t.p3 == p2) or (t.p2 == p2 and t.p3 == p1)):
        return t.p1
    else:
        return t.p2
#funcion que retorna el angulo formado por dos vectores
def angVectores(v1,v2):
    return acos((v1.x*v2.x + v1.y*v2.y)/(v1.modulo()*v2.modulo()))
#funcion que retorna el angulo minimo de un triangulo
def anguloMin(triangulo):
    p1 = triangulo.p1
    p2 = triangulo.p2
    p3 = triangulo.p3
    ang1 = angVectores(restar(p1,p3),restar(p2,p3))
    ang2 = angVectores(restar(p2, p1), restar(p3, p1))
    ang3 = angVectores(restar(p1, p2), restar(p3, p2))
    angMin = min(ang1,ang2,ang3)
    return angMin

#retorna los puntos de la arista mas larga
def aristaGrande(triangulo):
    v1 = restar(triangulo.p2,triangulo.p1)
    v2 = restar(triangulo.p3,triangulo.p2)
    v3 = restar(triangulo.p1,triangulo.p3)
    if(v1.modulo() >= v2.modulo() and v1.modulo() >= v3.modulo()):
        return [triangulo.p1,triangulo.p2]
    elif ( v2.modulo() >= v1.modulo() and v2.modulo() >= v3.modulo()):
        return [triangulo.p2,triangulo.p3]
    elif(v3.modulo() >= v2.modulo() and v3.modulo() >= v1.modulo()):
        return [triangulo.p1,triangulo.p3]

def lepp(triangulo,listaTriangulos,tAnt):
    t0 = triangulo
    posT0 = posicionTriangulo(t0,listaTriangulos)
    p1 = aristaGrande(t0)[0]
    p2 = aristaGrande(t0)[1]
    p3 = verticeRestante(t0,p1,p2)
    posT1 = listaTriangulos[posT0][1][posVertice(p3,t0)-1]
    if(posT1== None):
        return [t0,tAnt,p1,p2]
    t1 = listaTriangulos[posT1][0]
    if(t1 == tAnt):
        return [t0,t1,p1,p2]
    else:
        return lepp(t1,listaTriangulos,t0)


#Funcion que retorna una lista con los triangulos que tienen al punto P como vertice
def buscarTriangulosPunto(listaTriangulos,p):
    lista = []
    for t in listaTriangulos:
        #print(t[0].p1,t[0].p2,t[0].p3)
        if(t[0].p1.x == p.x and t[0].p1.y == p.y or t[0].p2.x == p.x and t[0].p2.y == p.y  or t[0].p3.x == p.x and t[0].p3.y == p.y ):
            lista.append(t[0])
    return lista
#Funcion que retorna una lista con los dos puntos restantes de un triangulo
def dosPuntos(t,vertice):
    lista = []
    if(t.p1.x == vertice.x and t.p1.y == vertice.y):
        lista = [t.p2,t.p3]
    elif(t.p2.x == vertice.x and t.p2.y == vertice.y):
        lista = [t.p3,t.p1]
    elif(t.p3.x == vertice.x and t.p3.y == vertice.y):
        lista = [t.p1,t.p2]
    return lista

def restringir(punto1,punto2,listaTriangulos):
    listaPunto1 = buscarTriangulosPunto(listaTriangulos,punto1)
    for t in listaPunto1:
        ver1 = dosPuntos(t,punto1)[0]
        ver2 = dosPuntos(t,punto1)[1]
        if(sentido(restar(ver1,punto1),restar(punto2,punto1))*sentido(restar(ver2,punto1),restar(punto2,punto1))<=0):
            primerTriangulo = t
    primerTriangulo.imprimir()
    print(verticeEnTriangulo(punto2,primerTriangulo))


