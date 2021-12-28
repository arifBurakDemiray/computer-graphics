from PIL import Image
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import numpy


def initTextures(programID):
    glUseProgram(programID)

    tex1ID = loadTexture("texture/white_wolf.png")

    # set shader stuff
    tex1Location = glGetUniformLocation(programID, "tex1")
    glUniform1i(tex1Location, tex1ID)

    # now activate texture units
    glActiveTexture(GL_TEXTURE0 + tex1ID)
    glBindTexture(GL_TEXTURE_2D, tex1ID)

    tex2ID = loadTexture("texture/lady_of_the_time.png")

    # set shader stuff
    tex2Location = glGetUniformLocation(programID, "tex2")
    glUniform1i(tex2Location, tex2ID)

    # now activate texture units
    glActiveTexture(GL_TEXTURE0 + tex2ID)
    glBindTexture(GL_TEXTURE_2D, tex2ID)

    # reset program
    glUseProgram(0)


def loadTexture(texFilename):
    # load texture - flip int verticallt to convert from pillow to OpenGL orientation
    image = Image.open(texFilename).transpose(Image.FLIP_TOP_BOTTOM)

    # create a new id
    texID = glGenTextures(1)
    # bind to the new id for state
    glBindTexture(GL_TEXTURE_2D, texID)

    # set texture params
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # copy texture data
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.size[0], image.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE,
                 numpy.frombuffer(image.tobytes(), dtype=numpy.uint8))
    glGenerateMipmap(GL_TEXTURE_2D)

    return texID
