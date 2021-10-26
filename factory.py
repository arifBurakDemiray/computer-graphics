# CENG 487 Assignment1 by
# Arif Burak Demiray
# StudentId: 250201022
# October 2021

from polygon import Polygon
from vec3d import vec3d
from vertex_color import RGBA, VertexRope


def create_triangle() -> Polygon:
    return Polygon([
                        vec3d(0.0,1.0,0.0,1.0),
                        vec3d(-1.0,-1.0,1.0,1.0),
                        vec3d(1.0,-1.0,1.0,1.0),
                        vec3d(1.0,-1.0,-1.0,1.0),
                        vec3d(-1.0,-1.0,-1.0,1.0)
                    ],
                    [
                        VertexRope([0,1,2],[RGBA(1,0,0),RGBA(0,1,0),RGBA(0,0,1)]),
                        VertexRope([0,2,3],[RGBA(1,0,0),RGBA(0,0,1),RGBA(0,1,0)]),
                        VertexRope([0,3,4],[RGBA(1,0,0),RGBA(0,1,0),RGBA(0,0,1)]),
                        VertexRope([0,4,1],[RGBA(1,0,0),RGBA(0,0,1),RGBA(0,1,0)])
                    ])

def create_cube() -> Polygon:
    return Polygon([
                    vec3d(1.0, 1.0,-1.0,1.0),
                    vec3d(-1.0, 1.0,-1.0,1.0),
                    vec3d(-1.0, 1.0, 1.0,1.0),
                    vec3d(1.0, 1.0, 1.0,1.0),
                    vec3d(1.0,-1.0, 1.0,1.0),
                    vec3d(-1.0,-1.0, 1.0,1.0),
                    vec3d(-1.0,-1.0,-1.0,1.0),
                    vec3d(1.0,-1.0,-1.0,1.0)
                ],
                [
                    VertexRope([0,1,2,3],[RGBA(0,1,0)]),
                    VertexRope([2,1,6,5],[RGBA(1.0,0.5,0.0)]),
                    VertexRope([3,2,5,4],[RGBA(1,0,0)]),
                    VertexRope([4,5,6,7],[RGBA(1,1,0)]),
                    VertexRope([7,6,1,0],[RGBA(0,0,1)]),
                    VertexRope([0,3,4,7],[RGBA(1,0,1)])
                ]
                )