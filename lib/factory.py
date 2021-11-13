# CENG 487 Assignment2 by
# Arif Burak Demiray
# StudentId: 250201022
# November 2021

from .polygon import Polygon
from .vec3d import Vec3d
from .vertex_color import RGBA, VertexLink
import numpy


def create_triangle() -> Polygon:
    """
    This function creates a triangle polygon for the main app

    Returns:

    A triangle polygon
    """
    return Polygon([
        Vec3d(0.0, 1.0, 0.0, 1.0),
        Vec3d(-1.0, -1.0, 1.0, 1.0),
        Vec3d(1.0, -1.0, 1.0, 1.0),
        Vec3d(1.0, -1.0, -1.0, 1.0),
        Vec3d(-1.0, -1.0, -1.0, 1.0)
    ],
        [
        VertexLink([0, 1, 2], [RGBA(1, 0, 0), RGBA(0, 1, 0), RGBA(0, 0, 1)]),
        VertexLink([0, 2, 3], [RGBA(1, 0, 0), RGBA(0, 0, 1), RGBA(0, 1, 0)]),
        VertexLink([0, 3, 4], [RGBA(1, 0, 0), RGBA(0, 1, 0), RGBA(0, 0, 1)]),
        VertexLink([0, 4, 1], [RGBA(1, 0, 0), RGBA(0, 0, 1), RGBA(0, 1, 0)])
    ])


def create_sub_level_cyclinder(parts: int, radius: float, level: int = 0) -> Polygon:
    """
    Creates sub level cyclinders by given parts and radius

    Parameters:

    parts is how many subdivisions occurs
    radius is radius of the cyclinder
    level is level of the model

    Returns:

    Creates cyclinder    
    """
    vertices: list[Vec3d] = []
    links: list[VertexLink] = []
    link_circle: list[int] = []
    i: int = 0

    for y in range(parts):
        angle = float(y) * 1.0 * numpy.pi / parts  # calculate part degree
        points: list[float] = [
            numpy.cos(angle)*radius, numpy.sin(angle)*radius]
        link_circle.append(i)  # for the upper circle
        # upper points of the cyclinder
        vertices.append(Vec3d(points[0], 2, points[1], 1.0))
        # down points of the cyclinder
        vertices.append(Vec3d(points[0], -2, points[1], 1.0))
        links.append(VertexLink([i % (parts*2), (i+1) % (parts*2),
                                 (i+3) % (parts*2), (i+2) % (parts*2)], [RGBA.pick_random_color()]))
        i += 2
    links.append(VertexLink(link_circle, [RGBA.pick_random_color()]))
    return Polygon(vertices, links, level)


def create_cube() -> Polygon:
    """
    This function creates a cube polygon for the main app

    Returns:

    A cube polygon
    """
    return Polygon([
        Vec3d(1.0, 1.0, -1.0, 1.0),
        Vec3d(-1.0, 1.0, -1.0, 1.0),
        Vec3d(-1.0, 1.0, 1.0, 1.0),
        Vec3d(1.0, 1.0, 1.0, 1.0),
        Vec3d(1.0, -1.0, 1.0, 1.0),
        Vec3d(-1.0, -1.0, 1.0, 1.0),
        Vec3d(-1.0, -1.0, -1.0, 1.0),
        Vec3d(1.0, -1.0, -1.0, 1.0)
    ],
        [
        VertexLink([2, 1, 6, 5], [RGBA.pick_random_color()]),
        VertexLink([3, 2, 5, 4], [RGBA.pick_random_color()]),
    ]
    )


