from random import *
from Utils import *


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


#genera lista n puntos aleatorios
def generar(n):
    lista = []
    for i in range(n):
        lista.append(Vector(randint(30,570), randint(30,570)))
    for p in lista:
        while(lista.count(p)>1):
            lista.remove(p)
    return lista

#genera grilla de puntos
def grilla():
    lista = []
    for i in range(5,25):
        for j in range(5,25):
            lista.append(Vector(i*20,j*20))
    return lista

def mallaCircular():
    lista = []
    radio = 250
    teta = 18
    while(radio > 20):
        for i in range (20):
            lista.append(Vector(int(radio*cos(teta*i)+300),int(radio*sin(teta*i)+300)))
        radio -= 20
    #shuffle(lista)
    return lista


#funcion que entrega lista con los vertices en sentido antihorario de un cuadrado que encierre a los puntos dados
#con un ancho de holgura
def esquinas(puntos,ancho):
    minX = float('inf')
    maxX = 0
    minY = float('inf')
    maxY = 0

    for i in puntos:
        minX = min(minX,i.x)
        maxX = max(maxX,i.x)
        minY = min(minY,i.y)
        maxY = max(maxY,i.y)

    esquinas = [Vector(minX-ancho,minY-ancho),Vector(maxX+ancho,minY-ancho),Vector(maxX+ancho,maxY+ancho),Vector(minX-ancho,maxY+ancho)]
    return esquinas

#Funcion que verifica si un punto pertenece a uno de los vertices de un triangulo
def verticeEnTriangulo(vertice,triangulo):
    if(triangulo.p1 == vertice or triangulo.p2 == vertice or triangulo.p3 == vertice):
        return True
    return False

#Ordena los puntos de un triangulo de manera que queden en sentido anti-horario
def anti(triangulo):
    dABx = triangulo.p2.x-triangulo.p1.x
    dABy = triangulo.p2.y-triangulo.p1.y
    dACx = triangulo.p3.x-triangulo.p1.x
    dACy = triangulo.p3.y-triangulo.p1.y
    vAB = Vector(dABx,dABy)
    vAC = Vector(dACx,dACy)
    #producto cruz
    producto = (vAB.x*vAC.y)-(vAB.y*vAC.x)
    if(producto>0): #Sentido anti-horario
        pass
    elif(producto<0):
        aux = triangulo.p2
        triangulo.p2 = triangulo.p3
        triangulo.p3 = aux
    else: #producto = 0
        pass
    return triangulo

#Funcion que entrega +1 si un punto esta sobre un vector, -1 si esta bajo un vector,0 si esta colineal
def sentido(vector1,vector2):
    producto = (vector1.x * vector2.y) - (vector1.y * vector2.x)
    if(producto>0):
        return 1
    elif(producto<0):
        return -1
    else:
        return 0

#Funcion que retorna si un punto esta dentro de las aristas de un triangulo y los vertices de las aristas
def estaEnAristas(t,punto):
    # Recta P1 P2

    p1x = float(t.p1.x)
    p2x = float(t.p2.x)
    p3x = float(t.p3.x)
    p1y = float(t.p1.y)
    p2y = float(t.p2.y)
    p3y = float(t.p3.y)
    ## Recta P1 P2 ##

    if(p2x-p1x !=0):
        m1 = (p2y - p1y) / (p2x - p1x)
        if(punto.y == m1*(punto.x-p1x)+p1y and ((punto.x <= p1x and punto.x >= p2x) or (punto.x <= p2x and punto.x >= p1x))):
            return [True,t.p1,t.p2]
    elif(p2x-p1x ==0):
        if(p2x==punto.x and ((p1y <= punto.y and punto.y <= p2y)or(p2y <= punto.y and punto.y <= p1y))):
            return [True,t.p1,t.p2]
    ## Recta P2 P3  ##
    if(p3x-p2x != 0):
        m2 = (p3y - p2y) / (p3x - p2x)
        if (punto.y == m2 * (punto.x - p2x) + p2y and (
            (punto.x <= p2x and punto.x >= p3x) or (punto.x <= p3x and punto.x >= p2x))):

            return [True, t.p2, t.p3]
    elif(p3x-p2x == 0):
        if (p3x == punto.x and ((p3y <= punto.y and punto.y <= p2y) or (p2y <= punto.y and punto.y <= p3y))):
            return [True, t.p2, t.p3]

    ## Recta P1 P3 ##
    if(p3x - p1x != 0):
        m3 = (p3y - p1y) / (p3x - p1x)
        if (punto.y == m3 * (punto.x - p1x) + p1y and (
            (punto.x <= p1x and punto.x >= p3x) or (punto.x <= p3x and punto.x >= p1x))):
            return [True, t.p1, t.p3]
    elif(p3x - p1x == 0):
        if (p1x == punto.x and ((p3y <= punto.y and punto.y <= p1y) or (p1y <= punto.y and punto.y <= p3y))):
            return [True, t.p1, t.p3]

    return [False, None, None]

