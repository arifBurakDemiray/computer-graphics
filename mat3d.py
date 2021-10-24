# CENG 487 Assignment1 by
# Arif Burak Demiray
# StudentId: 250201022
# October 2021

from vec3d import vec3d 
import numpy as np
from helper import degree_to_radian,radian_to_degree

class mat3d:
    """
    This class holds a 4x4 matrix

    Please give matrix as an array because of memory access

    [4][1] in matrix
    width(row)*4 + 1 in array implementation

    so in the matrix [x,y] is equal to width(row)*y + x in the array
    """
    content = []

    def __init__(self,content: list[int]) -> 'mat3d':
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

    def calc_multiplacation(self,matrix: 'mat3d') -> 'mat3d':
        """
        Calculates multiplacation of two 4x4 matrices, 
        it start multiplacation with parameter mat3d attribute

        Parameters:

        A mat3d object

        Returns:

        A new mat3d object that multiplied with caller mat3d object

        """
        value = []

        for z in range(int(len(matrix.content)/4)):
            for i in range(4):
                total = 0
                for y in range(4):
                    total += matrix.content[z*4+y]*self.content[y*4 + i]
                value.append(total)

        return mat3d(value)
    
    def calc_scale(self, constant: float) -> 'mat3d':
        """
        This function calculates scaled version of caller mat3d object by given constant

        Parameters:
        
        Constant value for scaling

        Returns:

        Scaled new mat3d object of scaled caller mat3d object
        """
        return self.calc_multiplacation(self.__create_scale_matrix(constant))

    def calc_translation(self, vector: vec3d) -> 'mat3d':
        """
        This function calculates translation of mat3d matrix by given vec3d vector

        Parameters:

        A vector instance that's type is vec3d

        Returns:

        new mat3d object that is translated by given vector
        """
        return self.calc_multiplacation(self.__create_translation_matrix(vector))

    
    def calc_rotation_x(self, degree: float) -> 'mat3d':
        """
        This function calculates rotated by x axis of given caller mat3d matrix

        Parameters:

        Degree of rotation

        Returns:

        Rotated matrix by x axis
        """
        return self.calc_multiplacation(self.__create_rotation_matrix_x(degree))

    def calc_rotation_y(self, degree: float) -> 'mat3d':
        """
        This function calculates rotated by y axis of given caller mat3d matrix

        Parameters:

        Degree of rotation

        Returns:

        Rotated matrix by y axis
        """
        return self.calc_multiplacation(self.__create_rotation_matrix_y(degree))

    def calc_rotation_z(self, degree: float) -> 'mat3d':
        """
        This function calculates rotated by z axis of given caller mat3d matrix

        Parameters:

        Degree of rotation

        Returns:

        Rotated matrix by z axis
        """
        return self.calc_multiplacation(self.__create_rotation_matrix_z(degree))

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
            np.cos(rad),-np.sin(rad),0,0,
            np.sin(rad),np.cos(rad),0,0,
            0,0,1,0,
            0,0,0,1
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
            np.cos(rad),0,np.sin(rad),0,
            0,1,0,0,
            -np.sin(rad),0,np.cos(rad),0,
            0,0,0,1
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
            1,0,0,0,
            0,np.cos(rad),-np.sin(rad),0,
            0,np.sin(rad),np.cos(rad),0,
            0,0,0,1
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
            1,0,0,vector.x,
            0,1,0,vector.y,
            0,0,1,vector.z,
            0,0,0,1
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
            [constant,0,0,0,
            0,constant,0,0,
            0,0,constant,0,
            0,0,0,1])
