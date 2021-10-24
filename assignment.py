# CENG 487 Assignment1 by
# Arif Burak Demiray
# StudentId: 250201022
# October 2021

from mat3d import mat3d
from vec3d import vec3d
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from polygon_helper import vectors_to_matrices
import sys

class Polygon:
    vertices = mat3d
    matrix_stack = [mat3d]

    def __init__(self,vertices: list[vec3d]) -> 'Polygon':
        self.vertices = vectors_to_matrices(vertices)

    def transformate(self, matrix: mat3d) -> None:
        self.matrix_stack.append(matrix)
        self.vertices = self.vertices.calc_multiplacation(matrix)
    

    def vertices_to_vectors(self) -> list[vec3d]:
        
        result = [vec3d]
        
        for i in range(int(len(self.vertices.content)/4) - 1):
            result.append(
                vec3d(i*4,i*4+1,i*4+2,0)
            )
        
        return result

triangle_vertices = [
    vec3d(0.0,1.0,0.0,0.0),
    vec3d(-1.0,-1.0,1.0,0.0),
    vec3d(1.0,-1.0,1.0,0.0),
    vec3d(1.0,-1.0,-1.0,0.0),
    vec3d(-1.0,-1.0,-1.0,0.0)
]

triangle = Polygon(triangle_vertices)

def update_vertices(triangle_vertices):
    print("%s - %s - %s" % (triangle_vertices[0].x,triangle_vertices[0].y,triangle_vertices[0].z))
    triangle_vertices = triangle.vertices_to_vectors()
    print("%s - %s - %s" % (triangle_vertices[0].x,triangle_vertices[0].y,triangle_vertices[0].z))
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
    update_vertices(triangle_vertices)
    global rtri, rquad
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(-1.5,0.0,-6.0)
    glRotatef(rtri,0.0,1.0,0.0)
    glBegin(GL_TRIANGLES)
    for i in range(4):
        glVertex3f(triangle_vertices[0].x,triangle_vertices[0].y,triangle_vertices[0].z)
        glVertex3f(triangle_vertices[i+1].x,triangle_vertices[i+1].y,triangle_vertices[i+1].z)
        if(i==3):
            glVertex3f(triangle_vertices[1].x,triangle_vertices[1].y,triangle_vertices[1].z)
        else:    
            glVertex3f(triangle_vertices[i+2].x,triangle_vertices[i+2].y,triangle_vertices[i+2].z)
    glEnd()
    glLoadIdentity()
    glTranslatef(1.5,0.0,-7.0)
    glRotatef(rquad,1.0,1.0,1.0)
    rtri  = rtri + 0.2
    rquad = rquad - 0.15
    glutSwapBuffers()


def keyPressed(key, x, y):
    if ord(key) == 27:
        glutLeaveMainLoop()
        return
    elif(ord(key) == 13):
        print("boom")
        triangle.transformate(triangle.vertices.create_scale_matrix(2))
        DrawGLScene()
        return


def main():
	global window
	glutInit(sys.argv)

	# Select type of Display mode:
	#  Double buffer
	#  RGBA color
	#  Alpha components supported
	#  Depth buffer
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

	# get a 640 x 480 window
	glutInitWindowSize(640, 480)

	# the window starts at the upper left corner of the screen
	glutInitWindowPosition(0, 0)

	# Okay, like the C version we retain the window id to use when closing, but for those of you new
	# to Python (like myself), remember this assignment would make the variable local and not global
	# if it weren't for the global declaration at the start of main.
	window = glutCreateWindow("CENG487 Development Env Test")

   	# Register the drawing function with glut, BUT in Python land, at least using PyOpenGL, we need to
	# set the function pointer and invoke a function to actually register the callback, otherwise it
	# would be very much like the C version of the code.
	glutDisplayFunc(DrawGLScene)

	# Uncomment this line to get full screen.
	# glutFullScreen()

	# When we are doing nothing, redraw the scene.
	glutIdleFunc(DrawGLScene)

	# Register the function called when our window is resized.
	glutReshapeFunc(ReSizeGLScene)

	# Register the function called when the keyboard is pressed.
	glutKeyboardFunc(keyPressed)

	# Initialize our window.
	InitGL(640, 480)

	# Start Event Processing Engine
	glutMainLoop()

# Print message to console, and kick off the main to get it rolling.
print ("Hit ESC key to quit.")
main()
