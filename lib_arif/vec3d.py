# CENG 487 Assignment2 by
# Arif Burak Demiray
# StudentId: 250201022
# November 2021

import numpy as np
from .helper import degree_to_radian, radian_to_degree


class vec3d:
    """
    A vector class implemented for 3d
    """
    x: float
    y: float
    z: float
    w: float

    def __init__(self, x: float, y: float, z: float, w: float) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def calc_multi(self) -> float:
        """
        Calculates multiplacation of the values of the vector

        Returns:

        Float value of the vector values
        """
        return self.x*self.y*self.z*self.w

    def calc_dot(self, vector: 'vec3d') -> float:
        """
        Calculates dot product of 2 3d vectors by formula
        A = [a,b,c]  B = [x,y,z] 

        A.B = a.x + b.y + c.z

        Parameters:

        A vec3d object

        Returns:

        Dot product of two vectors 

        """
        return (self.x*vector.x) + (self.y*vector.y) + (self.z*vector.z)

    def calc_angle_between(self, vector: 'vec3d') -> float:
        """
        Calculates angle between two vectors by formula
        A = [a,b,c]  B = [x,y,z] 

        A.B = |A|.|B|.cosx \n
        a.x + b.y + c.z = |A|.|B|.cosx \n
        cosx = (a.x + b.y + c.z) / |A|.|B| \n
        arccos((a.x + b.y + c.z) / |A|.|B|) = x \n

        Parameters:

        A vec3d object

        Returns:

        Angle between vectors in terms of degree


        """

        value = self.__check_value(self.calc_dot(
            vector)/(self.calc_length()*vector.calc_length()))

        return radian_to_degree(np.arccos(value))

    def calc_length(self) -> float:
        """
        Calculates lenght of a 3d vector by dot product of itself

        Returns:

        Length of the 3d vector in terms of float
        """
        return np.sqrt(self.calc_dot(self))

    def add(self, vector: 'vec3d') -> 'vec3d':
        """
        Adds to vectors and returns a new vector

        Parameters:

        A vec3d object

        Returns:

        New vec3d object vector is added to the caller object
        """
        return vec3d(self.x+vector.x, self.y+vector.y,self.z+vector.z, self.__check_homo_index(vector))

    def multiply(self, constant: float) -> 'vec3d':
        """
        Multiplies all values of a vector by a given constant

        Parameters:

        Multiplier constant

        Returns:

        A new vec3d object multiplied by the constant
        """
        return vec3d(self.x*constant, self.y*constant, self.z*constant, self.w)

    def subtract(self, vector: 'vec3d') -> 'vec3d':
        """
        Subtracts two vectors. vector parameter is subtracted from caller object

        Parameters:

        A vec3d object

        Returns:

        A new vec3d object
        """
        return vec3d(self.x-vector.x, self.y-vector.y, self.z-vector.z, self.__check_homo_index(vector))

    def calc_cross(self, vector: 'vec3d') -> 'vec3d':
        """
        Calculate cross product of two vectors by formula 

        |a1|___|b1|_____|a2*b3_-_a3*b2| \n
        |a2|_X_|b2|__=__|a3*b1_-_a1*b3| \n
        |a3|___|b3|_____|a1*b2_-_a2*b1| \n

        Parameters:

        A vec3d object

        Returns:

        A new vec3d object
        """
        return vec3d(
            self.y*vector.z - self.z*vector.y,
            self.z*vector.x - self.x*vector.z,
            self.x*vector.y - self.y*vector.x,
            self.__check_homo_index(vector)
        )

    def calc_projection(self, vector: 'vec3d') -> 'vec3d':
        """
        Calculates projection vector of vector onto caller vector by the formula

        projb(a) = |a|*cosx*b/|b|

        where x is angle between a and b
        |b| is length of vector b

        Parameters:

        A vec3d object

        Returns:

        A new vec3d object
        """
        degree = self.calc_angle_between(vector)

        constant = (self.calc_length()/vector.calc_length()) * \
            np.cos(degree_to_radian(degree))

        return vector.multiply(constant)

    def calc_triple_cross(self, vector1: 'vec3d', vector2: 'vec3d') -> 'vec3d':
        """
        Calculates triple cross product of 3 vectors by the formula

        let A,B and C a 3d vector

        A x B x C = (A.C)*B - (A.B)*C

        Parameters:

        Two vec3d objects

        Returns:

        A new vec3d object

        """
        return vector1.multiply(self.calc_dot(vector2)).subtract(vector2.multiply(self.calc_dot(vector1)))

    def calc_triple_scalar(self, vector1: 'vec3d', vector2: 'vec3d') -> float:
        """
        Calculates triple scalar product of 3 vectors by the formula

        let A,B and C a 3d vector

        A.B.C = A.(B x C)

        it can be other combinations

        Parameters:

        Two vec3d object

        Returs:

        Float result of the triple scalar product
        """
        return self.calc_dot(vector1.calc_cross(vector2))

    def calc_normalize(self) -> 'vec3d':
        """
        This function calculates normalized vector of caller vector

        Returns:

        Normalized version of the caller vector
        """
        return self.multiply(1/self.calc_length())

    def __check_homo_index(self, vector: 'vec3d') -> float:
        """
        Checks whether they have same homogenous value or not

        Parameters:

        A vec3d object

        Returns:

        1 if they have 1 as homogenous value otherwise 0

        """

        if self.w == 1.0 and vector.w == 1.0:
            return 1
        else:
            return 0

    def __check_value(self, val):
        """
        Checks value of a trigonometric function that it cannot be greater than 1 or less than -1

        Parameters:

        A trigonometric function result

        Returns: 

        If result is greater than 1 clips it to the 1
        If result is less than -1 clips it to the -1
        Otherwise returns the value directly
        """
        if(val > 1):
            return 1
        elif(val < -1):
            return -1
        else:
            return val
