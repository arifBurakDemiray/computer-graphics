# CENG 487 Assignment2 by
# Arif Burak Demiray
# StudentId: 250201022
# November 2021

from .vec3d import vec3d
from .mat3d import mat3d


def vectors_to_matrices(vectors: list[vec3d]) -> mat3d:
    """
    This function converts list of vertices to mat3d instance

    Parameters:

    List of vec3d objects

    Returns:

    Mat3d instance
    """
    content = []

    vectors_len = len(vectors)

    for i in range(vectors_len):

        temp = vectors[i]

        content.extend([temp.x, temp.y, temp.z, temp.w])

    content.extend([0, 0, 0, 1])  # for the homogeneous coordinates

    return mat3d(content)
