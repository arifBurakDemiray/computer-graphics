# CENG 487 Assignment2 by
# Arif Burak Demiray
# StudentId: 250201022
# November 2021

from .vec3d import vec3d
import numpy as np
from .helper import degree_to_radian


class Pair:
    """
    This class is for response object from transformation functions
    It holds both result of transformation and transformation matrix
    """
    transformer: 'mat3d'
    transformed: 'mat3d'

    def __init__(self, transformer: 'mat3d', transformed: 'mat3d') -> 'Pair':
        self.transformer = transformer
        self.transformed = transformed


class mat3d:
    """
    This class holds a 4x4 matrix

    Please give matrix as an array because of memory access

    [4][1] in matrix
    width(row)*4 + 1 in array implementation

    so in the matrix [x,y] is equal to width(row)*y + x in the array
    """
    content: list[float]

    def __init__(self, content: list[float]) -> 'mat3d':
        self.content = content

    def calc_transpose(self) -> 'mat3d':
        """
        This function calculates transpose of the caller mat3d object

        Returns:

        Transposed version of new mat3d object
        """

        value = []

        for i in range(4):
            for y in range(4):
                value.append(self.content[y*4 + i])

        return mat3d(value)

    def calc_inverse(self) -> 'mat3d':
        """
        This function calculates inverse of a matrix that has 4 column

        Returns:

        Inverse of the caller mat3d object
        """
        dimensional = []
        for i in range(int(len(self.content)/4)):
            dimensional.append([
                self.content[i*4],
                self.content[i*4 + 1],
                self.content[i*4 + 2],
                self.content[i*4 + 3]])
        inversed = np.linalg.inv(dimensional)
        return mat3d(inversed.flatten())

    def calc_multiplacation(self, matrix: 'mat3d') -> 'mat3d':
        """
        Calculates multiplacation of two matrices that have 4 columns second matrix should be 4x4 
        it start multiplacation with caller mat3d

        Parameters:

        A mat3d object

        Returns:

        A new mat3d object that multiplied with caller mat3d object

        """
        value = []

        for z in range(int(len(self.content)/4)):
            for i in range(4):
                total = 0
                for y in range(4):
                    total += self.content[z*4+y]*matrix.content[y*4 + i]
                value.append(total)

        return mat3d(value)

    def calc_scale(self, constant: float) -> Pair:
        """
        This function calculates scaled version of caller mat3d object by given constant

        Parameters:

        Constant value for scaling

        Returns:

        Scaled new mat3d object of scaled caller mat3d object and scale matrix
        """

        matrix = self.create_scale_matrix(constant)

        return Pair(matrix, self.calc_multiplacation(matrix))

    def calc_translation(self, vector: vec3d) -> Pair:
        """
        This function calculates translation of mat3d matrix by given vec3d vector

        Parameters:

        A vector instance that's type is vec3d

        Returns:

        new mat3d object that is translated by given vector and translation matrix
        """

        matrix = self.create_translation_matrix(vector)

        return Pair(matrix, self.calc_multiplacation(matrix))

    def calc_rotation_x(self, degree: float) -> Pair:
        """
        This function calculates rotated by x axis of given caller mat3d matrix

        Parameters:

        Degree of rotation

        Returns:

        Rotated matrix by x axis and x rotation matrix
        """

        matris_x = self.create_rotation_matrix_x(degree)

        return Pair(matris_x, self.calc_multiplacation(matris_x))

    def calc_rotation_y(self, degree: float) -> Pair:
        """
        This function calculates rotated by y axis of given caller mat3d matrix

        Parameters:

        Degree of rotation

        Returns:

        Rotated matrix by y axis and y rotation matrix
        """

        matris_y = self.create_rotation_matrix_y(degree)

        return Pair(matris_y, self.calc_multiplacation(matris_y))

    def calc_rotation_z(self, degree: float) -> Pair:
        """
        This function calculates rotated by z axis of given caller mat3d matrix

        Parameters:

        Degree of rotation

        Returns:

        Rotated matrix by z axis and z rotation matrix
        """

        matris_z = self.create_rotation_matrix_z(degree)

        return Pair(matris_z, self.calc_multiplacation(matris_z))

    def calc_rotation(self, degree: float) -> Pair:
        """
        This function rotates caller mat3d in order of X,Y and Z directions

        Parameters:

        Degree of the rotation

        Returns:

        Rotated version of the caller mat3d and rotation matrix
        """
        matrix = self.create_rotation_matrix(degree)

        return Pair(matrix, self.calc_multiplacation(matrix))

    def create_rotation_matrix(self, degree: float) -> 'mat3d':
        """
        This function creates rotation matrix in order of X,Y and Z

        Parameters:

        Degree of the rotation

        Returns:

        Rotation matrix
        """
        matris_xyz = self.create_rotation_matrix_x(degree).calc_multiplacation(
            self.create_rotation_matrix_y(degree)
        ).calc_multiplacation(self.create_rotation_matrix_z(degree))

        return matris_xyz

    def create_rotation_matrix_z(self, degree: float) -> 'mat3d':
        """
        This function creates rotation matrix for z axis

        Parameters:

        Degree of rotation

        Returns:

        Rotation matrix of x axis
        """
        rad = degree_to_radian(degree)

        return mat3d([
            np.cos(rad), -np.sin(rad), 0, 0,
            np.sin(rad), np.cos(rad), 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1
        ])

    def create_rotation_matrix_y(self, degree: float) -> 'mat3d':
        """
        This function creates rotation matrix for y axis

        Parameters:

        Degree of rotation

        Returns:

        Rotation matrix of y axis
        """
        rad = degree_to_radian(degree)

        return mat3d([
            np.cos(rad), 0, np.sin(rad), 0,
            0, 1, 0, 0,
            -np.sin(rad), 0, np.cos(rad), 0,
            0, 0, 0, 1
        ])

    def create_rotation_matrix_x(self, degree: float) -> 'mat3d':
        """
        This function creates rotation matrix for x axis

        Parameters:

        Degree of rotation

        Returns:

        Rotation matrix of x axis
        """
        rad = degree_to_radian(degree)

        return mat3d([
            1, 0, 0, 0,
            0, np.cos(rad), -np.sin(rad), 0,
            0, np.sin(rad), np.cos(rad), 0,
            0, 0, 0, 1
        ])

    def create_translation_matrix(self, vector: vec3d) -> 'mat3d':
        """
        This function creates translation matrix by given vec3d object

        Parameters:

        Translation vector

        Returns:

        Translation matrix
        """
        return mat3d([
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            vector.x, vector.y, vector.z, 1
        ])

    def create_shear_matrix(self, xy: float, yx: float, xz: float, zx: float, yz: float, zy: float) -> 'mat3d':
        return mat3d([
            1, yx, zx, 0,
            xy, 1, zy, 0,
            xz, yz, 1, 0,
            0, 0, 0, 1
        ])

    def create_scale_matrix(self, constant: float) -> 'mat3d':
        """
        This function creates scale matrix for given constant

        Parameters:

        Constant value for the scale matrix

        Returns:

        Scale matrix for constant value
        """
        return mat3d(
            [constant, 0, 0, 0,
             0, constant, 0, 0,
             0, 0, constant, 0,
             0, 0, 0, 1])
