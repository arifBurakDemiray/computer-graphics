# CENG 487 Assignment6 by
# Arif Burak Demiray
# December 2021

from PIL import Image
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import numpy


def initTextures(programID, textures):

    glUseProgram(programID)
    glGenTextures(2, textures)
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, textures[0])

    image = Image.open("texture/white_wolf.png").transpose(Image.FLIP_TOP_BOTTOM)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.size[0], image.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE,
                 numpy.frombuffer(image.tobytes(), dtype=numpy.uint8))
    glUniform1i(glGetUniformLocation(programID, "tex1"), 0)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glActiveTexture(GL_TEXTURE1)
    glBindTexture(GL_TEXTURE_2D, textures[1])
    image = Image.open("texture/lady_of_the_time.png").transpose(Image.FLIP_TOP_BOTTOM)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.size[0], image.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE,
                 numpy.frombuffer(image.tobytes(), dtype=numpy.uint8))
    glUniform1i(glGetUniformLocation(programID, "tex2"), 1)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glUseProgram(0)
