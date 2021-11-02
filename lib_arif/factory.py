# CENG 487 Assignment2 by
# Arif Burak Demiray
# StudentId: 250201022
# November 2021

from numpy.lib.type_check import real
from .polygon import Polygon
from .vec3d import vec3d
from .vertex_color import RGBA, VertexLink
import numpy


def create_triangle() -> Polygon:
    """
    This function creates a triangle polygon for the main app

    Returns:

    A triangle polygon
    """
    return Polygon([
        vec3d(0.0, 1.0, 0.0, 1.0),
        vec3d(-1.0, -1.0, 1.0, 1.0),
        vec3d(1.0, -1.0, 1.0, 1.0),
        vec3d(1.0, -1.0, -1.0, 1.0),
        vec3d(-1.0, -1.0, -1.0, 1.0)
    ],
        [
        VertexLink([0, 1, 2], [RGBA(1, 0, 0), RGBA(0, 1, 0), RGBA(0, 0, 1)]),
        VertexLink([0, 2, 3], [RGBA(1, 0, 0), RGBA(0, 0, 1), RGBA(0, 1, 0)]),
        VertexLink([0, 3, 4], [RGBA(1, 0, 0), RGBA(0, 1, 0), RGBA(0, 0, 1)]),
        VertexLink([0, 4, 1], [RGBA(1, 0, 0), RGBA(0, 0, 1), RGBA(0, 1, 0)])
    ])


def create_sub_level_cyclinder(parts: int, radius: float, level: int = 0) -> Polygon:
    vertices : list[vec3d] = []
    links : list[VertexLink]  = []
    link_circle : list[int] = []
    i : int = 0

    for vertex in range(0, parts):
        angle  = float(vertex) * 1.0 * numpy.pi / parts
        points : list[float] = [numpy.cos(angle)*radius, numpy.sin(angle)*radius]
        link_circle.append(i)
        vertices.append(vec3d(points[0],2,points[1],1.0))
        vertices.append(vec3d(points[0],-2,points[1],1.0))
        links.append(VertexLink([i % (parts*2),(i+1) % (parts*2),
        (i+3) % (parts*2),(i+2) % (parts*2)],[RGBA.pick_random_color()]))
        i+=2
    links.append(VertexLink(link_circle,[RGBA.pick_random_color()]))
    return Polygon(vertices,links,level)

def create_cube() -> Polygon:
    """
    This function creates a cube polygon for the main app

    Returns:

    A cube polygon
    """
    return Polygon([
        vec3d(1.0, 1.0, -1.0, 1.0),
        vec3d(-1.0, 1.0, -1.0, 1.0),
        vec3d(-1.0, 1.0, 1.0, 1.0),
        vec3d(1.0, 1.0, 1.0, 1.0),
        vec3d(1.0, -1.0, 1.0, 1.0),
        vec3d(-1.0, -1.0, 1.0, 1.0),
        vec3d(-1.0, -1.0, -1.0, 1.0),
        vec3d(1.0, -1.0, -1.0, 1.0)
    ],
        [
        VertexLink([2, 1, 6, 5], [RGBA.pick_random_color()]),
        VertexLink([3, 2, 5, 4], [RGBA.pick_random_color()]),
    ]
    )
