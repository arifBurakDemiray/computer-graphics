# CENG 487 Assignment2 by
# Arif Burak Demiray
# StudentId: 250201022
# November 2021

from factory import create_cube, create_sub_level_cubes
from polygon import Polygon
from vec3d import vec3d
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys


# translation vectors for the models
cube_translator = vec3d(1.5, 0.0, -7.0, 1.0)
cubes = [create_cube()]

window = 0

cube_degree = -1

# info for the automatic rotation
isStopped = False

level = 0
max_level = 0
factor = 1.0

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


def DrawCube(cube: Polygon) -> None:
    glLoadIdentity()
    glBegin(GL_QUADS)
    vertices = cube.vertices_to_vectors()

    for rope in cube.vertex_links:
        rgb = rope.colors[0]
        glColor3f(rgb.r, rgb.b, rgb.g) #draw color for each face
        for i in range(len(rope.links)):
            glVertex3f(vertices[rope.links[i]].x,
                       vertices[rope.links[i]].y, vertices[rope.links[i]].z)
    glEnd()


def DrawGLScene() -> None:
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    #draw models
    for model in cubes:
        if(model.level == level):
            DrawCube(model)

    glutSwapBuffers()

def PopulateUpLevel() -> None:
    global level,factor,max_level
    level+=1
    if(max_level>=level):
        return
    max_level+=1
    factor=factor/2

    sub_models : list[Polygon] = []

    #untranslate_models(level-1)

    for model in cubes:
        if(model.level+1==level):
            sub_models.extend(create_sub_level_cubes(level,model,factor))

    cubes.extend(sub_models)

        
    

def PopulateDownLevel() -> None:
    global level,factor
    if(level == 0):
        return
    factor = factor*2
    level-=1

#fix infinite loop

def keyPressed(key, x, y) -> None:
    #translate_models()  # prepare space to the origin
    value = ord(key)
    if value == 27:  # Esc leave
        glutLeaveMainLoop()
    if value == 43:
        PopulateUpLevel()
    if value == 45:
        PopulateDownLevel()

    #untranslate_models()
      # return it to its place


def translate_models() -> None:
    """
    Translates models to the origin
    """

    for model in cubes:
        if(model.level == level):
            model.plane_translate(0, cube_translator)


def untranslate_models(init_level: int = level) -> None:
    """
    Untranslates models to their start vertices
    """

    for model in cubes:
        if(model.level == init_level):
            model.plane_translate(1, cube_translator)


def main() -> None:
    #translate_models() #Firstly put models to their locations
    global window
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("CENG487 Assignment 1")
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
    "------------------------------------------------"
)
main()
