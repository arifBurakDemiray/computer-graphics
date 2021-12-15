# CENG 487 Assignment5 by
# Arif Burak Demiray
# StudentId: 250201022
# December 2021


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from vector import *
from matrix import *
from boundingbox import *
from defs import DrawStyle

__all__ = ['_Shape', 'Cube', 'DrawStyle']


class _Shape:
    def __init__(self, name, vertices, faces):
        self.vertices = vertices
        self.edges = []
        self.faces = faces
        self.colors = []
        self.obj2World = Matrix()
        self.drawStyle = DrawStyle.NODRAW
        self.wireOnShaded = False
        self.wireWidth = 2
        self.name = name
        self.fixedDrawStyle = False
        self.wireColor = ColorRGBA(0.7, 1.0, 0.0, 1.0)
        self.wireOnShadedColor = ColorRGBA(1.0, 1.0, 1.0, 1.0)
        self.bboxObj = BoundingBox()
        self.bboxWorld = BoundingBox()
        self.calcBboxObj()
        self.VBOData = []

    def initBuffers(self):
        self.VBO = glGenBuffers(1)

        # set array buffer to our ID
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)

        elementSize = numpy.dtype(numpy.float32).itemsize

        glBufferData(  # PyOpenGL allows for the omission of the size parameter
            GL_ARRAY_BUFFER,
            elementSize * len(self.VBOData),
            self.VBOData,
            GL_STATIC_DRAW
        )

        # reset array buffer
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def calcBboxObj(self):
        for vertex in self.vertices:
            self.bboxObj.expand(vertex)

    def setDrawStyle(self, style):
        self.drawStyle = style

    def setWireColor(self, r, g, b, a):
        self.wireColor = ColorRGBA(r, g, b, a)

    def setWireWidth(self, width):
        self.wireWidth = width

    def prepareVBD(self):
        finalVertexPositions = []
        finalVertexColors = []

        # go over faces and assemble an array for all vertex data

        faceId = 0

        lastAccessed = [0.0, 0.0, 0.0, 1.0]

        for face in self.faces:
            if self.drawStyle == DrawStyle.FACETED or self.drawStyle == DrawStyle.SMOOTH:
                if(len(self.colors) > 0):
                    lastAccessed = self.colors[faceId].asList()
                else:
                    lastAccessed = [1.0, 0.6, 0.0, 1.0]

            if self.drawStyle == DrawStyle.WIRE or (not self.wireOnShaded):
                if not self.wireOnShaded:
                    if not self.fixedDrawStyle:
                        lastAccessed = self.wireColor.asList()
                    else:
                        lastAccessed = self.wireOnShadedColor.asList()
                else:
                    lastAccessed = self.wireColor.asList()

            for vertex in face:
                finalVertexPositions.extend(self.vertices[vertex].asList())
                finalVertexColors.extend(lastAccessed)

            faceId += 1

        self.VBOData = numpy.array(finalVertexPositions + finalVertexColors, dtype='float32')

    def draw(self):

        self.prepareVBD()
        self.initBuffers()

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        elementSize = numpy.dtype(numpy.float32).itemsize
        offset = 0

        glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, elementSize * 4, ctypes.c_void_p(offset))
        glEnableVertexAttribArray(0)

        offset += elementSize * 4 * len(self.vertices)
        glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, elementSize * 4, ctypes.c_void_p(offset))
        glEnableVertexAttribArray(1)

        type_of_draw = GL_QUADS

        if self.drawStyle == DrawStyle.FACETED or self.drawStyle == DrawStyle.SMOOTH:
            type_of_draw = GL_QUADS
        if self.drawStyle == DrawStyle.WIRE or (not self.wireOnShaded):
            type_of_draw = GL_LINES

        glDrawArrays(type_of_draw, 0, len(self.vertices) * 4)

        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)

        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def Translate(self, x, y, z):
        translate = Matrix.T(x, y, z)
        self.obj2World = self.obj2World.product(translate)


class Cube(_Shape):
    def __init__(self, name, xSize, ySize, zSize, xDiv, yDiv, zDiv):
        vertices = []

        # add corners
        vertices.append(Point3f(-xSize / 2.0, -ySize / 2.0, zSize / 2.0))
        vertices.append(Point3f(xSize / 2.0, -ySize / 2.0, zSize / 2.0))
        vertices.append(Point3f(-xSize / 2.0, ySize / 2.0, zSize / 2.0))
        vertices.append(Point3f(xSize / 2.0, ySize / 2.0, zSize / 2.0))
        vertices.append(Point3f(-xSize / 2.0, -ySize / 2.0, -zSize / 2.0))
        vertices.append(Point3f(xSize / 2.0, -ySize / 2.0, -zSize / 2.0))
        vertices.append(Point3f(-xSize / 2.0, ySize / 2.0, -zSize / 2.0))
        vertices.append(Point3f(xSize / 2.0, ySize / 2.0, -zSize / 2.0))

        faces = []
        faces.append([0, 2, 3, 1])
        faces.append([4, 6, 7, 5])
        faces.append([4, 6, 2, 0])
        faces.append([1, 3, 7, 5])
        faces.append([2, 6, 7, 3])
        faces.append([4, 0, 1, 5])

        _Shape.__init__(self, name, vertices, faces)
        self.drawStyle = DrawStyle.SMOOTH

        for i in range(0, len(faces) + 1):
            self.colors.append(ColorRGBA.pick_random_color())
