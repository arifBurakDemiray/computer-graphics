# CENG 487 Assignment2 by
# Arif Burak Demiray
# StudentId: 250201022
# November 2021

from .factory import create_cube,create_sub_level_cyclinder,create_sub_level_cubes, create_sphere
from .polygon import Polygon
from .vec3d import vec3d
from OpenGL.GL import *

class Populator:

    models: list[Polygon]
    translator: vec3d
    level : int

    def __init__(self) -> None:
        self.level = 0

    def populate_up(self) -> None:
        pass

    def populate_down(self) -> None:
        pass

    def draw(self) -> None:
        pass

    def translate_models(self) -> None:
        for model in self.models:
            model.plane_translate(0,self.translator)

    def untranslate_models(self) -> None:    
        for model in self.models:
            model.plane_translate(1,self.translator)
    


class CubePopulator(Populator):

    factor: float = 1.0

    def __init__(self) -> None:
        super().__init__()
        self.models = [create_cube()]
        self.translator = vec3d(1.5, 0.0, -7.0, 1.0)

    def populate_up(self) -> None:
        self.level+=1
        sub_models : list[Polygon] = []

        for model in self.models:
            if(model != None and model.level+1==self.level):
                sub_models.extend(create_sub_level_cubes(self.level,model,self.factor))
        self.factor=self.factor/2
        self.models.extend(sub_models)

    def populate_down(self) -> None:
        if(self.level == 0):
            return
        self.factor=self.factor*2
        last_comers = 8**self.level

        for i in range(last_comers):
            self.models.remove(self.models[-1])

        self.level-=1
    
    def draw(self) -> None:
        for model in self.models:
            if(model.level == self.level):
                self.__DrawCube(model)

    def __DrawCube(self,model: Polygon):
        glLoadIdentity()
        glBegin(GL_QUADS)
        vertices = model.vertices_to_vectors()

        for rope in model.vertex_links:
            rgb = rope.colors[0]
            glColor3f(rgb.r, rgb.b, rgb.g) #draw color for each face
            for i in range(len(rope.links)):
                glVertex3f(vertices[rope.links[i]].x,
                        vertices[rope.links[i]].y, vertices[rope.links[i]].z)
        glEnd()

class CyclinderPopulator(Populator):

    parts: int = 8
    radius: float = 1.0

    def __init__(self) -> None:
        super().__init__()
        self.translator = vec3d(1.5, 0.0, -7.0, 1.0)
        self.models = [create_sub_level_cyclinder(self.parts,self.radius)]

    def populate_up(self) -> None:
        self.level+=1

        self.parts = self.parts*2
        
        self.models.append(create_sub_level_cyclinder(self.parts,self.radius,self.level))

    def populate_down(self) -> None:
        if(self.level == 0):
            return
        self.parts=int(self.parts/2)
       
        self.models.remove(self.models[-1])

        self.level-=1

    def draw(self) -> None:
        for cyclinder in self.models:
            if(cyclinder.level == self.level):
                self.__DrawCyclinder(cyclinder)

    def __DrawCyclinder(self,cyclinder: Polygon) -> None:
        glLoadIdentity()
        glBegin(GL_QUADS)    
        vertices = cyclinder.vertices_to_vectors()

        for rope in cyclinder.vertex_links:
            rgb = rope.colors[0]
            glColor3f(rgb.r, rgb.b, rgb.g) #draw color for each face
            for i in range(len(rope.links)):
                glVertex3f(vertices[rope.links[i]].x,
                        vertices[rope.links[i]].y, vertices[rope.links[i]].z)
        glEnd()

class SpherePopulator(Populator):

    parts: int = 4
    radius: float = 1.0

    def __init__(self) -> None:
        super().__init__()
        self.models = [create_sphere(self.level,self.parts,self.radius)]
        self.translator = vec3d(1.5, 0.0, -7.0, 1.0)

    def populate_up(self) -> None:
        self.level+=1

        self.parts = self.parts*2

        self.models.append(create_sphere(self.level,self.parts,self.radius))


    def populate_down(self) -> None:
        if(self.level == 0):
            return
        self.parts=int(self.parts/2)
       
        self.models.remove(self.models[-1])

        self.level-=1
    
    def draw(self) -> None:
        for model in self.models:
            if(model.level == self.level):
                self.__DrawSphere(model)

    def __DrawSphere(self,model: Polygon):
        glLoadIdentity()
        glBegin(GL_TRIANGLES)
        vertices = model.vertices_to_vectors()

        for rope in model.vertex_links:
            rgb = rope.colors[0]
            glColor3f(rgb.r, rgb.b, rgb.g) #draw color for each face
            for i in range(len(rope.links)):
                glVertex3f(vertices[rope.links[i]].x,
                        vertices[rope.links[i]].y, vertices[rope.links[i]].z)
        glEnd()