#/2, x,y,z xy, xz, yz, xyz
def create_sub_level_cubes(level: int,parent: Polygon, factor: float) -> list[Polygon]:

    if(parent.level != level-1):
        return None

    first_sub : Polygon = parent.create_hard_copy(level,[
        VertexLink([2, 1, 6, 5], [RGBA.pick_random_color()]),
        VertexLink([3, 2, 5, 4], [RGBA.pick_random_color()]),
    ])
    first_sub.scale(0.5)

    translation : vec3d = vec3d(
        parent.vertices.content[20],parent.vertices.content[21],parent.vertices.content[22],1.0).subtract(
            vec3d(first_sub.vertices.content[20],first_sub.vertices.content[21],first_sub.vertices.content[22],1.0)) 

    first_sub.translate(translation.x,translation.y,translation.z)

    sub_vectors : list[vec3d] = [
        vec3d(factor,0.0,0.0,1.0),
        vec3d(0.0,factor,0.0,1.0),
        vec3d(0.0,0.0,factor,1.0),
        vec3d(factor,factor,0.0,1.0),
        vec3d(factor,0.0,factor,1.0),
        vec3d(0.0,factor,factor,1.0),
        vec3d(factor,factor,factor,1.0)
    ]

    result_list = [first_sub]

    for sub_vector in sub_vectors:
        temp : Polygon = first_sub.create_hard_copy(level,[
        VertexLink([2, 1, 6, 5], [RGBA.pick_random_color()]),
        VertexLink([3, 2, 5, 4], [RGBA.pick_random_color()]),
    ])
        temp.translate(sub_vector.x,sub_vector.y,sub_vector.z)
        result_list.append(temp)


    return result_list
  
def F(u,v,r) -> vec3d:
    return vec3d(numpy.cos(u)*numpy.sin(v)*r, numpy.cos(v)*r, numpy.sin(u)*numpy.sin(v)*r,1.0)


def create_sphere(level: int, factor: int, radius: float) -> Polygon:
    startU=0
    startV=0
    endU=numpy.pi*2
    endV=numpy.pi
    stepU=(endU-startU)/factor
    stepV=(endV-startV)/factor
    result = []

    vertices : list[vec3d] = []
    links: list[VertexLink] = []

    for i in range(factor):
        for j in range(factor):
            u=i*stepU+startU
            v=j*stepV+startV
            un= endU if (i+1==factor) else (i+1)*stepU+startU
            vn= endV if (j+1==factor)  else (j+1)*stepV+startV
            color = RGBA.pick_random_color()
            vertices.extend([F(u, v, radius),F(u, vn, radius),F(un, v, radius),F(un, vn, radius)])
            len_vert = len(vertices) -1
            links.extend([VertexLink([len_vert-3,len_vert-1,len_vert-2],[color]),
            VertexLink([len_vert,len_vert-2,len_vert-1],[color])])
        

    return Polygon(vertices,links,level)

def create_trapezoid() -> list[Polygon]:
    """
    This function creates a cube polygon for the main app

    Returns:

    A cube polygon
    """

    result : list[Polygon] = []

    radiues = [1,0.75,0.5]
    ys = [0,0.25,0.5]

    for reversed in [1,-1]:
        for z in range(2):
            vertices : list[vec3d] = []
            links : list[VertexLink]  = []
            i : int = 0
            for vertex in range(0, 32):
                angle  = float(vertex) * 1.0 * numpy.pi / 32
                points : list[float] = [numpy.cos(angle)*radiues[z+1], numpy.sin(angle)*1]
                points1 : list[float] = [numpy.cos(angle)*radiues[z], numpy.sin(angle)*1.5]

                vertices.append(vec3d(points[0],ys[z+1]*reversed,points[1],1.0))
                vertices.append(vec3d(points1[0],ys[z]*reversed,points1[1],1.0))
                links.append(VertexLink([i % (32*2),(i+1) % (32*2),
                (i+3) % (32*2),(i+2) % (32*2)],[RGBA.pick_random_color()]))
                i+=2
            result.append(Polygon(vertices,links))
    return result

    return Polygon([
        vec3d(0.75, 0.75, -0.75, 1.0),
        vec3d(-0.35, 0.75, -0.35, 1.0),
        vec3d(-0.35, 0.75, 0.35, 1.0),
        vec3d(0.35, 0.75, 0.35, 1.0),
        vec3d(0.75, -0.75, 0.75, 1.0),
        vec3d(-0.75, -0.75, 0.75, 1.0),
        vec3d(-0.75, -0.75, -0.75, 1.0),
        vec3d(0.75, -0.75, -0.75, 1.0)
    ],
        [
        VertexLink([2, 1, 6, 5], [RGBA.pick_random_color()]),
        VertexLink([3, 2, 5, 4], [RGBA.pick_random_color()]),
    ]
    )