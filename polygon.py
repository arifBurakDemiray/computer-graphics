# CENG 487 Assignment1 by
# Arif Burak Demiray
# StudentId: 250201022
# October 2021

from vec3d import vec3d
from mat3d import mat3d
from polygon_helper import vectors_to_matrices
from vertex_color import RGBA, VertexLink


class Polygon:
    """
    This class holds informations about a 3d polygon

    its vertices, links and transformation matrix stack
    """
    vertices: mat3d
    matrix_stack: list[mat3d]
    vertex_links: list[VertexLink]
    level: int

    def __init__(self, vertices: list[vec3d], vertex_links: list[VertexLink], level: int = 0) -> None:
        #TODO make type checker

        if(vertices != None):
            self.vertices = vectors_to_matrices(vertices)
        self.matrix_stack = []
        self.vertex_links = vertex_links
        self.level = level

    def transformate(self, matrix: mat3d) -> None:
        """
        This function transformates caller polygon by given matrix and saves matrix to matrix stack

        Parameters:

        Transformation matrix
        """
        self.matrix_stack.append(matrix)
        self.vertices = self.vertices.calc_multiplacation(matrix)

    def translate(self, x: float, y: float, z: float) -> None:
        """
        This function translates polygon object by given coordinates

        Parameters:

        X,Y and Z coordinate of the translation point
        """
        vector = vec3d(x, y, z, 1.0)
        result = self.vertices.calc_translation(vector)

        self.vertices = result.transformed
        #self.matrix_stack.append(result.transformer)

    def set_vertices(self,vertices: mat3d) -> 'Polygon':
        self.vertices = vertices
        return self

    def plane_translate(self, inverse: int, vector: vec3d) -> None:
        """
        This function translates caller polygon by given vector
        but does not saves translation matrix to matrix stack

        Parameters:

        Translation matrix and inverse parameter that 
            if it is 0 it translates it by given points unreversed
            otherwise translates it by reversed version of the vector
        """

        temp_vector: vec3d

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
        #self.matrix_stack.append(result.transformer)

    def scale_and_return(self,constant: float) -> list[vec3d]:
        resultt = self.vertices.calc_scale(constant)
        result = []

        for i in range(int(len(resultt.transformed.content)/4) - 1):  # do not get last row
            result.append(
                vec3d(
                    resultt.transformed.content[i*4],
                    resultt.transformed.content[i*4+1],
                    resultt.transformed.content[i*4+2],
                    resultt.transformed.content[i*4+3])
            )

        return result

    def change_colors(self) -> 'Polygon':
        for link in self.vertex_links:
            for i in range(len(link.colors)):
                link.colors[i]=RGBA.pick_random_color()
        
        return self

    def create_hard_copy(self,level: int, links: list[VertexLink] = None) -> 'Polygon':
        
        link_vertex = links if links != None else self.vertex_links

        return Polygon(self.vertices_to_vectors(),link_vertex,level)
        

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

    def vertices_to_vectors(self) -> list[vec3d]:
        """
        This function converts mat3d object of vertices to list vec3d

        Returns:

        List of vertices in terms of vec3d instances
        """
        result = []

        for i in range(int(len(self.vertices.content)/4) - 1):  # do not get last row
            result.append(
                vec3d(
                    self.vertices.content[i*4],
                    self.vertices.content[i*4+1],
                    self.vertices.content[i*4+2],
                    self.vertices.content[i*4+3])
            )

        return result
