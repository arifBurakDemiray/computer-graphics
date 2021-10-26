# CENG 487 Assignment1 by
# Arif Burak Demiray
# StudentId: 250201022
# October 2021

from mat3d import mat3d
from polygon import Polygon
from vec3d import vec3d
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from polygon_helper import vectors_to_matrices
import time
import sys

from vertex_color import RGBA, VertexRope



cube_translator = vec3d(1.5,0.0,-7.0,1.0)
triangle_translator = vec3d(-1.5,0.0,-6.0,1.0)

triangle = Polygon([
                        vec3d(0.0,1.0,0.0,1.0),
                        vec3d(-1.0,-1.0,1.0,1.0),
                        vec3d(1.0,-1.0,1.0,1.0),
                        vec3d(1.0,-1.0,-1.0,1.0),
                        vec3d(-1.0,-1.0,-1.0,1.0)
                    ],
                    [
                        VertexRope([0,1,2],[RGBA(1,0,0),RGBA(0,1,0),RGBA(0,0,1)]),
                        VertexRope([0,2,3],[RGBA(1,0,0),RGBA(0,0,1),RGBA(0,1,0)]),
                        VertexRope([0,3,4],[RGBA(1,0,0),RGBA(0,1,0),RGBA(0,0,1)]),
                        VertexRope([0,4,1],[RGBA(1,0,0),RGBA(0,0,1),RGBA(0,1,0)])
                    ])


cube = Polygon([
                    vec3d(1.0, 1.0,-1.0,1.0),
                    vec3d(-1.0, 1.0,-1.0,1.0),
                    vec3d(-1.0, 1.0, 1.0,1.0),
                    vec3d(1.0, 1.0, 1.0,1.0),
                    vec3d(1.0,-1.0, 1.0,1.0),
                    vec3d(-1.0,-1.0, 1.0,1.0),
                    vec3d(-1.0,-1.0,-1.0,1.0),
                    vec3d(1.0,-1.0,-1.0,1.0)
                ],
                [
                    VertexRope([0,1,2,3],[RGBA(0,1,0)]),
                    VertexRope([2,1,6,5],[RGBA(1.0,0.5,0.0)]),
                    VertexRope([3,2,5,4],[RGBA(1,0,0)]),
                    VertexRope([4,5,6,7],[RGBA(1,1,0)]),
                    VertexRope([7,6,1,0],[RGBA(0,0,1)]),
                    VertexRope([0,3,4,7],[RGBA(1,0,1)])
                ]
                )
window = 0

triangle_degree = 1
cube_degree = -1

isStopped = False

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
        rotate_models()

    DrawGLScene()

def keyPressed(key, x, y):
    translate_models()
    if ord(key) == 27:
        glutLeaveMainLoop()
    elif(ord(key) == 119):
        triangle.scale(2)
        cube.scale(2)
    elif(ord(key) == 115):
        triangle.scale(0.5)
        cube.scale(0.5)
    elif(ord(key) == 8):
        undo_models()
    elif(ord(key) == 32):
        global isStopped 
        isStopped = True
        rotate_models()
    untranslate_models()

def undo_models():
    triangle.undo()
    cube.undo()

def rotate_models():
    triangle.rotate(triangle_degree)
    cube.rotate(cube_degree)

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
    window = glutCreateWindow("CENG487 Development Env Test")
    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(RotateOverTime)
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)
    InitGL(640, 480)
    glutMainLoop()

print ("Hit ESC key to quit.")
main()
