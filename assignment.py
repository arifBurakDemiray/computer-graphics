# CENG 487 Assignment1 by
# Arif Burak Demiray
# StudentId: 250201022
# October 2021

from mat3d import mat3d
from vec3d import vec3d
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys

class Polygon:
    vertices = [vec3d]
    matrix_stack = [mat3d]

    def __init__(self,vertices: list[vec3d]) -> 'Polygon':
        self.vertices = vertices

    def transformate(self, matrix: mat3d) -> 'Polygon':
        self.matrix_stack.append(matrix)
        return self

x = vec3d(1,5,8,1)

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

	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);	# Clear The Screen And The Depth Buffer
	glLoadIdentity();				# Reset The View
	glTranslatef(-1.5,0.0,-6.0);	# Move Left And Into The Screen

	glRotatef(rtri,0.0,1.0,0.0);	# Rotate The Pyramid On It's Y Axis

	glBegin(GL_TRIANGLES);			# Start Drawing The Pyramid

	glColor3f(1.0,0.0,0.0);			# Red
	glVertex3f( 0.0, 1.0, 0.0);		# Top Of Triangle (Front)
	glColor3f(0.0,1.0,0.0);			# Green
	glVertex3f(-1.0,-1.0, 1.0);		# Left Of Triangle (Front)
	glColor3f(0.0,0.0,1.0);			# Blue
	glVertex3f( 1.0,-1.0, 1.0);

	glColor3f(1.0,0.0,0.0);			# Red
	glVertex3f( 0.0, 1.0, 0.0);		# Top Of Triangle (Right)
	glColor3f(0.0,0.0,1.0);			# Blue
	glVertex3f( 1.0,-1.0, 1.0);		# Left Of Triangle (Right)
	glColor3f(0.0,1.0,0.0);			# Green
	glVertex3f( 1.0,-1.0, -1.0);	# Right

	glColor3f(1.0,0.0,0.0);			# Red
	glVertex3f( 0.0, 1.0, 0.0);		# Top Of Triangle (Back)
	glColor3f(0.0,1.0,0.0);			# Green
	glVertex3f( 1.0,-1.0, -1.0);	# Left Of Triangle (Back)
	glColor3f(0.0,0.0,1.0);			# Blue
	glVertex3f(-1.0,-1.0, -1.0);	# Right Of


	glColor3f(1.0,0.0,0.0);			# Red
	glVertex3f( 0.0, 1.0, 0.0);		# Top Of Triangle (Left)
	glColor3f(0.0,0.0,1.0);			# Blue
	glVertex3f(-1.0,-1.0,-1.0);		# Left Of Triangle (Left)
	glColor3f(0.0,1.0,0.0);			# Green
	glVertex3f(-1.0,-1.0, 1.0);		# Right Of Triangle (Left)
	glEnd();


	glLoadIdentity();
	glTranslatef(1.5,0.0,-7.0);		# Move Right And Into The Screen
	glRotatef(rquad,1.0,1.0,1.0);	# Rotate The Cube On X, Y & Z
	glBegin(GL_QUADS);				# Start Drawing The Cube


	glColor3f(0.0,1.0,0.0);			# Set The Color To Blue
	glVertex3f( 1.0, 1.0,-1.0);		# Top Right Of The Quad (Top)
	glVertex3f(-1.0, 1.0,-1.0);		# Top Left Of The Quad (Top)
	glVertex3f(-1.0, 1.0, 1.0);		# Bottom Left Of The Quad (Top)
	glVertex3f( 1.0, 1.0, 1.0);		# Bottom Right Of The Quad (Top)

	glColor3f(1.0,0.5,0.0);			# Set The Color To Orange
	glVertex3f( 1.0,-1.0, 1.0);		# Top Right Of The Quad (Bottom)
	glVertex3f(-1.0,-1.0, 1.0);		# Top Left Of The Quad (Bottom)
	glVertex3f(-1.0,-1.0,-1.0);		# Bottom Left Of The Quad (Bottom)
	glVertex3f( 1.0,-1.0,-1.0);		# Bottom Right Of The Quad (Bottom)

	glColor3f(1.0,0.0,0.0);			# Set The Color To Red
	glVertex3f( 1.0, 1.0, 1.0);		# Top Right Of The Quad (Front)
	glVertex3f(-1.0, 1.0, 1.0);		# Top Left Of The Quad (Front)
	glVertex3f(-1.0,-1.0, 1.0);		# Bottom Left Of The Quad (Front)
	glVertex3f( 1.0,-1.0, 1.0);		# Bottom Right Of The Quad (Front)

	glColor3f(1.0,1.0,0.0);			# Set The Color To Yellow
	glVertex3f( 1.0,-1.0,-1.0);		# Bottom Left Of The Quad (Back)
	glVertex3f(-1.0,-1.0,-1.0);		# Bottom Right Of The Quad (Back)
	glVertex3f(-1.0, 1.0,-1.0);		# Top Right Of The Quad (Back)
	glVertex3f( 1.0, 1.0,-1.0);		# Top Left Of The Quad (Back)

	glColor3f(0.0,0.0,1.0);			# Set The Color To Blue
	glVertex3f(-1.0, 1.0, 1.0);		# Top Right Of The Quad (Left)
	glVertex3f(-1.0, 1.0,-1.0);		# Top Left Of The Quad (Left)
	glVertex3f(-1.0,-1.0,-1.0);		# Bottom Left Of The Quad (Left)
	glVertex3f(-1.0,-1.0, 1.0);		# Bottom Right Of The Quad (Left)

	glColor3f(1.0,0.0,1.0);			# Set The Color To Violet
	glVertex3f( 1.0, 1.0,-1.0);		# Top Right Of The Quad (Right)
	glVertex3f( 1.0, 1.0, 1.0);		# Top Left Of The Quad (Right)
	glVertex3f( 1.0,-1.0, 1.0);		# Bottom Left Of The Quad (Right)
	glVertex3f( 1.0,-1.0,-1.0);		# Bottom Right Of The Quad (Right)
	glEnd();						# Done Drawing The Quad

	rtri  = rtri + 0.2				# Increase The Rotation Variable For The Triangle
	rquad = rquad - 0.15			# Decrease The Rotation Variable For The Quad

	#  since this is double buffered, swap the buffers to display what just got drawn.
	glutSwapBuffers()


# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)
def keyPressed(key, x, y):
	# If escape is pressed, kill everything.
	# ord() is needed to get the keycode
	if ord(key) == 27:
		# Escape key = 27
		glutLeaveMainLoop()
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
