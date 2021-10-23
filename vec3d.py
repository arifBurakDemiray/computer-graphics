# CENG 487 Assignment1 by
# Arif Burak Demiray
# StudentId: 250201022
# October 2021

import numpy as np

class vec3d:
    x = 0
    y = 0
    z = 0
    w = 0

    def __init__(self,x,y,z,w) -> 'vec3d':
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def calc_multi(self) -> float:
        return self.x*self.y*self.z*self.w

    def calc_dot(self,vector: 'vec3d') -> float:
        return (self.x*vector.x) + (self.y*vector.y) + (self.z*vector.z)

    def calc_angle_between(self,vector: 'vec3d') -> float:
        
        value = self.__check_value(self.calc_dot(vector)/(self.calc_length()*vector.calc_length()))

        return np.arccos(value)*(180/np.pi)

    def calc_length(self):
        return np.sqrt(self.calc_dot(self))

    def add(self,vector: 'vec3d') -> 'vec3d':
        return vec3d(self.x+vector.x,self.y+vector.y+self.z+vector.z,self.__check_homo_index(vector))

    def multiply(self,constant: float) -> 'vec3d':
        return vec3d(self.x*constant,self.y*constant,self.z*constant,self.w)

    def subtract(self,vector: 'vec3d') -> 'vec3d':
        return vec3d(self.x-vector.x,self.y-vector.y,self.z-vector.z,self.__check_homo_index(vector))

    def calc_cross(self,vector: 'vec3d') -> 'vec3d':
        return vec3d(
            self.y*vector.z - self.z*vector.y,
            self.z*vector.x - self.x*vector.z,
            self.x*vector.y - self.y*vector.x,
            self.__check_homo_index(vector)   
        )

    def calc_projection(self, vector: 'vec3d') -> 'vec3d':

        degree = self.calc_angle_between(vector)

        constant = (self.calc_length()/vector.calc_length())*np.cos(np.deg2rad(degree))

        return vector.multiply(constant)

    def calc_triple_cross(self,vector1: 'vec3d',vector2: 'vec3d') -> 'vec3d':
        return vector1.multiply(self.calc_dot(vector2)).subtract(vector2.multiply(self.calc_dot(vector1)))

    def calc_triple_scalar(self,vector1: 'vec3d',vector2: 'vec3d') -> float:
        return self.calc_dot(vector1.calc_cross(vector2))

    def __check_homo_index(self,vector: 'vec3d') -> int:
        return 1 if (self.w==1 & vector.w==1) else 0

    def __check_value(self,val):
        if(val > 1):
            return 1
        elif(val < -1):
            return -1
        else:
            return val
