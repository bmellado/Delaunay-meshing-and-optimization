from parte1 import *
from Utils import *
import math

################   TAREA 2 ####################################################################
###############################################################################################


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


#Funcion que retorna true si un triangulo existe en la lista, false caso contrario
def existe(triangulo, listaTriangulos):
    for i in listaTriangulos:
        if(i[0] != None):
            if(triangulo == i[0]):
                return True
    return False

#Algoritmo de busqueda del Lepp (arista terminal mas larga), retorna los triangulos que comparten la arista terminal
def lepp(t,listaTriangulos):
    posT = posicionTriangulo(t, listaTriangulos)
    p1 = aristaGrande(t)[0]
    p2 = aristaGrande(t)[1]
    p3 = verticeRestante(t, p1, p2)
    restringido = False
    posNextT = listaTriangulos[posT][1][posVertice(p3, t)-1]
    if(posNextT == None):
        return [t, None]
    nextT = listaTriangulos[posNextT][0]
    np1 = aristaGrande(nextT)[0]
    np2 = aristaGrande(nextT)[1]

    while((p1 != np1 or p2 != np2) and (p1 != np2 or p2 != np1)):
        t = nextT
        posT = posicionTriangulo(t, listaTriangulos)
        p1 = aristaGrande(t)[0]
        p2 = aristaGrande(t)[1]
        p3 = verticeRestante(t, p1, p2)
        posNextT = listaTriangulos[posT][1][posVertice(p3, t) - 1]
        if (posNextT == None):
            return [t, None]
        nextT = listaTriangulos[posNextT][0]
        np1 = aristaGrande(nextT)[0]
        np2 = aristaGrande(nextT)[1]

    return [t, nextT]

#funcion que indica si alguno de los dos triangulos retornados por el lepp tiene alguna arista restringida
def parTerminalRestringido(parT, listaTriangulos):

    t0 =  parT[0]
    t1 =  parT[1]
    posT0 = posicionTriangulo(t0, listaTriangulos)
    posT1 = posicionTriangulo(t1, listaTriangulos)
    p1 = aristaGrande(t0)[0]
    p2 = aristaGrande(t0)[1]

    #Sabemos que p1 p2 van a ser los puntos de la arista grande compartida por los triangulos terminales
    posP1T0 = posVertice(p1, t0)
    posP2T0 = posVertice(p2, t0)
    posP1T1 = posVertice(p1, t1)
    posP2T1 = posVertice(p2, t1)

    if(listaTriangulos[posT0][1][posP1T0 - 1] == None or listaTriangulos[posT0][1][posP2T0 - 1] == None):
        return [True, t0]
    elif(listaTriangulos[posT1][1][posP1T1 - 1] == None or listaTriangulos[posT1][1][posP2T1 - 1] == None):
        return [True, t1]
    else:
        return [False, None]

#Funcion que retorna true si un punto esta en el triangulo t, false de lo contrario
def estaEnTriangulo(p,t):
    if(t.p1==p or t.p2==p or t.p3==p):
        return True
    return False

#Funcion que retorna una lista con los triangulos que tienen al punto P como vertice
def buscarTriangulosPunto(listaTriangulos,p):
    lista = []
    for t in listaTriangulos:
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
#Funcion que retorna el signo de un int,float
def signo(x):
    if(x>0):
        return 1
    if(x<0):
        return -1
    else:
        return 1

# def --> Son convexos
#Retorna True si dos triangulos adyacentes son convexos o False si no son convexos
def convexos(t1,t2):
    verLibreT1 = verticeNoCompartido(t1,t2)
    verLibreT2 = verticeNoCompartido(t2,t1)
    listaT1 = [t1.p1,t1.p2,t1.p3]
    listaCompartidos = []
    for  p in listaT1:
        if(p!=verLibreT1):
            listaCompartidos.append(p)
    verComp1 = listaCompartidos[0]
    verComp2 = listaCompartidos[1]
    ang1 = angVectores(restar(verComp2,verComp1),restar(verLibreT1,verComp1)) + angVectores(restar(verComp2,verComp1),restar(verLibreT2,verComp1))
    ang2 = angVectores(restar(verComp1,verComp2),restar(verLibreT1,verComp2)) + angVectores(restar(verComp1,verComp2),restar(verLibreT2,verComp2))
    if(ang1 > math.pi or ang2 > math.pi):
        return False
    return True