def create_sub_level_cubes(level: int, parent: Polygon, factor: float) -> list[Polygon]:

    if(parent.level != level-1):
        return None

    first_sub: Polygon = parent.create_hard_copy(level, [
        VertexLink([2, 1, 6, 5], [RGBA.pick_random_color()]),
        VertexLink([3, 2, 5, 4], [RGBA.pick_random_color()]),
    ])
    first_sub.scale(0.5)  # scale it with 1/2

    translation: Vec3d = Vec3d(
        parent.vertices.content[20], parent.vertices.content[21], parent.vertices.content[22], 1.0).subtract(
            Vec3d(first_sub.vertices.content[20], first_sub.vertices.content[21], first_sub.vertices.content[22], 1.0))

    # move it to the start of the left down cube location
    first_sub.translate(translation.x, translation.y, translation.z)

    # and prepare its translation matrices
    sub_vectors: list[Vec3d] = [
        Vec3d(factor, 0.0, 0.0, 1.0),
        Vec3d(0.0, factor, 0.0, 1.0),
        Vec3d(0.0, 0.0, factor, 1.0),
        Vec3d(factor, factor, 0.0, 1.0),
        Vec3d(factor, 0.0, factor, 1.0),
        Vec3d(0.0, factor, factor, 1.0),
        Vec3d(factor, factor, factor, 1.0)
    ]

    result_list = [first_sub]

    for sub_vector in sub_vectors:
        temp: Polygon = first_sub.create_hard_copy(level, [
            VertexLink([2, 1, 6, 5], [RGBA.pick_random_color()]),
            VertexLink([3, 2, 5, 4], [RGBA.pick_random_color()]),
        ])
        temp.translate(sub_vector.x, sub_vector.y, sub_vector.z)
        result_list.append(temp)

    return result_list


def create_sub_level_polygons(level: int, parent: Polygon, factor: float) -> list[Polygon]:

    if(parent.level != level-1):
        return None

    first_sub: Polygon = parent.create_hard_copy(level, parent.vertex_links)
    first_sub.scale(0.5)  # scale it with 1/2

    translation: Vec3d = Vec3d(
        parent.vertices.content[20], parent.vertices.content[21], parent.vertices.content[22], 1.0).subtract(
            Vec3d(first_sub.vertices.content[20], first_sub.vertices.content[21], first_sub.vertices.content[22], 1.0))

    # move it to the start of the left down cube location
    first_sub.translate(translation.x, translation.y, translation.z)

    # and prepare its translation matrices
    sub_vectors: list[Vec3d] = [
        Vec3d(factor, 0.0, 0.0, 1.0),
        Vec3d(0.0, factor, 0.0, 1.0),
        Vec3d(0.0, 0.0, factor, 1.0),
        Vec3d(factor, factor, 0.0, 1.0),
        Vec3d(factor, 0.0, factor, 1.0),
        Vec3d(0.0, factor, factor, 1.0),
        Vec3d(factor, factor, factor, 1.0)
    ]

    result_list = [first_sub]

    for sub_vector in sub_vectors:
        temp: Polygon = first_sub.create_hard_copy(level, parent.vertex_links)
        temp.translate(sub_vector.x, sub_vector.y, sub_vector.z)
        result_list.append(temp)

    return result_list

def parametric_equation(x, y, r) -> Vec3d:
    """
    Sphere parametric equation
    """
    return Vec3d(r*numpy.cos(x)*numpy.sin(y), r*numpy.cos(y), r*numpy.sin(x)*numpy.sin(y), 1.0)


def create_sphere(level: int, factor: int, radius: float) -> Polygon:
    start_degree_x = 0  # start of x plane degree to 2pi
    start_degree_y = 0  # start of y plane degree to pi
    end_degree_x = numpy.pi*2
    end_degree_y = numpy.pi
    part_x = (end_degree_x-start_degree_x) / \
        factor  # how many parts there will be
    part_y = (end_degree_y-start_degree_y)/factor

    vertices: list[Vec3d] = []
    links: list[VertexLink] = []

    for i in range(factor):  # part for the x plane triangles
        for j in range(factor):  # part for the y plane triangles
            x = i*part_x+start_degree_x
            y = j*part_y+start_degree_y
            x_degree = end_degree_x if (
                i+1 == factor) else (i+1)*part_x+start_degree_x
            y_degree = end_degree_y if (
                j+1 == factor) else (j+1)*part_y+start_degree_y
            color = RGBA.pick_random_color()
            vertices.extend([parametric_equation(x, y, radius), parametric_equation(x, y_degree, radius),
                             parametric_equation(x_degree, y, radius), parametric_equation(x_degree, y_degree, radius)])
            len_vert = len(vertices) - 1  # create links of the triangles
            links.extend([VertexLink([len_vert-3, len_vert-1, len_vert-2], [color]),
                          VertexLink([len_vert, len_vert-2, len_vert-1], [color])])

    return Polygon(vertices, links, level)
