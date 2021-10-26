# CENG 487 Assignment1 by
# Arif Burak Demiray
# StudentId: 250201022
# October 2021

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


class VertexLink:
    """
    This class holds links informations of vertices and colors of them
    """
    links: list[int]
    colors: list[RGBA]

    def __init__(self, links: list[int], colors: list[RGBA]) -> None:
        self.links = links
        self.colors = colors