#Funcion que retorna el triangulo que encierra el punto 2  de una lista de triangulos que ya contienen el punto 1
def trianguloEncierraPunto(listaPunto1,punto1,punto2):
    for t in listaPunto1:
        ver1 = dosPuntos(t,punto1)[0]
        ver2 = dosPuntos(t,punto1)[1]
        vector1 = restar(ver1,punto1)
        vector2 = restar(ver2,punto1)
        vectorPunto = restar(punto2,punto1)
        if(sentido(vector1,vectorPunto)*sentido(vector2,vectorPunto)==-1 and ((signo(vectorPunto.x)==signo(vector1.x)==signo(vector2.x)) or (signo(vectorPunto.y)==signo(vector1.y)==signo(vector2.y)))):
            return t
        if(sentido(vector1,vectorPunto)== 0 and (signo(vector1.x)==signo(vectorPunto.x) and signo(vector1.y) == signo(vectorPunto.y))):
            return t
        if (sentido(vector2, vectorPunto) == 0 and (signo(vector2.x) == signo(vectorPunto.x) and signo(vector2.y) == signo(vectorPunto.y))):
            return t
        if(vector1.x==0):
            if (sentido(vector1, vectorPunto) * sentido(vector2, vectorPunto) == -1 and (
                (signo(vectorPunto.x) == signo(vector2.x)) or (
                    signo(vectorPunto.y) == signo(vector1.y) == signo(vector2.y)))):
                return t
        if(vector1.y==0):
            if (sentido(vector1, vectorPunto) * sentido(vector2, vectorPunto) == -1 and (
                (signo(vectorPunto.x) == signo(vector1.x) == signo(vector2.x)) or (
                    signo(vectorPunto.y) == signo(vector2.y)))):
                return t
        if(vector2.x==0):
            if (sentido(vector1, vectorPunto) * sentido(vector2, vectorPunto) == -1 and (
                (signo(vectorPunto.x) == signo(vector1.x)) or (
                    signo(vectorPunto.y) == signo(vector1.y) == signo(vector2.y)))):
                return t
        if(vector2.y==0):
            if (sentido(vector1, vectorPunto) * sentido(vector2, vectorPunto) == -1 and (
                (signo(vectorPunto.x) == signo(vector1.x) == signo(vector2.x)) or (
                    signo(vectorPunto.y) == signo(vector1.y)))):
                return t

