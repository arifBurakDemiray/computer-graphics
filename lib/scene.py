# CENG 487 Assignment4 by
# Arif Burak Demiray
# December 2021

from typing import Any
from OpenGL.raw.GL.VERSION.GL_1_0 import GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, glClear, glColor3f
from OpenGL.raw.GLUT import glutBitmapCharacter
from OpenGL.GLUT.fonts import GLUT_BITMAP_HELVETICA_10
from OpenGL.raw.GL.VERSION.GL_1_4 import glWindowPos2f
from OpenGL.raw.GLUT import glutSwapBuffers
from OpenGL.raw.GLUT.constants import *
from OpenGL.GLUT.freeglut import glutLeaveMainLoop
from lib.exporter import export_as_obj
from .populator import Populator


class Scene:

    populators: 'list[Populator]'
    is_process: bool = False

    def __init__(self) -> None:
        self.populators = []

    def subscribe(self, populator: Populator) -> None:
        self.populators.append(populator)

    def unsubscribe(self, populator: Populator) -> None:
        self.populators.remove(populator)

    def unsubscribe(self) -> None:
        self.populators.__delitem__(-1)

    def draw(self) -> None:

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for populator in self.populators:
            populator.draw()
        self.is_process = False

        self.print_menu(480)

        glutSwapBuffers()

    def print_menu(self, height) -> None:
        menu = [
            "Hit ESC key to quit",
            "Hit + to increase subdivide",
            "Hit - to decrease subdivide",
            "Hit RIGHT Arrow Key to rotate right by y axis",
            "Hit LEFT Arrow Key to rotate left by y axis",
            "Hit UP Arrow Key to rotate up by x axis",
            "Hit DOWN Arrow Key to rotate down by x axis",
            "Hit * to rotate up by z axis",
            "Hit / to rotate down by z axis",
            "Hit BACKSPACE to Undo",
            "Hit PAGE UP to zoom in",
            "Hit PAGE DOWN to zoom out",
            "Hit S export as obj file",
            "Use your mouse to move camera (it is in early stage)"]
        h_buff = -10
        for text in menu:
            glColor3f(1, 1, 1)
            glWindowPos2f(2, height+h_buff)
            for i in range(len(text)):
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_10, ord(text[i]))
            h_buff -= 10

    def idle(self) -> None:
        if(self.is_process):
            self.draw()

    def process(self, args: 'list[Any]' = []) -> None:

        populator = self.populators[0]

        populator.untranslate_models()

        key = args[0]

        if key == GLUT_KEY_LEFT:  # left
            populator.models[0].rotate_y(5)
        elif key == GLUT_KEY_RIGHT:  # right
            populator.models[0].rotate_y(-5)
        elif key == GLUT_KEY_UP:  # up
            populator.models[0].rotate_x(5)
        elif key == GLUT_KEY_DOWN:  # down
            populator.models[0].rotate_x(-5)
        elif key == GLUT_KEY_PAGE_UP:  # zoom in
            populator.models[0].scale(2)
        elif key == GLUT_KEY_PAGE_DOWN:  # zoom out
            populator.models[0].scale(0.5)
        elif key == 27:  # Esc leave
            glutLeaveMainLoop()
        elif key == 43:  # + subdive
            populator.populate_up()
        elif key == 45:  # - subdivide
            populator.populate_down()
        elif(key == 8):  # Backspace undo
            populator.models[0].undo()
        elif(key == 42):  # * rotate z positive
            populator.models[0].rotate_z(5)
        elif(key == 47):  # / rotate z negative
            populator.models[0].rotate_z(-5)
        elif(key == 115):  # S save
            export_as_obj(populator.models[0], args[1])
        elif(key == "t"):  # translate
            populator.translate_models()
        elif(key == "C"):  # camera movement
            populator.models[0].project(args[1])

        populator.translate_models()

        self.is_process = True
