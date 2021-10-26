# CENG 487 Assignment1 by
# Arif Burak Demiray
# StudentId: 250201022
# October 2021

from types import FunctionType
from vec3d import vec3d


class RGBA:
    r : float
    g : float
    b : float
    a : float

    def __init__(self,r : float, g : float, b : float, a : float = 0.0) -> 'RGBA':
        self.r = r
        self.b = b
        self.g = g
        self.a = a

class VertexRope:
    links : list[int]
    colors: list[RGBA]

    def __init__(self,links : list[int],colors: list[RGBA]) -> 'VertexRope':
        self.links = links
        self.colors = colors