# CENG 487 Assignment4 by
# Arif Burak Demiray
# December 2021

from lib.view import Camera
from .vec3d import Vec3d
from .mat3d import Mat3d
from .polygon_helper import vectors_to_matrices
from .vertex_color import RGBA, VertexLink


class Polygon:
    """
    This class holds informations about a 3d polygon

    its vertices, links and transformation matrix stack
    """
    vertices: Mat3d
    matrix_stack: 'list[Mat3d]'
    vertex_links: 'list[VertexLink]'
    level: int
    edge_adjaceny: 'list[Edge]' = []
    face_adjaceny: 'list[Edge]' = []
    vertex_adjaceny: 'list[Edge]' = []
    # tried to do winged edge structure

    def __init__(self, vertices: 'list[Vec3d]', vertex_links: 'list[VertexLink]', level: int = 0) -> None:
        if(vertices != None):
            self.vertices = vectors_to_matrices(vertices)
        self.matrix_stack = []
        self.vertex_links = vertex_links
        self.level = level

    def get(self, index: int = 0) -> 'list[float]':
        multiplied = index*4
        return [self.vertices.content[multiplied], self.vertices.content[multiplied+1],
                self.vertices.content[multiplied+2], self.vertices.content[multiplied+3]]

    def transformate(self, matrix: Mat3d) -> None:
        """
        This function transformates caller polygon by given matrix and saves matrix to matrix stack

        Parameters:

        Transformation matrix
        """
        self.matrix_stack.append(matrix)
        self.vertices = self.vertices.calc_multiplacation(matrix)

    def with_edges(self, edges: 'list[Edge]') -> 'Polygon':
        self.edge_adjaceny = edges
        return self

    def with_vertices(self, vertices: 'list[Edge]') -> 'Polygon':
        self.vertex_adjaceny = vertices
        return self

    def with_faces(self, faces: 'list[Edge]') -> 'Polygon':
        self.face_adjaceny = faces
        return self

    def translate(self, x: float, y: float, z: float) -> None:
        """
        This function translates polygon object by given coordinates

        Parameters:

        X,Y and Z coordinate of the translation point
        """
        vector = Vec3d(x, y, z, 1.0)
        result = self.vertices.calc_translation(vector)

        self.vertices = result.transformed
        # self.matrix_stack.append(result.transformer)

    def set_vertices(self, vertices: Mat3d) -> 'Polygon':
        self.vertices = vertices
        return self

    def plane_translate(self, inverse: int, vector: Vec3d) -> None:
        """
        This function translates caller polygon by given vector
        but does not saves translation matrix to matrix stack

        Parameters:

        Translation matrix and inverse parameter that 
            if it is 0 it translates it by given points unreversed
            otherwise translates it by reversed version of the vector
        """

        temp_vector: Vec3d

        if(inverse == 0):
            temp_vector = vector
        else:
            temp_vector = vector.multiply(-1)

        result = self.vertices.calc_translation(temp_vector)
        self.vertices = result.transformed

    def __shear(self, xy: float, yx: float, xz: float, zx: float, yz: float, zy: float) -> None:
        """
        This function is under construction for now so it is private
        It shears x,y,z in a row 

        Parameters:

        X,Y and Z directions of shear values

        """
        matrix = self.vertices.create_shear_matrix(xy, yx, xz, zx, yz, zy)

        self.vertices = self.vertices.calc_multiplacation(matrix)

        self.matrix_stack.append(matrix)

    def scale(self, constant: float) -> None:
        """
        This function scales caller polygon object

        Parameters:

        Scale constant
        """
        result = self.vertices.calc_scale(constant)
        self.vertices = result.transformed
        # self.matrix_stack.append(result.transformer)

    def project(self, camera: Camera) -> None:
        """
        This function scales caller polygon object

        Parameters:

        Scale constant
        """

        result = self.vertices.calc_multiplacation(camera.matrix)
        self.vertices = result

    def change_colors(self) -> 'Polygon':
        for link in self.vertex_links:
            for i in range(len(link.colors)):
                link.colors[i] = RGBA.pick_random_color()

        return self

    def create_hard_copy(self, level: int, links: 'list[VertexLink]' = None) -> 'Polygon':

        link_vertex = links if links != None else self.vertex_links

        return Polygon(None, link_vertex, level).set_vertices(self.vertices)

    def rotate(self, degree: float) -> None:
        """
        This function rotates polygon object by given degree

        Parameters:

        Degree to rotate
        """
        vector = self.vertices_to_vectors()[0]  # get first vertex
        matrix = self.vertices.create_translation_matrix(
            vector.multiply(-1.0))  # move to origin
        inv_matrix = matrix.calc_inverse()

        rot_matrix = self.vertices.create_rotation_matrix(
            degree)  # X,Y,Z in a row

        matrix = matrix.calc_multiplacation(
            rot_matrix).calc_multiplacation(inv_matrix)
        # rotate than go back to original coordinate by inverse matrix of translation

        result = self.vertices.calc_multiplacation(
            matrix)  # than multiply with vertices

        self.vertices = result
        self.matrix_stack.append(matrix)

    def rotate_y(self, degree: float) -> None:
        """
        This function rotates polygon object by given degree

        Parameters:

        Degree to rotate
        """
        result = self.vertices.calc_rotation_y(degree)

        self.vertices = result.transformed
        self.matrix_stack.append(result.transformer)

    def rotate_z(self, degree: float) -> None:
        """
        This function rotates polygon object by given degree

        Parameters:

        Degree to rotate
        """
        result = self.vertices.calc_rotation_z(degree)

        self.vertices = result.transformed
        self.matrix_stack.append(result.transformer)

    def rotate_x(self, degree: float) -> None:
        """
        This function rotates polygon object by given degree

        Parameters:

        Degree to rotate
        """
        result = self.vertices.calc_rotation_x(degree)

        self.vertices = result.transformed
        self.matrix_stack.append(result.transformer)

    def undo(self) -> None:
        """
        This function undoes the last transformation done to the caller polygon
        """
        if(len(self.matrix_stack) < 1):
            return
        last_matrix = self.matrix_stack[len(self.matrix_stack) - 1]
        self.matrix_stack.remove(last_matrix)
        self.vertices = self.vertices.calc_multiplacation(
            last_matrix.calc_inverse())

    def vertices_to_vectors(self) -> 'list[Vec3d]':
        """
        This function converts mat3d object of vertices to list vec3d

        Returns:

        List of vertices in terms of vec3d instances
        """
        result = []

        for i in range(int(len(self.vertices.content)/4) - 1):  # do not get last row
            result.append(
                Vec3d(
                    self.vertices.content[i*4],
                    self.vertices.content[i*4+1],
                    self.vertices.content[i*4+2],
                    self.vertices.content[i*4+3])
            )

        return result


class Edge:
    vertices: 'list[int]'
    faces: 'list[VertexLink]'
    edges: 'list[Edge]'
    edge_point: 'Vec3d' = Vec3d(0, 0, 0, 1)
    level: int = 0

    def __init__(self, vertices: 'list[int]', faces: 'list[VertexLink]', edges: 'list[Edge]', level: int = 0) -> None:
        self.vertices = vertices
        self.faces = faces
        self.edges = edges
        self.level = level

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.vertices[0] == other.vertices[0] and
                    self.vertices[1] == other.vertices[1]) or (self.vertices[1] == other.vertices[0] and
                                                               self.vertices[0] == other.vertices[1])
        else:
            return False

    def is_neighbour(self, edge: 'Edge') -> bool:
        return self.vertices[0] in edge.vertices or self.vertices[1] in edge.vertices and self.level == edge.level
