# CENG 487 Assignment2 by
# Arif Burak Demiray
# StudentId: 250201022
# November 2021


from lib_arif.populator import CubePopulator, CyclinderPopulator, Populator
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys


# translation vectors for the models
isCyclinder = False
isCube = False

populators : list[Populator] = [CubePopulator(),CyclinderPopulator()]
selected_populator = 0
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

    populators[selected_populator].draw()

    glutSwapBuffers()


def keyPressed(key, x, y) -> None:
    global selected_populator
    populators[selected_populator].untranslate_models()
    value = ord(key)
    if value == 27:  # Esc leave
        glutLeaveMainLoop()
    elif value == 43:
        populators[selected_populator].populate_up()
    elif value == 45:
        populators[selected_populator].populate_down()
    elif value >=49 and value <=50:
        selected_populator = value - 49
    populators[selected_populator].translate_models()


def main() -> None:
    global window
    populators[selected_populator].translate_models()
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
    "------------------------------------------------"
)
main()
