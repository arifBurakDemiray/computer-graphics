# CENG 487 Assignment1 by
# Arif Burak Demiray
# StudentId: 250201022
# October 2021

from factory import create_cube, create_triangle
from polygon import Polygon
from vec3d import vec3d
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
import sys

cube_translator = vec3d(1.5,0.0,-7.0,1.0)
triangle_translator = vec3d(-1.5,0.0,-6.0,1.0)

triangle = create_triangle()

cube = create_cube()

window = 0

triangle_degree = 1
cube_degree = -1

isStopped = True

def InitGL(Width, Height):				
	glClearColor(0.0, 0.0, 0.0, 0.0)	
	glClearDepth(1.0)				
	glDepthFunc(GL_LESS)			
	glEnable(GL_DEPTH_TEST)				
	glShadeModel(GL_SMOOTH)				

	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()					
	gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)

	glMatrixMode(GL_MODELVIEW)

def ReSizeGLScene(Width, Height):
	if Height == 0:						# Prevent A Divide By Zero If The Window Is Too Small
		Height = 1

	glViewport(0, 0, Width, Height)		# Reset The Current Viewport And Perspective Transformation
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
	glMatrixMode(GL_MODELVIEW)

def DrawTriangle(triangle: Polygon):
    glLoadIdentity()
    glBegin(GL_TRIANGLES)
    vertices = triangle.vertices_to_vectors()
    for rope in triangle.vertex_links:
        for i in range(len(rope.links)):
            rgb = rope.colors[i]
            glColor3f(rgb.r,rgb.b,rgb.g)	
            glVertex3f(vertices[rope.links[i]].x,vertices[rope.links[i]].y,vertices[rope.links[i]].z)
    
    glEnd()
    
    
def DrawCube(cube: Polygon):
    glLoadIdentity()
    glBegin(GL_QUADS)
    vertices = cube.vertices_to_vectors()

    for rope in cube.vertex_links:
        rgb = rope.colors[0]
        glColor3f(rgb.r,rgb.b,rgb.g)
        for i in range(len(rope.links)):	
            glVertex3f(vertices[rope.links[i]].x,vertices[rope.links[i]].y,vertices[rope.links[i]].z)
    glEnd()

def DrawGLScene():
    global rtri, rquad
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    DrawTriangle(triangle)

    DrawCube(cube)

    glutSwapBuffers()

def RotateOverTime() -> None:
    if(not isStopped):
        global triangle_degree,cube_degree
        time.sleep(0.04)
        translate_models()
        rotate_models()
        untranslate_models()

    DrawGLScene()

def keyPressed(key, x, y):
    translate_models() #prepare space to the origin

    value = ord(key)

    if value == 27: #Esc leave
        glutLeaveMainLoop()
    elif(value == 119): #W zoom in
        triangle.scale(2)
        cube.scale(2)
    elif(value == 115): #S zoom out
        triangle.scale(0.5)
        cube.scale(0.5)
    elif(value == 8): #Backspace undo
        undo_models()
    elif(value == 32): #Space start/stop
        global isStopped 
        isStopped = not isStopped
    elif(value == 100): #D Rotate by triangle to the right
        rotate_models(True)
    elif(value == 97): #A Rotate by triangle to the left
        rotate_models()
    untranslate_models() #return it to its place

def undo_models():
    triangle.undo()
    cube.undo()

def rotate_models(inversed: bool = False):
    triangle.rotate(triangle_degree*-1 if inversed else triangle_degree)
    cube.rotate(cube_degree*-1 if inversed else cube_degree)

def translate_models():
    triangle.plane_translate(0,triangle_translator)
    cube.plane_translate(0,cube_translator)

def untranslate_models():
    triangle.plane_translate(1,triangle_translator)
    cube.plane_translate(1,cube_translator)

def main():
    translate_models()
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

print (
    "------------------------------------------------\n"+
    "[/_\] Hit ESC key to quit\n"+ 
    "[\_/] Hit W to zoom in, S to zoom out\n"+
    "[/_\] Hit D to rotate manually to right by triangle\n"+
    "[\_/] Hit A to rotate manually to left by triangle\n"+
    "[/_\] Hit SPACE to Start/Stop the rotation\n"+
    "[\_/] Hit BACKSPACE to Undo\n"+
    "------------------------------------------------"
    )
main()
