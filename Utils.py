#####################################################################
# CC3501-1 : funciones y clases para usar pygame y opengl
#####################################################################
from math import *

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *


# funcion para inicializar pygame y opengl en 2D
def init(ancho, alto, titulo):
    # inicializar pygame
    pygame.init()
    pygame.display.set_mode((ancho, alto), OPENGL | DOUBLEBUF)
    pygame.display.set_caption(titulo)

    # inicializar opengl
    glViewport(0, 0, ancho, alto)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, ancho, 0.0, alto)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # definir variables de opengl
    glClearColor(1.0, 1.0, 1.0, 0.0)  # color del fondo OJOOOO
    glShadeModel(GL_SMOOTH)
    glClearDepth(1.0)
    glDisable(GL_DEPTH_TEST)

    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)

    glLightModeli(GL_LIGHT_MODEL_COLOR_CONTROL, GL_SEPARATE_SPECULAR_COLOR)
    glEnable(GL_TEXTURE_2D)
    return


# Clase para representar vectores en un espacio 2D
class Vector:
    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)

    # angulo con respecto al eje X
    def angulo(self):
        if self.x != 0:
            return atan2(self.y, self.x)
        else:
            if self.y > 0:
                return pi / 2.0
            else:
                return -pi / 2.0

    def modulo(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def polares(self):
        return self.modulo(), self.angulo()

    def cartesianas(self):
        return self.x, self.y

    # ------------------------ definicion de operaciones primitivas +-*/ -----------------------------
    # suma vectores
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    # resta vectores
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    # multiplicacion por numero, pondera
    def __mul__(self, a: (float, int)):
        return Vector(self.x * a, self.y * a)

    # division por numero, pondera
    def __truediv__(self, a: (float, int)):
        return Vector(self.x / a, self.y / a)

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


# vector en coordenadas polares
class VectorPolar(Vector):
    def __init__(self, radio, ang):
        super().__init__(radio * cos(ang), radio * sin(ang))


def sumar(v1: Vector, v2: Vector):
    return v1 + v2


def restar(v1: Vector, v2: Vector):
    return v1 - v2


def ponderar(a: float, v: Vector):
    return v * a


def normalizar(v: Vector):
    m = v.modulo()
    if m > 0:
        return v / m
    else:
        return v


def angulo(v1: Vector, v2: Vector):
    return v1.angulo() - v2.angulo()


def rotar(v: Vector, a: float):
    return VectorPolar(v.modulo(), v.angulo() + a)


def distancia(v1: Vector, v2: Vector):
    return (v1 - v2).modulo()


def punto(v1: Vector, v2: Vector):
    return v1.x * v2.x + v1.y * v2.y


# Clase generica para crear figuras de openGL con posicion y color.
# se usa self.dibujar() para dibujar en la escena.
# self.figura define las primitivas que tiene.
class Figura:
    def __init__(self,pos: Vector, rgb=(1.0, 1.0, 1.0), escala = 1):
        self.pos = pos
        self.color = rgb
        self.lista = 0
        self.crear()
        self.angulo = angulo
        self.escala = escala

    def crear(self):
        self.lista = glGenLists(1)
        glNewList(self.lista, GL_COMPILE)
        self.figura()
        glEndList()

    def dibujar(self):
        glPushMatrix()

        glColor3fv(self.color)
        glTranslatef(self.pos.x, self.pos.y, 0.0)
        glScalef(self.escala,self.escala,0)
        glCallList(self.lista)

        glPopMatrix()

    def figura(self):
        pass

