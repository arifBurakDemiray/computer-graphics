# CENG 487 Assignment6 by
# Arif Burak Demiray
# December 2021

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from project.texture import initTextures
from .shader import Shader

from .vector import *
from .matrix import *
from .shapes import *
from .scene import *
from .defs import *


class Event:
    def __init__(self):
        self.x = -1
        self.y = -1
        self.button = -1
        self.state = -1
        self.altPressed = False


# String containing fragment shader program written in GLSL


class View:
    def __init__(self, camera, grid, scene=None):
        self.camera = camera
        self.grid = grid
        self.scene = scene
        self.bgColor = ColorRGBA(0.15, 0.15, 0.15, 1.0)
        self.cameraIsMoving = False
        self.objectAnimOn = False
        self.event = Event()
        self.mouseX = -1
        self.mouseY = -1
        self.programID = -1
        self.shader = Shader()
        self.percent = 0
        self.textures = [0, 1]

    def initProgram(self):
        shaderList = []

        shaderList.append(self.createShader(GL_VERTEX_SHADER, self.shader.get_vertex_shader()))
        shaderList.append(self.createShader(GL_FRAGMENT_SHADER, self.shader.get_fragment_shader()))

        self.programID = self.createProgram(shaderList)

        for shader in shaderList:
            glDeleteShader(shader)

        initTextures(self.programID, self.textures)

    def draw(self):

        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(self.programID)

        percentLocation = glGetUniformLocation(self.programID, "percent")
        glUniform1i(percentLocation, self.percent)

        viewLocation = glGetUniformLocation(self.programID, "view")
        glUniformMatrix4fv(viewLocation, 1, GL_FALSE, self.camera.getViewMatrix())

        projLocation = glGetUniformLocation(self.programID, "proj")
        glUniformMatrix4fv(projLocation, 1, GL_FALSE, self.camera.getProjMatrix())

        # first draw grid
        modelLocation = glGetUniformLocation(self.programID, "model")
        glUniformMatrix4fv(modelLocation, 1, GL_FALSE, self.grid.obj2World.asNumpy())
        self.grid.draw()

        for node in self.scene.nodes:
            modelLocation = glGetUniformLocation(self.programID, "model")
            glUniformMatrix4fv(modelLocation, 1, GL_FALSE, node.obj2World.asNumpy())
            node.draw()

        glUseProgram(0)
        glutSwapBuffers()

    def setScene(self, scene):
        self.scene = scene

    def setObjectAnim(self, onOff):
        self.objectAnimOn = onOff

    def isObjectAnim(self):
        return self.objectAnimOn

    def setCameraIsMoving(self, onOff):
        self.cameraIsMoving = onOff

    def isCameraMoving(self):
        return self.cameraIsMoving

    # The function called whenever a key is pressed.

    def keyPressed(self, key, x, y):
        # If escape is pressed, kill everything.
        # ord() is needed to get the keycode
        if ord(key) == 27:
            # Escape key = 27
            glutLeaveMainLoop()
            glDeleteTextures(2, self.textures)
            return
        if key == b'f':
            self.camera.reset()
            self.draw()

        if key == b'4':
            for node in self.scene.nodes:
                if not node.fixedDrawStyle:
                    node.drawStyle = DrawStyle.WIRE
                    node.wireOnShaded = False
                    self.draw()

        if key == b'5':
            for node in self.scene.nodes:
                if not node.fixedDrawStyle:
                    node.drawStyle = DrawStyle.SMOOTH
                    node.wireOnShaded = False
                    self.draw()

        if key == b'6':
            for node in self.scene.nodes:
                if not node.fixedDrawStyle and node.drawStyle != DrawStyle.WIRE:
                    node.wireOnShaded = True
                    self.draw()

        if key == b'+':
            self.percent += 5
            if(self.percent >= 100):
                self.percent = 100
            self.draw()
        if key == b'-':
            self.percent -= 5
            if(self.percent <= 0):
                self.percent = 0
            self.draw()
    # The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)

    def resizeView(self, width, height):
        if height == 0:						# Prevent A Divide By Zero If The Window Is Too Small
            height = 1

        glViewport(0, 0, width, height)		# Reset The Current Viewport And Perspective Transformation
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.camera.fov, float(width) / float(height), self.camera.near, self.camera.far)
        glMatrixMode(GL_MODELVIEW)

    # The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)

    def specialKeyPressed(self, *args):
        if args[0] == GLUT_KEY_LEFT:
            self.camera.eye.x -= .5
            self.camera.center.x -= .5
            self.draw()  # computeFrame

        if args[0] == GLUT_KEY_RIGHT:
            self.camera.eye.x += .5
            self.camera.center.x += .5
            self.draw()

    def createShader(self, shaderType, shaderCode):
        shaderID = glCreateShader(shaderType)
        glShaderSource(shaderID, shaderCode)
        glCompileShader(shaderID)

        status = None
        glGetShaderiv(shaderID, GL_COMPILE_STATUS, status)
        if status == GL_FALSE:
            # Note that getting the error log is much simpler in Python than in C/C++
            # and does not require explicit handling of the string buffer
            strInfoLog = glGetShaderInfoLog(shaderID)
            strShaderType = ""
            if shaderType is GL_VERTEX_SHADER:
                strShaderType = "vertex"
            elif shaderType is GL_GEOMETRY_SHADER:
                strShaderType = "geometry"
            elif shaderType is GL_FRAGMENT_SHADER:
                strShaderType = "fragment"

            print(b"Compilation failure for " + strShaderType + b" shader:\n" + strInfoLog)

        return shaderID

    def createProgram(self, shaderList):
        programID = glCreateProgram()

        for shader in shaderList:
            glAttachShader(programID, shader)

        glLinkProgram(programID)

        status = glGetProgramiv(programID, GL_LINK_STATUS)
        if status == GL_FALSE:
            strInfoLog = glGetProgramInfoLog(programID)
            print(b"Linker failure: \n" + strInfoLog)

        # important for cleanup
        for shaderID in shaderList:
            glDetachShader(programID, shaderID)

        return programID

    def mousePressed(self, button, state, x, y):
        self.event.x = x
        self.event.y = y
        self.event.state = state
        self.event.button = button

        # get status of alt key
        m = glutGetModifiers()
        self.event.altPressed = m & GLUT_ACTIVE_ALT

        self.mouseX = x
        self.mouseY = y

        if state == 0:
            if self.event.altPressed > 0:
                self.setCameraIsMoving(True)
        else:
            self.setCameraIsMoving(False)

    def mouseMove(self, x, y):
        if not self.event.altPressed:
            return

        xSpeed = 0.02
        ySpeed = 0.02
        xOffset = (x - self.mouseX) * xSpeed
        yOffset = (y - self.mouseY) * ySpeed

        if (self.event.button == GLUT_RIGHT_BUTTON):
            self.camera.zoom(xOffset)
            self.camera.roll(yOffset)
        elif (self.event.button == GLUT_MIDDLE_BUTTON):
            self.camera.dolly(-xOffset, yOffset, 0)
        elif (self.event.button == GLUT_LEFT_BUTTON):
            self.camera.yaw(xOffset)
            self.camera.pitch(yOffset)
            self.camera.dollyCamera(-xOffset, yOffset, 0)

        # store last positions
        self.mouseX = x
        self.mouseY = y

        # remember this point
        self.event.x = x
        self.event.y = y

    # The main drawing function

    def idleFunction(self):
        if self.isObjectAnim() or self.isCameraMoving():
            self.draw()


