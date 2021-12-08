# CENG 487 Assignment3 by
# Arif Burak Demiray
# StudentId: 250201022
# November 2021

from OpenGL.GL import *
from OpenGL.GLUT.fonts import GLUT_BITMAP_9_BY_15
from OpenGL.raw.GLUT import glutBitmapCharacter
from numpy import character

def gluPrintText(text: 'list[character]',position_y : int = 0) -> None:
    """
    Helper method to print text to the screen
    """
    glColor3f( 1,1,1 )
    glWindowPos2d(20, 20+position_y)
    for i in range(len(text)):
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(text[i]))