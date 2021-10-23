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

    def dot(self,vector: 'vec3d') -> float:
        return (self.x*vector.x) + (self.y*vector.y) + (self.z*vector.z)

    def angle_between(self,vector: 'vec3d') -> int:
        
        value = self.__check_value(self.dot(vector)/(self.length()*vector.length()))

        return np.arccos(value)*(180/np.pi)

    def length(self):
        return np.sqrt(self.dot(self))

    def addition(self,vector: 'vec3d') -> 'vec3d':
        return vec3d(self.x+vector.x,self.y+vector.y+self.z+vector.z,self.__check_homo_index(vector))

    def cross(self,vector: 'vec3d') -> 'vec3d':
        return vec3d(
            self.y*vector.z - self.z*vector.y,
            self.z*vector.x - self.x*vector.z,
            self.x*vector.y - self.y*vector.x,
            self.__check_homo_index(vector)   
        )

    def projection(self, vector: 'vec3d') -> vec3d:
        return 

    def __check_homo_index(self,vector: 'vec3d')->int:
        return 1 if (self.w==1 & vector.w==1) else 0

    def __check_value(self,val):
        if(val > 1):
            return 1
        elif(val < -1):
            return -1
        else:
            return val
