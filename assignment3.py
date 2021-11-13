# CENG 487 Assignment3 by
# Arif Burak Demiray
# StudentId: 250201022
# November 2021


from lib.obj_parser import QuadParser
from lib.populator import QuadPopulator, Populator
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys


# translation vectors for the models
isCyclinder = False
isCube = False
parser = QuadParser(sys.argv[1])

obj = parser.parse()
#Populators, responsible for populating sub divisions of the objects
populator : Populator = QuadPopulator(obj)
window = 0

def InitGL(Width: float, Height: float) -> None:
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, Width/Height, 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)


def ReSizeGLScene(Width: float, Height: float) -> None:
    if Height == 0:
        Height = 1

    glViewport(0, 0, Width, Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, Width/Height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


def DrawGLScene() -> None:
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    populator.draw() #selected populator's draw method

    glutSwapBuffers()


def keyPressed(key, x, y) -> None:
    populator.untranslate_models()
    value = ord(key)
    if value == 27:  # Esc leave
        glutLeaveMainLoop()
    elif value == 43:
        populator.populate_up()
    elif value == 45:
        populator.populate_down()
    populator.translate_models()


def main() -> None:
    global window
    populator.translate_models()
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("CENG487 Assignment 2")
    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)
    InitGL(640, 480)
    glutMainLoop()


print(
    "------------------------------------------------\n" +
    "[/_\] Hit ESC key to quit\n" +
    "[\_/] Hit + increase\n" +
    "[/_\] Hit - decrease\n" +
    "[\_/] Hit 1 to select Cube\n"+
    "[/_\] Hit 2 to select Cyclinder\n"+
    "[\_/] Hit 3 to select Sphere\n"+
    "------------------------------------------------"
)

main()