#Funcion que restringe la arisgta de una triangulacion
def restringir(punto1,punto2,listaTriangulos):
    listaPunto1 = buscarTriangulosPunto(listaTriangulos,punto1)
    primerTriangulo = trianguloEncierraPunto(listaPunto1,punto1,punto2)
    #Si la arista restringida ya existe que corte la funcion
    if(verticeEnTriangulo(punto2,primerTriangulo)):
        return None

    #Si no existe iniciar el proceso de intercambio de arista
    puntoFinal = False
    verticeEje = punto1
    t1 = primerTriangulo
    tPendiente = None
    existeNoConvexo = False
    while(puntoFinal == False):
        posT1 = posicionTriangulo(t1,listaTriangulos)
        posVerEjeT1 = posVertice(verticeEje,t1)
        posT2 = listaTriangulos[posT1][1][posVerEjeT1-1]
        t2 = listaTriangulos[posT2][0]

        if(convexos(t1,t2)):
            verLibreT1 = verticeNoCompartido(t1, t2)
            verLibreT2 = verticeNoCompartido(t2, t1)
            listaT1 = [t1.p1, t1.p2, t1.p3]
            listaCompartidos = []
            for p in listaT1:
                if (p != verLibreT1):
                    listaCompartidos.append(p)
            p1 = listaCompartidos[0]
            p2 = listaCompartidos[1]
            pos = posT1
            posTAd = posT2
            vOp = verLibreT1
            vOpAd = verLibreT2
            t=t1
            tAd = t2
            referencia1 = listaTriangulos[pos][1]
            referencia2 = listaTriangulos[posTAd][1]
            nuevoT1 = Triangulo(p1, vOp, vOpAd)
            nuevoT2 = Triangulo(p2, vOp, vOpAd)
            anti(nuevoT1)
            anti(nuevoT2)
            ##Relacionar triangulos nuevos entre si
            # nuevoT1
            refT1 = [None, None, None]
            refT1[posVertice(verticeNoCompartido(nuevoT1, nuevoT2), nuevoT1) - 1] = posTAd

            # nuevoT2
            refT2 = [None, None, None]
            refT2[posVertice(verticeNoCompartido(nuevoT2, nuevoT1), nuevoT2) - 1] = pos

            # Relacionar triangulos nuevos con referencia de los antiguos

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
            if(estaEnTriangulo(punto2,nuevoT1) or estaEnTriangulo(punto2,nuevoT2)):
                puntoFinal=True
            else:
                t1 = trianguloEncierraPunto([nuevoT1,nuevoT2],verticeEje,punto2)

        else: #No son convexos
            existeNoConvexo = True
            verLibreT1 = verticeNoCompartido(t1, t2)
            listaT1 = [t1.p1, t1.p2, t1.p3]
            listaCompartidos = []
            for p in listaT1:
                if (p != verLibreT1):
                    listaCompartidos.append(p)
            p1 = listaCompartidos[0]
            p2 = listaCompartidos[1]
            if(trianguloEncierraPunto([t2],p1,punto2)!=None):
                verticeEje = p1
            else:
                verticeEje = p2
            tPendiente = t1
            t1 = t2

    if(existeNoConvexo):
        verticeEje = punto1
        t1 = tPendiente
        posT1 = posicionTriangulo(t1, listaTriangulos)
        posVerEjeT1 = posVertice(verticeEje, t1)
        posT2 = listaTriangulos[posT1][1][posVerEjeT1 - 1]
        t2 = listaTriangulos[posT2][0]
        verLibreT1 = verticeNoCompartido(t1, t2)
        verLibreT2 = verticeNoCompartido(t2, t1)
        listaT1 = [t1.p1, t1.p2, t1.p3]
        listaCompartidos = []
        for p in listaT1:
            if (p != verLibreT1):
                listaCompartidos.append(p)
        p1 = listaCompartidos[0]
        p2 = listaCompartidos[1]
        pos = posT1
        posTAd = posT2
        vOp = verLibreT1
        vOpAd = verLibreT2
        t = t1
        tAd = t2
        referencia1 = listaTriangulos[pos][1]
        referencia2 = listaTriangulos[posTAd][1]
        nuevoT1 = Triangulo(p1, vOp, vOpAd)
        nuevoT2 = Triangulo(p2, vOp, vOpAd)
        anti(nuevoT1)
        anti(nuevoT2)
        ##Relacionar triangulos nuevos entre si
        # nuevoT1
        refT1 = [None, None, None]
        refT1[posVertice(verticeNoCompartido(nuevoT1, nuevoT2), nuevoT1) - 1] = posTAd

        # nuevoT2
        refT2 = [None, None, None]
        refT2[posVertice(verticeNoCompartido(nuevoT2, nuevoT1), nuevoT2) - 1] = pos

        # Relacionar triangulos nuevos con referencia de los antiguos

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

#Funcion que elimina triangulos por fuera a partir de una lista de rectas restringidas
def eliminarAntiHorario(listaRestringidos,listaTriangulos):
    for arista in listaRestringidos:
        ver1 = arista[0]
        ver2 = arista[1]
        for t in listaTriangulos:
            if(t[0] != None):
                p1 = t[0].p1
                p2 = t[0].p2
                p3 = t[0].p3
                if(sentido(restar(ver2,ver1),restar(p1,ver1)) == -1 or
                    sentido(restar(ver2, ver1), restar(p2, ver1)) ==-1 or
                       sentido(restar(ver2, ver1), restar(p3, ver1)) ==-1):
                    #Eliminar referencias antiguas;
                    pos = posicionTriangulo(t[0], listaTriangulos)
                    for T in listaTriangulos:
                        for i in range(3):
                            if(T[1][i] == pos):
                                T[1][i] = None
                    listaTriangulos[pos][0] = None

