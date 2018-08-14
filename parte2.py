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

#Funcion que elimina triangulos a partir de una lista de rectas restringidas
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
                    listaTriangulos[posicionTriangulo(t[0],listaTriangulos)][0]=None
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
                listaTriangulos[posicionTriangulo(t[0],listaTriangulos)][0]=None