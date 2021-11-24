# CENG 487 Assignment3 by
# Arif Burak Demiray
# StudentId: 250201022
# November 2021

from typing import Any
from OpenGL.raw.GLUT.constants import *
from OpenGL.GLUT.freeglut import glutLeaveMainLoop
from lib.exporter import export_as_obj
from .populator import Populator

class Scene:

    populators : 'list[Populator]'

    def __init__(self) -> None:
        self.populators = []

    def subscribe(self,populator: Populator) -> None:
        self.populators.append(populator)

    def unsubscribe(self,populator: Populator) -> None:
        self.populators.remove(populator)
    
    def unsubscribe(self) -> None:
        self.populators.__delitem__(-1)

    def draw(self) -> None:
        for populator in self.populators:
            populator.draw()

    def process(self, args : 'list[Any]' = []) -> None:

        populator = self.populators[0]

        populator.untranslate_models()

        key = args[0]

        if key == GLUT_KEY_LEFT: #left
            populator.models[0].rotate_y(5)
        elif key == GLUT_KEY_RIGHT: #right
            populator.models[0].rotate_y(-5)
        elif key == GLUT_KEY_UP: #up
            populator.models[0].rotate_x(5)
        elif key == GLUT_KEY_DOWN: #down
            populator.models[0].rotate_x(-5)
        elif key == GLUT_KEY_PAGE_UP: #zoom in
            populator.models[0].scale(2)
        elif key == GLUT_KEY_PAGE_DOWN: #zoom out
            populator.models[0].scale(0.5)
        elif key == 27:  # Esc leave
            glutLeaveMainLoop()
        elif key == 43: #+ subdive
            populator.populate_up()
        elif key == 45: #- subdivide
            populator.populate_down()
        elif(key == 8):  # Backspace undo
            populator.models[0].undo()
        elif(key == 42): #* rotate z positive 
            populator.models[0].rotate_z(5)
        elif(key == 47): #/ rotate z negative
            populator.models[0].rotate_z(-5)
        elif(key == 115): #S save
            export_as_obj(populator.models[0],args[1])
        elif(key == "t"):
            populator.translate_models()
        elif(key == "C"):
            populator.models[0].project(args[1])

        populator.translate_models()