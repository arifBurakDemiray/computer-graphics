

from OpenGL.GL import *
from OpenGL.GLUT.fonts import GLUT_BITMAP_9_BY_15
from OpenGL.raw.GLUT import glutBitmapCharacter
from numpy import character

def gluPrintText(text: 'list[character]') -> None:
    glColor3f( 1,1,1 )
    glWindowPos2d(20, 20)
    for i in range(len(text)):
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(text[i]))