#import os
from CC3501Utils import *
#os.environ['SDL_VIDEO_CENTERED'] = '1'  # centrar pantalla

class Triangulo(Figura):
    def __init__(self,p1,p2,p3,pos=Vector(0.0,0.0),rgb = (1.0,1.0,1.0)):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        super().__init__(pos, rgb)

    def figura(self):
        glBegin(GL_LINE_LOOP)
        glColor3f(0,0,0)
        glVertex2f(self.p1.x,self.p1.y)
        glVertex2f(self.p2.x,self.p2.y)
        glVertex2f(self.p3.x,self.p3.y)
        glEnd()

    def imprimir(self):
        print(self.p1,self.p2,self.p3)

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

def main():
    ancho = 800
    alto = 600
    init(ancho, alto, "Delaunay")
    t1=Triangulo(Vector(11,1),Vector(11,11),Vector(9,5))
    t1.imprimir()
    esta = estaEnAristas(t1,Vector(11,8))
    #print(type(esta[0]),esta[1],esta[2])
    print(esta[0],esta[1],esta[2])


main()