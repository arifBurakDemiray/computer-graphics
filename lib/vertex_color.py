# CENG 487 Assignment3 by
# Arif Burak Demiray
# StudentId: 250201022
# November 2021

from numpy.random import random_sample

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

    def __init__(self, links: 'list[int]', colors: 'list[RGBA]', level : int = 0) -> None:
        self.links = links
        self.colors = colors
        self.level = level
