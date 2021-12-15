# CENG 487 Assignment5 by
# Arif Burak Demiray
# StudentId: 250201022
# December 2021

import sys

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from vector import *
from matrix import *
from shapes import *
from camera import *
from scene import *
from view import *

# create grid
grid = Grid("grid", 10, 10)
grid.setDrawStyle(DrawStyle.WIRE)
grid.setWireWidth(1)

# create camera
camera = Camera()
camera.createView( 	Point3f(0.0, 0.0, 10.0), \
					Point3f(0.0, 0.0, 0.0), \
					Vector3f(0.0, 1.0, 0.0) )
camera.setNear(1)
camera.setFar(1000)

# create View
view = View(camera, grid)

# init scene
scene = Scene()
view.setScene(scene)

# create objects
cube1 = Cube("cube", 1, 1, 1, 10, 10, 10)
cube1.Translate( 2, 0.5, 0)
scene.add(cube1)

cube2 = Cube("cube", 1.5, 1.5, 1.5, 10, 10, 10)
cube2.Translate( -2, 0, 0)
scene.add(cube2)

def main():
	global view
	glutInit(sys.argv)

	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

	glutInitWindowSize(640, 480)
	glutInitWindowPosition(200, 200)

	window = glutCreateWindow("CENG487 Assigment 5")

	# define callbacks
	glutDisplayFunc( view.draw )
	glutIdleFunc( view.idleFunction )
	glutReshapeFunc( view.resizeView )
	glutKeyboardFunc( view.keyPressed )
	glutSpecialFunc( view.specialKeyPressed )
	glutMouseFunc( view.mousePressed )
	glutMotionFunc( view.mouseMove )

	view.initProgram()


	glutMainLoop()

# Print message to console, and kick off the main to get it rolling.
print("Hit ESC key to quit.")

if __name__ == '__main__':
	main()