class Grid(_Shape):
    def __init__(self, name, xSize, zSize):
        vertices = []
        for x in range(-xSize, xSize + 1, 2):
            for z in range(-zSize, zSize + 1, 2):
                vertices.append(Point3f(x, 0, z))

        faces = []
        for x in range(0, xSize * zSize):
            indexX = x % xSize
            indexZ = x // zSize
            id1 = indexZ * (xSize + 1) + indexX
            id2 = (indexZ + 1) * (xSize + 1) + indexX
            faces.append([id1, id1 + 1, id2 + 1, id2])

        _Shape.__init__(self, name, vertices, faces, [], [])

        self.fixedDrawStyle = True

        self.setWireColor(0.3, 0.3, 0.3, 1.0)
        self.xAxisColor = ColorRGBA(0.4, 0.0, 0.0, 1.0)
        self.zAxisColor = ColorRGBA(0.0, 0.4, 0.0, 1.0)
        self.yAxisColor = ColorRGBA(0.0, 0.0, 0.4, 1.0)
        self.axisWidth = 2

        self.originColor = ColorRGBA(0.4, 0.4, 0.4, 1.0)
        self.originRadius = 4

        self.xSize = xSize
        self.zSize = zSize

    def setXAxisColor(self, r, g, b, a):
        self.xAxisColor = ColorRGBA(r, g, b, a)

    def setYAxisColor(self, r, g, b, a):
        self.yAxisColor = ColorRGBA(r, g, b, a)

    def setZAxisColor(self, r, g, b, a):
        self.zAxisColor = ColorRGBA(r, g, b, a)

    def setMainAxisWidth(self, width):
        self.mainAxisWidth = width
