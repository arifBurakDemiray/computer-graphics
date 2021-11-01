# CENG 487 Assignment1 by
# Arif Burak Demiray
# StudentId: 250201022
# October 2021

from polygon import Polygon
from vec3d import vec3d
from vertex_color import RGBA, VertexLink


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
    
# #/2, x,y,z xy, xz, yz, xyz
# def create_sub_level_cubes_f(level: int,parent: Polygon, factor: float) -> list[Polygon]:

#     if(parent.level != level-1):
#         return None

#     for vertex in parent.vertices_to_vectors():
#         print("%s %s %s %s" % (vertex.x,vertex.y,vertex.z,vertex.w))

#     temp_pol = Polygon(parent.vertices_to_vectors(),None,None)
#     temp_pol.scale(1/2)
#     first_sub : list[vec3d] = temp_pol.vertices_to_vectors() 

#     sub_vectors : list[vec3d] = [
#         vec3d(factor,0.0,0.0,1.0),
#         vec3d(0.0,factor,0.0,1.0),
#         vec3d(0.0,0.0,factor,1.0),
#         vec3d(factor,factor,0.0,1.0),
#         vec3d(factor,0.0,factor,1.0),
#         vec3d(0.0,factor,factor,1.0),
#         vec3d(factor,factor,factor,1.0)
#     ]

#     result_list = []

#     for ver in first_sub:
#         print("%s %s %s %s" % (ver.x,ver.y,ver.z,ver.w))

#     for sub_vector in sub_vectors:
#         temp_vertex : list[vec3d] = []
#         for vertex in first_sub:
#             temp_vertex.append(vertex.add(sub_vector))
#         for ver in temp_vertex:
#             print("%s %s %s %s" % (ver.x,ver.y,ver.z,ver.w))
#         result_list.append(Polygon(temp_vertex,[
#         VertexLink([0, 1, 2, 3], [RGBA.pick_random_color()]),
#         VertexLink([2, 1, 6, 5], [RGBA.pick_random_color()]),
#         VertexLink([3, 2, 5, 4], [RGBA.pick_random_color()]),
#         VertexLink([4, 5, 6, 7], [RGBA.pick_random_color()]),
#         VertexLink([7, 6, 1, 0], [RGBA.pick_random_color()]),
#         VertexLink([0, 3, 4, 7], [RGBA.pick_random_color()])
#     ],level))

#     result_list.append(Polygon(first_sub,[
#         VertexLink([0, 1, 2, 3], [RGBA.pick_random_color()]),
#         VertexLink([2, 1, 6, 5], [RGBA.pick_random_color()]),
#         VertexLink([3, 2, 5, 4], [RGBA.pick_random_color()]),
#         VertexLink([4, 5, 6, 7], [RGBA.pick_random_color()]),
#         VertexLink([7, 6, 1, 0], [RGBA.pick_random_color()]),
#         VertexLink([0, 3, 4, 7], [RGBA.pick_random_color()])
#     ],level))

#     return result_list
    