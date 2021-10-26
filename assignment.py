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

    def plane_translate(self, inverse: int, vector: vec3d) -> None:
        if(inverse == 0):
            self.translate_unregistered(vector)
        else:
            self.translate_unregistered(vector.multiply(-1.0))
    
    def translate_unregistered(self, vector: vec3d) -> None:
        result = self.vertices.calc_translation(vector)

        self.vertices = result.transformed

    def rotate(self,degree: float) -> None:
        vector = self.vertices_to_vectors()[0]
        #move to origin
        matrix = self.vertices.create_translation_matrix(vector.multiply(-1.0))
        inv_matrix = matrix.calc_inverse() #turn back to its place

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


class VertexRope:
    links : list[int]
    colors: list[RGBA]

    def __init__(self,links : list[int],colors: list[RGBA]) -> 'VertexRope':
        self.links = links
        self.colors = colors

cube_translator = vec3d(1.5,0.0,-7.0,1.0)
triangle_translator = vec3d(-1.5,0.0,-6.0,1.0)

triangle_vertices = [
    vec3d(0.0,1.0,0.0,1.0),
    vec3d(-1.0,-1.0,1.0,1.0),
    vec3d(1.0,-1.0,1.0,1.0),
    vec3d(1.0,-1.0,-1.0,1.0),
    vec3d(-1.0,-1.0,-1.0,1.0)
]
tri_index = [VertexRope([0,1,2],[RGBA(1,0,0),RGBA(0,1,0),RGBA(0,0,1)]),
            VertexRope([0,2,3],[RGBA(1,0,0),RGBA(0,0,1),RGBA(0,1,0)]),
            VertexRope([0,3,4],[RGBA(1,0,0),RGBA(0,1,0),RGBA(0,0,1)]),
            VertexRope([0,4,1],[RGBA(1,0,0),RGBA(0,0,1),RGBA(0,1,0)])]

cube_vertices = [
    vec3d(1.0, 1.0,-1.0,1.0),
    vec3d(-1.0, 1.0,-1.0,1.0),
    vec3d(-1.0, 1.0, 1.0,1.0),
    vec3d(1.0, 1.0, 1.0,1.0),
    vec3d(1.0,-1.0, 1.0,1.0),
    vec3d(-1.0,-1.0, 1.0,1.0),
    vec3d(-1.0,-1.0,-1.0,1.0),
    vec3d(1.0,-1.0,-1.0,1.0)
]

cube_index = [
    VertexRope([0,1,2,3],[RGBA(0,1,0)]),
    VertexRope([2,1,6,5],[RGBA(1.0,0.5,0.0)]),
    VertexRope([3,2,5,4],[RGBA(1,0,0)]),
    VertexRope([4,5,6,7],[RGBA(1,1,0)]),
    VertexRope([7,6,1,0],[RGBA(0,0,1)]),
    VertexRope([0,3,4,7],[RGBA(1,0,1)])]

triangle = Polygon(triangle_vertices)
cube = Polygon(cube_vertices)
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

def DrawTriangle(triangle: Polygon):
    glLoadIdentity()
    glBegin(GL_TRIANGLES)
    vertices = triangle.vertices_to_vectors()
    for rope in tri_index:
        for i in range(len(rope.links)):
            rgb = rope.colors[i]
            glColor3f(rgb.r,rgb.b,rgb.g)	
            glVertex3f(vertices[rope.links[i]].x,vertices[rope.links[i]].y,vertices[rope.links[i]].z)
    
    glEnd()
    
    
def DrawCube(cube: Polygon):
    glLoadIdentity()
    glBegin(GL_QUADS)
    vertices = cube.vertices_to_vectors()

    for rope in cube_index:
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


def keyPressed(key, x, y):
    translate_models()
    if ord(key) == 27:
        glutLeaveMainLoop()
    elif(ord(key) == 119):
        matris = triangle.vertices.create_scale_matrix(2)
        triangle.transformate(matris)
        cube.transformate(matris)
    elif(ord(key) == 115):
        matris = triangle.vertices.create_scale_matrix(0.5)
        triangle.transformate(matris)
        cube.transformate(matris)
    elif(ord(key) == 8):
        undo_models()
    elif(ord(key) == 32):
        rotate_models()
    untranslate_models()

def undo_models():
    triangle.undo()
    cube.undo()

def rotate_models():
    triangle.rotate(2)
    cube.rotate(2)

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
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)
    InitGL(640, 480)
    glutMainLoop()

print ("Hit ESC key to quit.")
main()