#Funcion que elimina triangulos por dentro a partir de una lista de rectas restringidas
def eliminarHorario(listaRestringidos,listaTriangulos):
    for t in listaTriangulos:
        if (t[0] != None):
            p1 = t[0].p1
            p2 = t[0].p2
            p3 = t[0].p3
            estaDentro = True
            for arista in listaRestringidos:
                ver1 = arista[0]
                ver2 = arista[1]
                if(sentido(restar(ver2,ver1),restar(p1,ver1)) == -1 or
                    sentido(restar(ver2, ver1), restar(p2, ver1)) ==-1 or
                       sentido(restar(ver2, ver1), restar(p3, ver1)) ==-1):
                    estaDentro = False
            if(estaDentro):
                pos = posicionTriangulo(t[0], listaTriangulos)
                for T in listaTriangulos:
                    for i in range(3):
                        if (T[1][i] == pos):
                            T[1][i] = None
                listaTriangulos[pos][0] = None

#funcion que retorna True si un triangulo no cumple que su angulo minimo sea mayor a 30 grados
def malo(t):
    if(anguloMin(t) < math.pi/6):
        return True
    else:
        return False


#determinar el midsize edge (segunda arista mas larga) si la funcion recibe los puntos de la arista mas larga y el triangulo terminal
def midsize(t, p1, p2):
    p3 = verticeRestante(t, p1, p2)
    v1 = restar(p3,p1)
    v2 = restar(p3,p2)
    if(v1.modulo() >= v2.modulo()):
        return [p1,p3]
    else:
        return [p2,p3]

#funcion inserta un punto de manera especial en un borde (arista restringida por ejemplo) y crea dos nuevos triangulos
#input: el triangulo y su arista a ser biseccionada
def insercionBorde(t, arista, listaTriangulos):
    p1 = arista[0]
    p2 = arista[1]
    p3 = verticeRestante(t, p1, p2)
    px = Vector((p1.x + p2.x)/2.0, (p1.y + p2.y)/2.0)

    nuevoT1 = Triangulo(p1, px, p3)
    nuevoT2 = Triangulo(p2, p3, px)
    anti(nuevoT1)
    anti(nuevoT2)

    pos = posicionTriangulo(t, listaTriangulos)
    ultimapos = len(listaTriangulos)
    # Guardar las referencias del triangulo antiguo
    referencia = listaTriangulos[pos][1]

    ##Relacionar triangulos nuevos entre si
    # nuevoT1
    refT1 = [None, None, None]
    refT1[posVertice(p1, nuevoT1) - 1] = ultimapos

    # nuevoT2
    refT2 = [None, None, None]
    refT2[posVertice(p2, nuevoT2) - 1] = pos

    #Relacionar los triangulos nuevos con los antiguos
    if( referencia[posVertice(p1, t) - 1] != None):
        post2ad = referencia[posVertice(p1, t) - 1]
        t2ad = listaTriangulos[post2ad][0]

        #t2 a t2ad
        refT2[posVertice(px, nuevoT2) - 1] = post2ad
        #t2ad a t2
        listaTriangulos[post2ad][1][posVertice(verticeNoCompartido(t2ad, t), t2ad) - 1] = ultimapos

    if (referencia[posVertice(p2, t) - 1] != None):
        post1ad = referencia[posVertice(p2, t) - 1]
        t1ad = listaTriangulos[post1ad][0]

        # t1 a t1ad
        refT1[posVertice(px, nuevoT1) - 1] = post1ad
        # t1ad a t1
        listaTriangulos[post1ad][1][posVertice(verticeNoCompartido(t1ad, t), t1ad) - 1] = pos

    # Insertar triangulos
    listaTriangulos.pop(pos)
    listaTriangulos.insert(pos, [nuevoT1, refT1])
    listaTriangulos.insert(ultimapos, [nuevoT2, refT2])
    legalize([p1,p3], nuevoT1, listaTriangulos)
    legalize([p2,p3], nuevoT2, listaTriangulos)