#funcion que retorna el punto no compartido de t1 entre los triangulos adyacentes t1 y t2
def verticeNoCompartido(t1,t2):
    if(t1.p1 == t2.p1 or t1.p1 == t2.p2 or t1.p1 == t2.p3):
        if(t1.p2 == t2.p1 or t1.p2 == t2.p2 or t1.p2 == t2.p3):
            return t1.p3
        else:
            return t1.p2
    else:
        return t1.p1

#funcion que retorna el vertice restante (tercero) de un triangulo y dos de sus puntos
def verticeRestante(t,p1,p2):
    if((t.p1 == p1 and t.p2 == p2) or (t.p1 == p2 and t.p2 == p1)):
        return t.p3
    elif((t.p2 == p1 and t.p3 == p2) or (t.p2 == p2 and t.p3 == p1)):
        return t.p1
    else:
        return t.p2

#funcion que encuentra la posicion de un triangulo en la lista de triangulos
def posicionTriangulo(triangulo, listaTriangulos):
    c=0
    for i in listaTriangulos:
        if(triangulo == i[0]):
            break
        c+=1
    return c

#funcion que retorna la posicion de un vertice en un Triangulo
def posVertice(vertice,t):
    if(t.p1==vertice):
        return 1
    elif(t.p2==vertice):
        return 2
    else:
        return 3

#funcion que retorna cual de los tres triangulos (t1, t2 o t3) es adyacente a t
def trianguloAdyacente(vector1,vector2,t1,t2,t3):
    lista = [t1,t2,t3]
    for i in lista:
        if((i.p1 == vector1 and i.p2 == vector2) or (i.p1 == vector2 and i.p2 == vector1)
           or (i.p1 == vector1 and i.p3 == vector2) or (i.p1 == vector2 and i.p3 == vector1)
            or (i.p2 == vector1 and i.p3 == vector2) or (i.p2 == vector2 and i.p3 == vector1)
           ):
            return i

def pCruz(p1, p2, punto):
    producto = (p2.x - p1.x) * (punto.y - p1.y) - (p2.y - p1.y) * (punto.x - p1.x)
    if (producto > 0):
        return 1
    elif (producto < 0):
        return -1
    else:
        return 0


def hallarTriangulo(punto,listaTriangulos,triangulo):
    pos = posicionTriangulo(triangulo, listaTriangulos)
    if(pCruz(triangulo.p1,triangulo.p2,punto)==1 and pCruz(triangulo.p2,triangulo.p3,punto)==1 and pCruz(triangulo.p3,triangulo.p1,punto)==1):
        return [triangulo, "in"]
    elif((pCruz(triangulo.p1,triangulo.p2,punto)==1 and pCruz(triangulo.p2,triangulo.p3,punto)==1 and pCruz(triangulo.p3,triangulo.p1,punto)==0)
         or (pCruz(triangulo.p1,triangulo.p2,punto)==1 and pCruz(triangulo.p2,triangulo.p3,punto)==0 and pCruz(triangulo.p3,triangulo.p1,punto)==1)
        or (pCruz(triangulo.p1,triangulo.p2,punto)==0 and pCruz(triangulo.p2,triangulo.p3,punto)==1 and pCruz(triangulo.p3,triangulo.p1,punto)==1)):
        return [triangulo, "edge"]
    elif(pCruz(triangulo.p1,triangulo.p2,punto)==-1):
        posTrianguloAd = listaTriangulos[pos][1][2]
        trianguloAd = listaTriangulos[posTrianguloAd][0]
        return hallarTriangulo(punto,listaTriangulos,trianguloAd)
    elif (pCruz(triangulo.p2, triangulo.p3, punto) == -1):
        posTrianguloAd = listaTriangulos[pos][1][0]
        trianguloAd = listaTriangulos[posTrianguloAd][0]
        return hallarTriangulo(punto, listaTriangulos, trianguloAd)
    elif (pCruz(triangulo.p3, triangulo.p1, punto) == -1):
        posTrianguloAd = listaTriangulos[pos][1][1]
        trianguloAd = listaTriangulos[posTrianguloAd][0]
        return hallarTriangulo(punto, listaTriangulos, trianguloAd)

