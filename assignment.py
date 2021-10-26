# CENG 487 Assignment1 by
# Arif Burak Demiray
# StudentId: 250201022
# October 2021

from types import FunctionType

from numpy import mat
from numpy.lib.twodim_base import tri
from mat3d import mat3d
from vec3d import vec3d
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from polygon_helper import vectors_to_matrices
import sys

class RGBA:
    r : float
    g : float
    b : float
    a : float

    def __init__(self,r : float, g : float, b : float, a : float = 0.0) -> 'RGBA':
        self.r = r
        self.b = b
        self.g = g
        self.a = a

class ColoredVertex:
    vertices: list[vec3d]
    colors: list[RGBA]

    def __init__(self,vertices: list[vec3d],color_provider: FunctionType) -> 'ColoredVertex':
        self.vertices = vertices
        self.colors = color_provider()


class Polygon:
    vertices : mat3d
    matrix_stack : list[mat3d]

    def __init__(self,vertices: list[vec3d]) -> 'Polygon':
        self.vertices = vectors_to_matrices(vertices)
        self.matrix_stack = []

    def transformate(self, matrix: mat3d) -> None:
        self.matrix_stack.append(matrix)
        self.vertices = self.vertices.calc_multiplacation(matrix)
    
    def translate(self, x: float, y: float, z: float) -> None:
        vector = vec3d(x,y,z,1.0)
        result = self.vertices.calc_translation(vector)

        self.vertices = result.transformed
        self.matrix_stack.append(result.transformer)

    def plane_translate(self, inverse: int) -> None:
        if(inverse == 0):
            self.translate_unregistered(-1.5,0.0,-6.0)
        else:
            self.translate_unregistered(1.5,0.0,6.0)
    
    def translate_unregistered(self, x: float, y: float, z: float) -> None:
        vector = vec3d(x,y,z,1.0)
        result = self.vertices.calc_translation(vector)

        self.vertices = result.transformed

    def rotate(self,degree: float) -> None:
        vector = self.vertices_to_vectors()[0]

        matrix = self.vertices.create_translation_matrix(vector.multiply(-1.0))
        inv_matrix = matrix.calc_inverse()

        rot_matrix = self.vertices.create_rotation_matrix(degree)

        bir = matrix.calc_multiplacation(rot_matrix).calc_multiplacation(inv_matrix)

        result = self.vertices.calc_multiplacation(bir)

        self.vertices = result
        self.matrix_stack.append(bir)

    def undo(self) -> None:
        if(len(self.matrix_stack) < 1):
            return
        last_matrix = self.matrix_stack[len(self.matrix_stack) - 1]
        self.matrix_stack.remove(last_matrix)
        self.vertices = self.vertices.calc_multiplacation(last_matrix.calc_inverse())
        

    def vertices_to_vectors(self) -> list[vec3d]:
        
        result = []

        for i in range(int(len(self.vertices.content)/4) - 1):
            result.append(
                vec3d(
                    self.vertices.content[i*4],
                    self.vertices.content[i*4+1],
                    self.vertices.content[i*4+2],
                    self.vertices.content[i*4+3])
            )

        return result

triangle_vertices = [
    vec3d(0.0,1.0,0.0,1.0),
    vec3d(-1.0,-1.0,1.0,1.0),
    vec3d(1.0,-1.0,1.0,1.0),
    vec3d(1.0,-1.0,-1.0,1.0),
    vec3d(-1.0,-1.0,-1.0,1.0)
]

triangle = Polygon(triangle_vertices)

window = 0

rtri = 0.0

rquad = 0.0

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

def DrawGLScene():
    global rtri, rquad
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    vertices = triangle.vertices_to_vectors()

    glBegin(GL_TRIANGLES)
    for i in range(4):
        glColor3f(1.0,0.0,0.0);	
        glVertex3f(vertices[0].x,vertices[0].y,vertices[0].z)
        glColor3f(0.0,1.0,0.0);	
        glVertex3f(vertices[i+1].x,vertices[i+1].y,vertices[i+1].z)
        if(i==3):
            glColor3f(0.0,0.0,1.0);	
            glVertex3f(vertices[1].x,vertices[1].y,vertices[1].z)
        else:    
            glColor3f(0.0,0.0,1.0);	
            glVertex3f(vertices[i+2].x,vertices[i+2].y,vertices[i+2].z)
    glEnd()
    glLoadIdentity()
    glutSwapBuffers()


def keyPressed(key, x, y):
    triangle.plane_translate(1)
    if ord(key) == 27:
        glutLeaveMainLoop()
    elif(ord(key) == 119):
        matris = triangle.vertices.create_scale_matrix(2)
        triangle.transformate(matris)
    elif(ord(key) == 115):
        matris = triangle.vertices.create_scale_matrix(0.5)
        triangle.transformate(matris)
    elif(ord(key) == 8):
        triangle.undo()
    elif(ord(key) == 32):
        triangle.rotate(15)
    elif(ord(key) == 116):
        triangle.translate(-1.5,0.0,-6.0)
    triangle.plane_translate(0)


def main():
    triangle.plane_translate(0)

    global window
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("CENG487 Development Env Test")
    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)
    InitGL(640, 480)
    glutMainLoop()

print ("Hit ESC key to quit.")
main()