def mejorar(listaTriangulos):
    while(1):
        hayMalos = False
        #la lista se revisa hasta que no queden triangulos por arreglar, en cuyo caso de rompe el ciclo
        for t in listaTriangulos:
            if(t[0] != None):
                if (malo(t[0])): #si existe un triangulo de mala calidad que comience el proceso lepp hasta que el triangulo desaparezca
                    hayMalos = True
                    #while(existe(t[0], listaTriangulos)):


                    while(existe(t[0], listaTriangulos)):
                        par = lepp(t[0], listaTriangulos)
                        # Caso 1: la funcion lepp retorna 2 triangulos
                        if(par[1] != None):

                            #Caso 1.1: alguno de los dos triangulos tiene una arista restringida
                            if(parTerminalRestringido(par, listaTriangulos)[0] == True):
                                triangulo = parTerminalRestringido(par,listaTriangulos)[1]
                                posTriangulo = posicionTriangulo(triangulo, listaTriangulos)
                                #Determinar el midsize edge
                                p1 = aristaGrande(triangulo)[0]
                                p2 = aristaGrande(triangulo)[1]

                                np1 = midsize(triangulo, p1, p2)[0]
                                np2 = midsize(triangulo, p1, p2)[1]
                                np3 = verticeRestante(triangulo, np1, np2)
                                insertionPoint = Vector((np1.x + np2.x)/2.0, (np1.y + np2.y)/2.0)

                                #si el midsize esta en una arista restringida
                                if(listaTriangulos[posTriangulo][1][posVertice(np3, triangulo) - 1] == None):
                                    insercionBorde(triangulo, [np1,np2], listaTriangulos)
                                else:  #caso borde en donde la arista midsize no sea un borde
                                    t0 = par[0]
                                    t1 = par[1]
                                    p1 = aristaGrande(t0)[0]  # indiferente usar t0 o t1,entregan lo mismo
                                    p2 = aristaGrande(t0)[1]

                                    p3 = verticeRestante(t0, p1, p2)
                                    p4 = verticeRestante(t1, p1, p2)
                                    centroidex = (p1.x + p2.x + p3.x + p4.x) / 4
                                    centroidey = (p1.y + p2.y + p3.y + p4.y) / 4
                                    centroide = Vector(centroidex, centroidey)
                                    agregar(centroide, listaTriangulos)

                            #Caso 1.2: los triangulos terminales no contienen aristas restringidas
                            else:
                                t0 = par[0]
                                t1 = par[1]
                                p1 = aristaGrande(t0)[0] #indiferente usar t0 o t1,entregan lo mismo
                                p2 = aristaGrande(t0)[1]

                                p3 = verticeRestante(t0, p1, p2)
                                p4 = verticeRestante(t1, p1, p2)
                                centroidex = (p1.x + p2.x + p3.x + p4.x)/4
                                centroidey = (p1.y + p2.y + p3.y + p4.y)/4
                                centroide = Vector(centroidex, centroidey)
                                agregar(centroide, listaTriangulos)


                        # Caso 2: la funcion lepp retorna un triangulo donde la arista mas larga esta en un borde
                        else:
                            #buscar la arista mas larga
                            #insercion en borde
                            triangulo = par[0]
                            arista = aristaGrande(triangulo)
                            insercionBorde(triangulo, arista, listaTriangulos)
                    break
        if not(hayMalos):
            break

def mallaCircular(puntos, radio, centrox, centroy):

    lista =  []
    teta = 2 * math.pi / puntos
    for i in range(puntos):
        lista.append(Vector(int(radio * cos(teta * i) + centrox), int(radio * sin(teta * i) + centroy)))
    listaRestringidos = []
    for i in range(len(lista)):
        listaRestringidos.append([lista[i],lista[(i + 1)%len(lista)]])


    return lista, listaRestringidos