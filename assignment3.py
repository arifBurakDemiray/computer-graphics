# CENG 487 Assignment3 by
# Arif Burak Demiray
# StudentId: 250201022
# November 2021

from lib.exporter import export_as_obj
from lib.obj_parser import QuadParser
from lib.populator import QuadPopulator, Populator
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys

populator : Populator  #populator

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

    populator.draw() #populator's draw method

    glutSwapBuffers()


def keyPressed(key, x, y) -> None:
    populator.untranslate_models()
    value = ord(key)
    if value == 27:  # Esc leave
        glutLeaveMainLoop()
    elif value == 43: #+ subdive
        populator.populate_up()
    elif value == 45: #- subdivide
        populator.populate_down()
    elif(value == 8):  # Backspace undo
        populator.models[0].undo()
    elif(value == 42): #* rotate z positive 
        populator.models[0].rotate_z(5)
    elif(value == 47): #/ rotate z negative
        populator.models[0].rotate_z(-5)
    elif(value == 115): #S save
        export_as_obj(populator.models[0],sys.argv[1])
    populator.translate_models()

def arrowsPressed(key, x, y) -> None:
    populator.untranslate_models()
    if key == GLUT_KEY_LEFT: #left
        populator.models[0].rotate_y(-5)
    elif key == GLUT_KEY_RIGHT: #right
        populator.models[0].rotate_y(5)
    elif key == GLUT_KEY_UP: #up
        populator.models[0].rotate_x(5)
    elif key == GLUT_KEY_DOWN: #down
        populator.models[0].rotate_x(-5)
    elif key == GLUT_KEY_PAGE_UP: #zoom in
        populator.models[0].scale(2)
    elif key == GLUT_KEY_PAGE_DOWN: #zoom out
        populator.models[0].scale(0.5)
    populator.translate_models()


def print_menu() -> None:
    print(
    "------------------------------------------------\n" +
    "[/_\] Hit ESC key to quit\n" +
    "[\_/] Hit + to increase subdivide\n" +
    "[/_\] Hit - to decrease subdivide\n" +
    "[\_/] Hit RIGHT Arrow Key to rotate right by y axis\n"+
    "[/_\] Hit LEFT Arrow Key to rotate left by y axis\n"+
    "[\_/] Hit UP Arrow Key to rotate up by x axis\n"+
    "[/_\] Hit DOWN Arrow Key to rotate down by x axis\n"+
    "[\_/] Hit * to rotate up by z axis\n"+
    "[/_\] Hit / to rotate down by z axis\n"+
    "[\_/] Hit BACKSPACE to Undo\n"+
    "[/_\] Hit PAGE UP to zoom in\n"+
    "[\_/] Hit PAGE DOWN to zoom out\n"+
    "[/_\] Hit S export as obj file\n"+
    "------------------------------------------------")

def InitScreen() -> None:
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    glutCreateWindow("CENG487 Assignment 3")
    glEnable(GL_BLEND)

def InitFunctions() -> None:
    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    
    glutReshapeFunc(ReSizeGLScene)
    
    glutKeyboardFunc(keyPressed)
    glutSpecialFunc(arrowsPressed)

    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) #blending for alpha color channel
    
def main() -> None:
    global populator
    parser = QuadParser(sys.argv[1])  #read file name
    obj = parser.parse()  #parse it
    populator = QuadPopulator(obj) #and create populator o it

    print_menu()  #print menu to console
    
    populator.translate_models()  #translate to visible area
    
    #init gls
    InitScreen()
    InitFunctions()
    InitGL(640, 480)
    glutMainLoop()
    

if __name__ == '__main__':
    main()
