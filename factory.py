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
        VertexLink([0, 1, 2, 3], [RGBA(0, 1, 0)]),
        VertexLink([2, 1, 6, 5], [RGBA(1.0, 0.5, 0.0)]),
        VertexLink([3, 2, 5, 4], [RGBA(1, 0, 0)]),
        VertexLink([4, 5, 6, 7], [RGBA(1, 1, 0)]),
        VertexLink([7, 6, 1, 0], [RGBA(0, 0, 1)]),
        VertexLink([0, 3, 4, 7], [RGBA(1, 0, 1)])
    ]
    )
