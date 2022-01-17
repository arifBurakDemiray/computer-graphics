# CENG 487 Assignment4 by
# Arif Burak Demiray
# December 2021

from .vec3d import Vec3d
import numpy as np
from .helper import degree_to_radian
from .mat3d import Mat3d


class View:

    cameras: 'list[Camera]'
    selected: int
    pitch: float
    yaw: float

    def __init__(self) -> None:
        self.cameras = []
        self.selected = 0
        self.pitch = 0.0
        self.yaw = 0.0

    def subscribe(self, camera: 'Camera') -> None:
        self.cameras.append(camera)

    def mouseMoved(self, xpos, ypos) -> None:
        # https://learnopengl.com/Getting-started/Camera
        xoffset = xpos - self.cameras[self.selected].posX
        yoffset = self.cameras[self.selected].posY - ypos
        self.cameras[self.selected].posX = xpos
        self.cameras[self.selected].posY = ypos
        xoffset *= self.cameras[self.selected].sensivity
        yoffset *= self.cameras[self.selected].sensivity
        self.yaw += xoffset
        self.pitch += yoffset

        if(self.pitch > 89.0):
            self.pitch = 89.0
        elif(self.pitch < -89.0):
            self.pitch = -89.0

        camPos: Vec3d = Vec3d(
            np.cos(degree_to_radian(self.yaw))*np.cos(degree_to_radian(self.pitch)),
            np.sin(degree_to_radian(self.pitch)),
            np.sin(degree_to_radian(self.yaw))*np.cos(degree_to_radian(self.pitch)),
            1
        )

        zaxiz = camPos.calc_normalize()
        xaxis = Vec3d(0, 1, 0, 1).calc_normalize().calc_cross(zaxiz)  # camera up vector
        yaxis = zaxiz.calc_cross(xaxis)

        self.cameras[self.selected].matrix = Mat3d(
            [xaxis.x, xaxis.y, xaxis.z, 0,
             yaxis.x, yaxis.y, yaxis.z, 0,
             zaxiz.x, zaxiz.y, zaxiz.z, 0,
             -1*camPos.x, -1*camPos.y, -1*camPos.z, 1]
        )


class Camera:

    posX: int
    posY: int
    sensivity: float
    matrix: Mat3d

    def __init__(self, posX: int, posY: int, sensivity: float = 0.01) -> None:
        self.posX = posX
        self.posY = posY
        self.sensivity = sensivity
