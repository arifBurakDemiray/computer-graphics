# CENG 487 Assignment3 by
# Arif Burak Demiray
# November 2021

import os
from lib.obj_parser import QuadParser
from lib.populator import Populator, QuadPopulatorCatmull
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from lib.scene import *
import sys

from lib.view import Camera, View

populator: Populator  # populator

scene: Scene
view: View


def InitGL(Width: float, Height: float) -> None:
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, Width / Height, 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)


def ReSizeGLScene(Width: float, Height: float) -> None:
    if Height == 0:
        Height = 1

    glViewport(0, 0, Width, Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, Width / Height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


def DrawGLScene() -> None:

    scene.draw()  # populator's draw method


def keyPressed(key, x, y) -> None:
    value = ord(key)
    scene.process([value, sys.argv[1]])


def arrowsPressed(key, x, y) -> None:

    scene.process([key])


def mouseMoved(x, y) -> None:

    view.mouseMoved(x, y)
    scene.process(["C", view.cameras[view.selected]])


def print_menu() -> None:
    print(
        "------------------------------------------------\n" +
        "[/_\] Hit ESC key to quit\n" +
        "[\_/] Hit + to increase subdivide\n" +
        "[/_\] Hit - to decrease subdivide\n" +
        "[\_/] Hit RIGHT Arrow Key to rotate right by y axis\n" +
        "[/_\] Hit LEFT Arrow Key to rotate left by y axis\n" +
        "[\_/] Hit UP Arrow Key to rotate up by x axis\n" +
        "[/_\] Hit DOWN Arrow Key to rotate down by x axis\n" +
        "[\_/] Hit * to rotate up by z axis\n" +
        "[/_\] Hit / to rotate down by z axis\n" +
        "[\_/] Hit BACKSPACE to Undo\n" +
        "[/_\] Hit PAGE UP to zoom in\n" +
        "[\_/] Hit PAGE DOWN to zoom out\n" +
        "[/_\] Hit S export as obj file\n" +
        "[\_/] Use your mouse to move camera (it is in early stage)\n" +
        "------------------------------------------------")


def InitScreen() -> None:
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    glutCreateWindow("CENG487 Assignment 3")
    glEnable(GL_BLEND)


def IdleFunc() -> None:
    scene.idle()


def InitFunctions() -> None:
    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(IdleFunc)

    glutReshapeFunc(ReSizeGLScene)

    glutKeyboardFunc(keyPressed)
    glutSpecialFunc(arrowsPressed)

    glutPassiveMotionFunc(mouseMoved)

    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # blending for alpha color channel


def check_file(filename: str) -> bool:
    return os.path.isfile(filename)


def main() -> None:
    global populator, view, scene

    scene = Scene()
    view = View()

    if(len(sys.argv) < 2):
        print("usage\n\tpython3 assigment3.py filename\n\tpython assigment3.py filename")
        return

    splitted = sys.argv[1].split(".")[-1]

    if(splitted not in ["obj", "OBJ"]):
        print("\n\tplease provide an obj format file\n")
        return

    if(not check_file(sys.argv[1])):
        print("\n\tplease provide an existing file\n")
        return

    parser = QuadParser(sys.argv[1])  # read file name
    obj = parser.parse()  # parse it

    scene.subscribe(QuadPopulatorCatmull(obj))  # and create populator o it

    print_menu()  # print menu to console

    scene.process("t")  # translate to visible area

    # init gls
    InitScreen()
    InitFunctions()
    InitGL(640, 480)
    view.subscribe(Camera(320, 240))
    glutMainLoop()


if __name__ == '__main__':
    main()
