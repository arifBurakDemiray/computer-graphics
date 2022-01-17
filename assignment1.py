# CENG 487 Assignment1 by
# Arif Burak Demiray
# October 2021

from lib.factory import create_cube, create_triangle
from lib.polygon import Polygon
from lib.vec3d import Vec3d
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
import sys

# translation vectors for the models
cube_translator = Vec3d(1.5, 0.0, -7.0, 1.0)
triangle_translator = Vec3d(-1.5, 0.0, -6.0, 1.0)

# create models
triangle = create_triangle()
cube = create_cube()

window = 0

# rotation degrees of the models
triangle_degree = 1
cube_degree = -1

# info for the automatic rotation
isStopped = False


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


def DrawTriangle(triangle: Polygon) -> None:
    glLoadIdentity()
    glBegin(GL_TRIANGLES)

    vertices = triangle.vertices_to_vectors()  # convert to vectors
    for rope in triangle.vertex_links:
        for i in range(len(rope.links)):  # draw by their links
            rgb = rope.colors[i]
            glColor3f(rgb.r, rgb.b, rgb.g)  # draw color for each vertex
            glVertex3f(vertices[rope.links[i]].x,
                       vertices[rope.links[i]].y, vertices[rope.links[i]].z)

    glEnd()


def DrawCube(cube: Polygon) -> None:
    glLoadIdentity()
    glBegin(GL_QUADS)
    vertices = cube.vertices_to_vectors()

    for rope in cube.vertex_links:
        rgb = rope.colors[0]
        glColor3f(rgb.r, rgb.b, rgb.g)  # draw color for each face
        for i in range(len(rope.links)):
            glVertex3f(vertices[rope.links[i]].x,
                       vertices[rope.links[i]].y, vertices[rope.links[i]].z)
    glEnd()


def DrawGLScene() -> None:
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # draw models
    DrawTriangle(triangle)
    DrawCube(cube)

    glutSwapBuffers()


def RotateOverTime() -> None:
    if(not isStopped):  # if user not stopped automatic rotation
        time.sleep(0.04)  # wait a little
        translate_models()  # translate to origin
        rotate_models()  # rotate
        untranslate_models()  # translate back

    DrawGLScene()


def keyPressed(key, x, y) -> None:
    translate_models()  # prepare space to the origin
    global isStopped
    value = ord(key)

    if value == 27:  # Esc leave
        glutLeaveMainLoop()
    elif(value == 119):  # W zoom in
        triangle.scale(2)
        cube.scale(2)
    elif(value == 115):  # S zoom out
        triangle.scale(0.5)
        cube.scale(0.5)
    elif(value == 8):  # Backspace undo
        undo_models()
    elif(value == 32):  # Space start/stop
        isStopped = not isStopped
    elif(value == 100):  # D Rotate by triangle to the right
        isStopped = True
        rotate_models(True)
    elif(value == 97):  # A Rotate by triangle to the left
        isStopped = True
        rotate_models()

    untranslate_models()  # return it to its place


def undo_models() -> None:
    """
    This function undoes last tranformation done to the models
    """
    triangle.undo()
    cube.undo()


def rotate_models(inversed: bool = False) -> None:
    """
    Rotates models by global degrees of them

    Parameters:

    Inverse rotate or not
    """
    triangle.rotate(triangle_degree*-1 if inversed else triangle_degree)
    cube.rotate(cube_degree*-1 if inversed else cube_degree)


def translate_models() -> None:
    """
    Translates models to the origin
    """
    triangle.plane_translate(0, triangle_translator)
    cube.plane_translate(0, cube_translator)


def untranslate_models() -> None:
    """
    Untranslates models to their start vertices
    """
    triangle.plane_translate(1, triangle_translator)
    cube.plane_translate(1, cube_translator)


def main() -> None:
    translate_models()  # Firstly put models to their locations

    global window
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("CENG487 Assignment 1")
    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(RotateOverTime)
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)
    InitGL(640, 480)
    glutMainLoop()


print(
    "------------------------------------------------\n" +
    "[/_\] Hit ESC key to quit\n" +
    "[\_/] Hit W to zoom in, S to zoom out\n" +
    "[/_\] Hit D to rotate manually to right by triangle\n" +
    "[\_/] Hit A to rotate manually to left by triangle\n" +
    "[/_\] Hit SPACE to Start/Stop the rotation\n" +
    "[\_/] Hit BACKSPACE to Undo\n" +
    "------------------------------------------------"
)
main()