#############################################################################################
####LEGALIZACION#############################################################################
#############################################################################################

def inCircle(a,b,c,d):
    termino1 = (a.x-d.x)*(((b.y-d.y)*((c.x-d.x)**2 + (c.y-d.y)**2))-((c.y-d.y)*((b.x-d.x)**2 + (b.y-d.y)**2)))
    termino2 = (a.y-d.y)*(((b.x-d.x)*((c.x-d.x)**2 + (c.y-d.y)**2))-((c.x-d.x)*((b.x-d.x)**2 + (b.y-d.y)**2)))
    termino3 = ((a.x-d.x)**2 + (a.y-d.y)**2)*(((b.x-d.x)*(c.y-d.y))-((c.x-d.x)*(b.y-d.y)))
    det = termino1 - termino2 + termino3
    if(det <= 0):
        return "out"
    else:
        return "in"

def legalize(arista,t,listaTriangulos,Q,listaQ):
    p1 = arista[0]
    p2 = arista[1]
    vOp = verticeRestante(t,p1,p2)
    pos = posicionTriangulo(t,listaTriangulos)
    posTAd = listaTriangulos[pos][1][posVertice(vOp,t)-1]
    if(posTAd == None):
        return None
    tAd = listaTriangulos[posTAd][0]
    vOpAd = verticeNoCompartido(tAd,t)
    test = inCircle(t.p1,t.p2,t.p3,vOpAd)
    if(test == "out"):
        return None
    else:
        referencia1 = listaTriangulos[pos][1]
        referencia2 = listaTriangulos[posTAd][1]
        nuevoT1 = Triangulo(p1,vOp,vOpAd)
        nuevoT2 = Triangulo(p2,vOp,vOpAd)

        anti(nuevoT1)
        anti(nuevoT2)

        # Agregar a listaQ los triangulos que tengan como vertice Q
        if (verticeEnTriangulo(Q, nuevoT1)):
            listaQ.append(nuevoT1)
        if (verticeEnTriangulo(Q, nuevoT2)):
            listaQ.append(nuevoT2)
        # Si el triangulo antiguo y adyacente estan en lista Q, que los remueva
        if (listaQ.count(t) != 0):
            listaQ.remove(t)
        if (listaQ.count(tAd) != 0):
            listaQ.remove(tAd)

        ##Relacionar triangulos nuevos entre si
        # nuevoT1
        refT1 = [None, None, None]
        refT1[posVertice(verticeNoCompartido(nuevoT1, nuevoT2), nuevoT1) - 1] = posTAd

        # nuevoT2
        refT2 = [None, None, None]
        refT2[posVertice(verticeNoCompartido(nuevoT2, nuevoT1), nuevoT2) - 1] = pos

        #Relacionar triangulos nuevos con referencia de los antiguos

        for r in referencia1:
            if (r != None):
                if (referencia1.index(r) == 0):
                    tAdyacente = trianguloAdyacente(t.p2, t.p3, nuevoT1, nuevoT1, nuevoT2)
                    if (tAdyacente == nuevoT1):
                        refT1[posVertice(verticeNoCompartido(nuevoT1, listaTriangulos[r][0]), nuevoT1) - 1] = r
                        listaTriangulos[r][1][posVertice(verticeNoCompartido(listaTriangulos[r][0], tAdyacente),
                                                         listaTriangulos[r][0]) - 1] = pos
                    elif (tAdyacente == nuevoT2):
                        refT2[posVertice(verticeNoCompartido(nuevoT2, listaTriangulos[r][0]), nuevoT2) - 1] = r
                        listaTriangulos[r][1][
                            posVertice(verticeNoCompartido(listaTriangulos[r][0], tAdyacente),
                                       listaTriangulos[r][0]) - 1] = posTAd


                elif (referencia1.index(r) == 1):
                    tAdyacente = trianguloAdyacente(t.p1, t.p3, nuevoT1, nuevoT1, nuevoT2)
                    if (tAdyacente == nuevoT1):
                        refT1[posVertice(verticeNoCompartido(nuevoT1, listaTriangulos[r][0]), nuevoT1) - 1] = r
                        listaTriangulos[r][1][
                            posVertice(verticeNoCompartido(listaTriangulos[r][0], tAdyacente),
                                       listaTriangulos[r][0]) - 1] = pos
                    elif (tAdyacente == nuevoT2):
                        refT2[posVertice(verticeNoCompartido(nuevoT2, listaTriangulos[r][0]), nuevoT2) - 1] = r
                        listaTriangulos[r][1][
                            posVertice(verticeNoCompartido(listaTriangulos[r][0], tAdyacente),
                                       listaTriangulos[r][0]) - 1] = posTAd

                elif (referencia1.index(r) == 2):
                    tAdyacente = trianguloAdyacente(t.p1, t.p2, nuevoT1, nuevoT1, nuevoT2)
                    if (tAdyacente == nuevoT1):
                        refT1[posVertice(verticeNoCompartido(nuevoT1, listaTriangulos[r][0]), nuevoT1) - 1] = r
                        listaTriangulos[r][1][
                            posVertice(verticeNoCompartido(listaTriangulos[r][0], tAdyacente),
                                       listaTriangulos[r][0]) - 1] = pos
                    elif (tAdyacente == nuevoT2):
                        refT2[posVertice(verticeNoCompartido(nuevoT2, listaTriangulos[r][0]), nuevoT2) - 1] = r
                        listaTriangulos[r][1][
                            posVertice(verticeNoCompartido(listaTriangulos[r][0], tAdyacente),
                                       listaTriangulos[r][0]) - 1] = posTAd

            else:
                continue

        for r in referencia2:
            if (r != None):
                if (referencia2.index(r) == 0):
                    tAdyacente = trianguloAdyacente(tAd.p2, tAd.p3, nuevoT1, nuevoT1, nuevoT2)
                    if (tAdyacente == nuevoT1):
                        refT1[posVertice(verticeNoCompartido(nuevoT1, listaTriangulos[r][0]), nuevoT1) - 1] = r
                        listaTriangulos[r][1][posVertice(verticeNoCompartido(listaTriangulos[r][0], tAdyacente),
                                                         listaTriangulos[r][0]) - 1] = pos
                    elif (tAdyacente == nuevoT2):
                        refT2[posVertice(verticeNoCompartido(nuevoT2, listaTriangulos[r][0]), nuevoT2) - 1] = r
                        listaTriangulos[r][1][
                            posVertice(verticeNoCompartido(listaTriangulos[r][0], tAdyacente),
                                       listaTriangulos[r][0]) - 1] = posTAd


                elif (referencia2.index(r) == 1):
                    tAdyacente = trianguloAdyacente(tAd.p1, tAd.p3, nuevoT1, nuevoT1, nuevoT2)
                    if (tAdyacente == nuevoT1):
                        refT1[posVertice(verticeNoCompartido(nuevoT1, listaTriangulos[r][0]), nuevoT1) - 1] = r
                        listaTriangulos[r][1][
                            posVertice(verticeNoCompartido(listaTriangulos[r][0], tAdyacente),
                                       listaTriangulos[r][0]) - 1] = pos
                    elif (tAdyacente == nuevoT2):
                        refT2[posVertice(verticeNoCompartido(nuevoT2, listaTriangulos[r][0]), nuevoT2) - 1] = r
                        listaTriangulos[r][1][
                            posVertice(verticeNoCompartido(listaTriangulos[r][0], tAdyacente),
                                       listaTriangulos[r][0]) - 1] = posTAd

                elif (referencia2.index(r) == 2):
                    tAdyacente = trianguloAdyacente(tAd.p1, tAd.p2, nuevoT1, nuevoT1, nuevoT2)
                    if (tAdyacente == nuevoT1):
                        refT1[posVertice(verticeNoCompartido(nuevoT1, listaTriangulos[r][0]), nuevoT1) - 1] = r
                        listaTriangulos[r][1][
                            posVertice(verticeNoCompartido(listaTriangulos[r][0], tAdyacente),
                                       listaTriangulos[r][0]) - 1] = pos
                    elif (tAdyacente == nuevoT2):
                        refT2[posVertice(verticeNoCompartido(nuevoT2, listaTriangulos[r][0]), nuevoT2) - 1] = r
                        listaTriangulos[r][1][
                            posVertice(verticeNoCompartido(listaTriangulos[r][0], tAdyacente),
                                       listaTriangulos[r][0]) - 1] = posTAd

            else:
                continue

        # Insertar triangulos
        listaTriangulos.pop(pos)
        listaTriangulos.insert(pos, [nuevoT1, refT1])
        listaTriangulos.pop(posTAd)
        listaTriangulos.insert(posTAd, [nuevoT2, refT2])

        return legalize([p1, vOp],nuevoT1,listaTriangulos,Q,listaQ),legalize([p1, vOpAd], nuevoT1, listaTriangulos, Q, listaQ),legalize([p2, vOp], nuevoT2, listaTriangulos, Q, listaQ),legalize([p2, vOpAd], nuevoT2, listaTriangulos, Q, listaQ)
        """
        legalize([p1, vOpAd], nuevoT1, listaTriangulos, Q, listaQ)
        legalize([p2, vOp], nuevoT2, listaTriangulos, Q, listaQ)
        legalize([p2, vOpAd], nuevoT2, listaTriangulos, Q, listaQ)
        """

