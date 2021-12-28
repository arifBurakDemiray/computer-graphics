# CENG 487 Assignment6 by
# Arif Burak Demiray
# StudentId: 250201022
# December 2021

import sys

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from project.obj_parser import ObjParser

from project.vector import *
from project.matrix import *
from project.shapes import *
from project.camera import *
from project.scene import *
from project.view import *

# create grid
grid = Grid("grid", 10, 10)
grid.setDrawStyle(DrawStyle.WIRE)
grid.setWireWidth(1)

# create camera
camera = Camera()
camera.createView(Point3f(0.0, 0.0, 10.0),
                  Point3f(0.0, 0.0, 0.0),
                  Vector3f(0.0, 1.0, 0.0))
camera.setNear(1)
camera.setFar(1000)

# create View
view = View(camera, grid)

# init scene
scene = Scene()
view.setScene(scene)


def check_file(filename: str) -> bool:
    splitted = filename.split("/")
    if(len(splitted) > 1):
        current = os.getcwd()

        pureFile = splitted[-1]

        splitted.remove(splitted[-1])
        os.chdir("/".join(splitted))

        result = pureFile in os.listdir()
        os.chdir(current)
        return result

    else:
        return filename in os.listdir()


def main():
    global view

    if(len(sys.argv) < 2):
        print("usage\n\tpython3 assigment3.py filename\n\tpython assigment3.py filename")
        return

    splitted = sys.argv[1].split("/")[-1].split(".")[1]

    if(splitted not in ["obj", "OBJ"]):
        print("\n\tplease provide an obj format file\n")
        return

    if(not check_file(sys.argv[1])):
        print("\n\tplease provide an existing file\n")
        return

    parser = ObjParser(sys.argv[1])  # read file name
    obj = parser.parse()  # parse it
    obj.Translate(-2, 0, 0)
    scene.add(obj)

    glutInit(sys.argv)

    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

    glutInitWindowSize(640, 480)
    glutInitWindowPosition(200, 200)

    glutCreateWindow("CENG487 Assigment 5")

    # define callbacks
    glutDisplayFunc(view.draw)
    glutIdleFunc(view.idleFunction)
    glutReshapeFunc(view.resizeView)
    glutKeyboardFunc(view.keyPressed)
    glutSpecialFunc(view.specialKeyPressed)
    glutMouseFunc(view.mousePressed)
    glutMotionFunc(view.mouseMove)

    view.initProgram()

    glutMainLoop()


# Print message to console, and kick off the main to get it rolling.
print("Hit ESC key to quit.\nHit 6 :)")

if __name__ == '__main__':
    main()
