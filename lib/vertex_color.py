# CENG 487 Assignment3 by
# Arif Burak Demiray
# StudentId: 250201022
# November 2021

from numpy.random import random_sample
from .vec3d import Vec3d

class RGBA:
    """
    This class holds r,g,b and a values of a color
    """
    r: float
    g: float
    b: float
    a: float

    def __init__(self, r: float, g: float, b: float, a: float = 0.0) -> None:
        self.r = r
        self.b = b
        self.g = g
        self.a = a

    def pick_random_color() -> 'RGBA':
        return RGBA(random_sample(),random_sample(),random_sample())


class VertexLink:
    """
    This class holds links informations of vertices and colors of them
    """
    links: 'list[int]'
    colors: 'list[RGBA]'
    level: int
    face_point : 'Vec3d'

    def __init__(self, links: 'list[int]', colors: 'list[RGBA]', 
    level : int = 0, vec : 'Vec3d' = Vec3d(0,0,0,0)) -> None:
        self.links = links
        self.colors = colors
        self.level = level
        self.face_point = vec

    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            is4 = len(self.links) == 4 and len(other.links) == 4
            iseq = self.links[0] == other.links[0] and self.links[1] == other.links[1] and self.links[2] == other.links[2] and self.links[3] == other.links[3]
            return is4 and iseq
        else:
            return False