#Funcion que agrega un punto dentro del triangulo que lo contiene
def agregar(punto,listaTriangulos,Q,listaQ):
    ultimaPos = len(listaTriangulos)

    triangulo = hallarTriangulo(punto,listaTriangulos,listaTriangulos[0][0])
    if(triangulo == None):
        print("no se encontro triangulo")
        return None
    posicion = triangulo[1]
    triangulo = triangulo[0]
    if(posicion == "in"):
        ####Si el punto esta dentro del triangulo que genere tres triangulos mas####
        nuevoT1 = Triangulo(triangulo.p1,triangulo.p2,punto)
        nuevoT2 = Triangulo(triangulo.p2,triangulo.p3,punto)
        nuevoT3 = Triangulo(triangulo.p1,triangulo.p3,punto)
        #Ordena los puntos de los triangulos en sentido antihorario
        anti(nuevoT1)
        anti(nuevoT2)
        anti(nuevoT3)
        #Agregar a listaQ los triangulos que tengan como vertice Q
        if(verticeEnTriangulo(Q,nuevoT1)):
            listaQ.append(nuevoT1)
        if (verticeEnTriangulo(Q, nuevoT2)):
            listaQ.append(nuevoT2)
        if (verticeEnTriangulo(Q, nuevoT3)):
            listaQ.append(nuevoT3)
        if(listaQ.count(triangulo)!=0):

            listaQ.remove(triangulo)

        #Buscar posicion del triangulo antiguo en lista
        pos = posicionTriangulo(triangulo,listaTriangulos)

        #Guardar las referencias del triangulo antiguo
        referencia = listaTriangulos[pos][1]
        ##Relacionar triangulos nuevos entre si

        #nuevoT1
        refT1 = [None,None,None]
        refT1[posVertice(verticeNoCompartido(nuevoT1,nuevoT2),nuevoT1)-1] = ultimaPos
        refT1[posVertice(verticeNoCompartido(nuevoT1, nuevoT3),nuevoT1) - 1] = ultimaPos + 1

        #nuevoT2
        refT2 = [None, None, None]
        refT2[posVertice(verticeNoCompartido(nuevoT2, nuevoT1),nuevoT2) - 1] = pos
        refT2[posVertice(verticeNoCompartido(nuevoT2, nuevoT3),nuevoT2) - 1] = ultimaPos +1

        #nuevoT3
        refT3 = [None, None, None]
        refT3[posVertice(verticeNoCompartido(nuevoT3, nuevoT1),nuevoT3) - 1] = pos
        refT3[posVertice(verticeNoCompartido(nuevoT3, nuevoT2),nuevoT3) - 1] = ultimaPos

        ##Relacionar triangulos nuevos con vecinos del triangulo antiguo
        ##REASIGNACION##

        for r in referencia:
            if(r != None):
                if(referencia.index(r)==0):
                    tAdyacente = trianguloAdyacente(triangulo.p2,triangulo.p3,nuevoT1,nuevoT2,nuevoT3)
                    if(tAdyacente == nuevoT1):
                        refT1[posVertice(verticeNoCompartido(nuevoT1,listaTriangulos[r][0]),nuevoT1)-1] = r
                        listaTriangulos[r][1][posVertice(verticeNoCompartido(listaTriangulos[r][0],tAdyacente),listaTriangulos[r][0])-1] = pos
                    elif(tAdyacente == nuevoT2):
                        refT2[posVertice(verticeNoCompartido(nuevoT2, listaTriangulos[r][0]),nuevoT2) - 1] =  r
                        listaTriangulos[r][1][
                            posVertice(verticeNoCompartido(listaTriangulos[r][0], tAdyacente), listaTriangulos[r][0])-1] = ultimaPos
                    elif(tAdyacente == nuevoT3):
                        refT3[posVertice(verticeNoCompartido(nuevoT3, listaTriangulos[r][0]),nuevoT3) - 1] = r
                        listaTriangulos[r][1][
                            posVertice(verticeNoCompartido(listaTriangulos[r][0], tAdyacente), listaTriangulos[r][0])-1] = ultimaPos+1


                elif(referencia.index(r)==1):
                    tAdyacente = trianguloAdyacente(triangulo.p1, triangulo.p3, nuevoT1, nuevoT2, nuevoT3)
                    if (tAdyacente == nuevoT1):
                        refT1[posVertice(verticeNoCompartido(nuevoT1, listaTriangulos[r][0]),nuevoT1) - 1] = r
                        listaTriangulos[r][1][
                            posVertice(verticeNoCompartido(listaTriangulos[r][0], tAdyacente), listaTriangulos[r][0])-1] = pos
                    elif (tAdyacente == nuevoT2):
                        refT2[posVertice(verticeNoCompartido(nuevoT2, listaTriangulos[r][0]),nuevoT2) - 1] = r
                        listaTriangulos[r][1][
                            posVertice(verticeNoCompartido(listaTriangulos[r][0], tAdyacente), listaTriangulos[r][0])-1] = ultimaPos
                    elif (tAdyacente == nuevoT3):
                        refT3[posVertice(verticeNoCompartido(nuevoT3, listaTriangulos[r][0]),nuevoT3) - 1] = r
                        listaTriangulos[r][1][
                            posVertice(verticeNoCompartido(listaTriangulos[r][0], tAdyacente), listaTriangulos[r][0])-1] = ultimaPos + 1

                elif(referencia.index(r)==2):
                    tAdyacente = trianguloAdyacente(triangulo.p1, triangulo.p2, nuevoT1, nuevoT2, nuevoT3)
                    if (tAdyacente == nuevoT1):
                        refT1[posVertice(verticeNoCompartido(nuevoT1, listaTriangulos[r][0]),nuevoT1) - 1] = r
                        listaTriangulos[r][1][
                            posVertice(verticeNoCompartido(listaTriangulos[r][0], tAdyacente), listaTriangulos[r][0])-1] = pos
                    elif (tAdyacente == nuevoT2):
                        refT2[posVertice(verticeNoCompartido(nuevoT2, listaTriangulos[r][0]),nuevoT2) - 1] = r
                        listaTriangulos[r][1][
                            posVertice(verticeNoCompartido(listaTriangulos[r][0], tAdyacente), listaTriangulos[r][0])-1] = ultimaPos
                    elif (tAdyacente == nuevoT3):
                        refT3[posVertice(verticeNoCompartido(nuevoT3, listaTriangulos[r][0]),nuevoT3) - 1] = r
                        listaTriangulos[r][1][
                            posVertice(verticeNoCompartido(listaTriangulos[r][0], tAdyacente), listaTriangulos[r][0])-1] = ultimaPos + 1

            else:
                continue


        #Insertar triangulos
        listaTriangulos.pop(pos)
        listaTriangulos.insert(pos, [nuevoT1,refT1])
        listaTriangulos.insert(ultimaPos, [nuevoT2, refT2])
        listaTriangulos.insert(ultimaPos + 1, [nuevoT3, refT3])
        legalize([triangulo.p1,triangulo.p2],nuevoT1,listaTriangulos,Q,listaQ)
        legalize([triangulo.p2, triangulo.p3], nuevoT2, listaTriangulos, Q, listaQ)
        legalize([triangulo.p1, triangulo.p3], nuevoT3, listaTriangulos, Q, listaQ)

    elif(posicion == "edge"):

        ultimaPos = len(listaTriangulos)
        p1 = estaEnAristas(triangulo,punto)[1]
        p2 = estaEnAristas(triangulo,punto)[2]

        # Buscar posicion del triangulo antiguo en lista
        pos = posicionTriangulo(triangulo, listaTriangulos)

        verOpTriangulo = verticeRestante(triangulo,p1,p2)

        posTriangOp = listaTriangulos[pos][1][posVertice(verOpTriangulo,triangulo)-1]

        trianguloAd = listaTriangulos[posTriangOp][0]
        posAd = posicionTriangulo(trianguloAd, listaTriangulos)
        verOpTrianguloAd = verticeNoCompartido(trianguloAd,triangulo)

        ####Si el punto esta dentro del triangulo que genere cuatro triangulos mas####
        nuevoT1 = Triangulo(p1,verOpTriangulo,punto)
        nuevoT2 = Triangulo(p2,verOpTriangulo,punto)
        nuevoT3 = Triangulo(p2,verOpTrianguloAd,punto)
        nuevoT4 = Triangulo(p1,verOpTrianguloAd,punto)
        # Ordena los puntos de los triangulos en sentido antihorario
        anti(nuevoT1)
        anti(nuevoT2)
        anti(nuevoT3)
        anti(nuevoT4)

        # Agregar a listaQ los triangulos que tengan como vertice Q
        if (verticeEnTriangulo(Q, nuevoT1)):
            listaQ.append(nuevoT1)
        if (verticeEnTriangulo(Q, nuevoT2)):
            listaQ.append(nuevoT2)
        if (verticeEnTriangulo(Q, nuevoT3)):
            listaQ.append(nuevoT3)
        if (verticeEnTriangulo(Q, nuevoT4)):
            listaQ.append(nuevoT4)
        #Si el triangulo antiguo y adyacente estan en lista Q, que los remueva
        if (listaQ.count(triangulo) != 0):
            listaQ.remove(triangulo)
        if (listaQ.count(trianguloAd) != 0):
            listaQ.remove(trianguloAd)

        # Guardar las referencias del triangulo antiguo
        referencia1 = listaTriangulos[pos][1]
        referencia2 = listaTriangulos[posAd][1]

        ##Relacionar triangulos nuevos entre si

        # nuevoT1
        refT1 = [None, None, None]
        refT1[posVertice(verticeNoCompartido(nuevoT1, nuevoT2), nuevoT1) - 1] = posAd
        refT1[posVertice(verticeNoCompartido(nuevoT1, nuevoT4), nuevoT1) - 1] = ultimaPos + 1

        # nuevoT2
        refT2 = [None, None, None]
        refT2[posVertice(verticeNoCompartido(nuevoT2, nuevoT1), nuevoT2) - 1] = pos
        refT2[posVertice(verticeNoCompartido(nuevoT2, nuevoT3), nuevoT2) - 1] = ultimaPos

        # nuevoT3
        refT3 = [None, None, None]
        refT3[posVertice(verticeNoCompartido(nuevoT3, nuevoT2), nuevoT3) - 1] = posAd
        refT3[posVertice(verticeNoCompartido(nuevoT3, nuevoT4), nuevoT3) - 1] = ultimaPos +1

        #nuevoT4
        refT4 = [None, None, None]
        refT4[posVertice(verticeNoCompartido(nuevoT4, nuevoT1), nuevoT4) - 1] = pos
        refT4[posVertice(verticeNoCompartido(nuevoT4, nuevoT3), nuevoT4) - 1] = ultimaPos

        ##Relacionar triangulos nuevos con vecinos del triangulo antiguo
        ##REASIGNACION##
        for r in referencia1:
            if(r != None):
                if(referencia1.index(r)==0):
                    tAdyacente = trianguloAdyacente(triangulo.p2,triangulo.p3,nuevoT1,nuevoT1,nuevoT2)
                    if(tAdyacente == nuevoT1):
                        refT1[posVertice(verticeNoCompartido(nuevoT1,listaTriangulos[r][0]),nuevoT1)-1] = r
                        listaTriangulos[r][1][posVertice(verticeNoCompartido(listaTriangulos[r][0],tAdyacente),listaTriangulos[r][0])-1] = pos
                    elif(tAdyacente == nuevoT2):
                        refT2[posVertice(verticeNoCompartido(nuevoT2, listaTriangulos[r][0]),nuevoT2) - 1] =  r
                        listaTriangulos[r][1][
                            posVertice(verticeNoCompartido(listaTriangulos[r][0], tAdyacente), listaTriangulos[r][0])-1] = posAd


                elif(referencia1.index(r)==1):
                    tAdyacente = trianguloAdyacente(triangulo.p1, triangulo.p3, nuevoT1, nuevoT1, nuevoT2)
                    if (tAdyacente == nuevoT1):
                        refT1[posVertice(verticeNoCompartido(nuevoT1, listaTriangulos[r][0]),nuevoT1) - 1] = r
                        listaTriangulos[r][1][
                            posVertice(verticeNoCompartido(listaTriangulos[r][0], tAdyacente), listaTriangulos[r][0])-1] = pos
                    elif (tAdyacente == nuevoT2):
                        refT2[posVertice(verticeNoCompartido(nuevoT2, listaTriangulos[r][0]),nuevoT2) - 1] = r
                        listaTriangulos[r][1][
                            posVertice(verticeNoCompartido(listaTriangulos[r][0], tAdyacente), listaTriangulos[r][0])-1] = posAd

                elif(referencia1.index(r)==2):
                    tAdyacente = trianguloAdyacente(triangulo.p1, triangulo.p2, nuevoT1, nuevoT1, nuevoT2)
                    if (tAdyacente == nuevoT1):
                        refT1[posVertice(verticeNoCompartido(nuevoT1, listaTriangulos[r][0]),nuevoT1) - 1] = r
                        listaTriangulos[r][1][
                            posVertice(verticeNoCompartido(listaTriangulos[r][0], tAdyacente), listaTriangulos[r][0])-1] = pos
                    elif (tAdyacente == nuevoT2):
                        refT2[posVertice(verticeNoCompartido(nuevoT2, listaTriangulos[r][0]),nuevoT2) - 1] = r
                        listaTriangulos[r][1][
                            posVertice(verticeNoCompartido(listaTriangulos[r][0], tAdyacente), listaTriangulos[r][0])-1] = posAd

            else:
                continue

        for r in referencia2:
            if (r != None):
                if (referencia2.index(r) == 0):
                    tAdyacente = trianguloAdyacente(trianguloAd.p2, trianguloAd.p3, nuevoT3, nuevoT3, nuevoT4)
                    if (tAdyacente == nuevoT3):
                        refT3[posVertice(verticeNoCompartido(nuevoT3, listaTriangulos[r][0]), nuevoT3) - 1] = r
                        listaTriangulos[r][1][posVertice(verticeNoCompartido(listaTriangulos[r][0], tAdyacente),
                                                         listaTriangulos[r][0]) - 1] = ultimaPos
                    elif (tAdyacente == nuevoT4):
                        refT4[posVertice(verticeNoCompartido(nuevoT4, listaTriangulos[r][0]), nuevoT4) - 1] = r
                        listaTriangulos[r][1][
                            posVertice(verticeNoCompartido(listaTriangulos[r][0], tAdyacente),
                                       listaTriangulos[r][0]) - 1] = ultimaPos +1


                elif (referencia2.index(r) == 1):
                    tAdyacente = trianguloAdyacente(trianguloAd.p1, trianguloAd.p3, nuevoT3, nuevoT3, nuevoT4)
                    if (tAdyacente == nuevoT3):
                        refT3[posVertice(verticeNoCompartido(nuevoT3, listaTriangulos[r][0]), nuevoT3) - 1] = r
                        listaTriangulos[r][1][
                            posVertice(verticeNoCompartido(listaTriangulos[r][0], tAdyacente),
                                       listaTriangulos[r][0]) - 1] = ultimaPos
                    elif (tAdyacente == nuevoT4):
                        refT4[posVertice(verticeNoCompartido(nuevoT4, listaTriangulos[r][0]), nuevoT4) - 1] = r
                        listaTriangulos[r][1][
                            posVertice(verticeNoCompartido(listaTriangulos[r][0], tAdyacente),
                                       listaTriangulos[r][0]) - 1] = ultimaPos +1

                elif (referencia2.index(r) == 2):
                    tAdyacente = trianguloAdyacente(trianguloAd.p1, trianguloAd.p2, nuevoT3, nuevoT3, nuevoT4)
                    if (tAdyacente == nuevoT3):
                        refT3[posVertice(verticeNoCompartido(nuevoT3, listaTriangulos[r][0]), nuevoT3) - 1] = r
                        listaTriangulos[r][1][
                            posVertice(verticeNoCompartido(listaTriangulos[r][0], tAdyacente),
                                       listaTriangulos[r][0]) - 1] = ultimaPos
                    elif (tAdyacente == nuevoT4):
                        refT4[posVertice(verticeNoCompartido(nuevoT4, listaTriangulos[r][0]), nuevoT4) - 1] = r
                        listaTriangulos[r][1][
                            posVertice(verticeNoCompartido(listaTriangulos[r][0], tAdyacente),
                                       listaTriangulos[r][0]) - 1] = ultimaPos +1

            else:
                continue

        # Insertar triangulos
        listaTriangulos.pop(pos)
        listaTriangulos.insert(pos, [nuevoT1, refT1])
        listaTriangulos.pop(posAd)
        listaTriangulos.insert(posAd, [nuevoT2, refT2])
        listaTriangulos.insert(ultimaPos, [nuevoT3, refT3])
        listaTriangulos.insert(ultimaPos + 1, [nuevoT4, refT4])
        legalize([p1,verOpTriangulo], nuevoT1, listaTriangulos, Q, listaQ)
        legalize([p2,verOpTriangulo], nuevoT2, listaTriangulos, Q, listaQ)
        legalize([p2,verOpTrianguloAd], nuevoT3, listaTriangulos, Q, listaQ)
        legalize([p1,verOpTrianguloAd], nuevoT4, listaTriangulos, Q, listaQ)