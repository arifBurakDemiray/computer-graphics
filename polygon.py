# CENG 487 Assignment1 by
# Arif Burak Demiray
# StudentId: 250201022
# October 2021

from vec3d import vec3d
from mat3d import mat3d
from polygon_helper import vectors_to_matrices
from vertex_color import VertexLink


class Polygon:
    """
    This class holds informations about a 3d polygon

    its vertices, links and transformation matrix stack
    """
    vertices : mat3d
    matrix_stack : list[mat3d]
    vertex_links : list[VertexLink]

    def __init__(self,vertices: list[vec3d], vertex_links : list[VertexLink]) -> None:
        self.vertices = vectors_to_matrices(vertices)
        self.matrix_stack = []
        self.vertex_links = vertex_links

    def transformate(self, matrix: mat3d) -> None:
        """
        """
        self.matrix_stack.append(matrix)
        self.vertices = self.vertices.calc_multiplacation(matrix)
    
    def translate(self, x: float, y: float, z: float) -> None:
        vector = vec3d(x,y,z,1.0)
        result = self.vertices.calc_translation(vector)

        self.vertices = result.transformed
        self.matrix_stack.append(result.transformer)

    def plane_translate(self, inverse: int, vector: vec3d) -> None:
        if(inverse == 0):
            self.translate_unregistered(vector)
        else:
            self.translate_unregistered(vector.multiply(-1.0))
    #TODO take care of shear
    def shear(self) -> None:
        matrix = self.vertices.create_shear_matrix(1,-1,8,-8,3,-3)

        self.vertices = self.vertices.calc_multiplacation(matrix)

        self.matrix_stack.append(matrix)

    def scale(self, constant: float) -> None:
        result = self.vertices.calc_scale(constant)
        self.vertices = result.transformed
        self.matrix_stack.append(result.transformer)

    def translate_unregistered(self, vector: vec3d) -> None:
        result = self.vertices.calc_translation(vector)

        self.vertices = result.transformed

    def rotate(self,degree: float) -> None:
        vector = self.vertices_to_vectors()[0]
        #move to origin
        matrix = self.vertices.create_translation_matrix(vector.multiply(-1.0))
        inv_matrix = matrix.calc_inverse() #turn back to its place

        rot_matrix = self.vertices.create_rotation_matrix(degree)
            
        bir = matrix.calc_multiplacation(rot_matrix).calc_multiplacation(inv_matrix)

        result = self.vertices.calc_multiplacation(bir)

        self.vertices = result
        self.matrix_stack.append(bir)

    def undo(self) -> None:
        if(len(self.matrix_stack) < 1):
            return
        last_matrix = self.matrix_stack[len(self.matrix_stack) - 1]
        self.matrix_stack.remove(last_matrix)
        self.vertices = self.vertices.calc_multiplacation(last_matrix.calc_inverse())
        

    def vertices_to_vectors(self) -> list[vec3d]:
        
        result = []

        for i in range(int(len(self.vertices.content)/4) - 1):
            result.append(
                vec3d(
                    self.vertices.content[i*4],
                    self.vertices.content[i*4+1],
                    self.vertices.content[i*4+2],
                    self.vertices.content[i*4+3])
            )

        return result