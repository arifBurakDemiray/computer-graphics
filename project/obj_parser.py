# CENG 487 Assignment6 by
# Arif Burak Demiray
# StudentId: 250201022
# December 2021


from project.defs import DrawStyle
from project.shapes import UV, _Shape, FaceProp
from project.vector import ColorRGBA, HCoord, Point3f


class Parser:

    file_name: str

    def __init__(self, file_name: str) -> None:
        self.file_name = file_name

    def parse(self) -> _Shape:
        pass


class ObjParser(Parser):
    """
    This class parses quad objects
    """

    def __init__(self, file_name: str) -> None:
        super().__init__(file_name)

    def __parse_hcoord(self, line: str) -> Point3f:
        data: 'list[str]' = line.split(" ")
        return Point3f(float(data[1]), float(data[2]), float(data[3]))

    def __parse_uv(self, line: str) -> UV:
        data: 'list[str]' = line.split(" ")
        return UV(float(data[1]), float(data[2]))

    def parse(self) -> _Shape:
        vertices: 'list[HCoord]' = []
        normals: 'list[HCoord]' = []
        faces: 'list[list[FaceProp]]' = []
        uvs: 'list[UV]' = []

        file = open(self.file_name, "r")

        for line in file:
            if(len(line) < 1):
                continue
            if(line[0] == "v" and line[1] == "t"):
                uvs.append(self.__parse_uv(line))
            elif(line[0] == "v" and line[1] == "n"):
                normals.append(self.__parse_hcoord(line))
            elif(line[0] == "v"):  # if vertex add vertices
                vertices.append(self.__parse_hcoord(line))
            elif(line[0] == "f"):
                datas: 'list[str]' = line.split(" ")
                face: 'list[FaceProp]' = []
                for data in datas:
                    if(len(data) < 3):
                        continue
                    indices = data.split("/")
                    face.append(FaceProp(vertices[int(indices[0]) - 1], normals[int(indices[2]) - 1], uvs[int(indices[1]) - 1]))
                faces.append(face)
        file.close()
        shape = _Shape(self.file_name, vertices, normals, uvs, faces)
        shape.drawStyle = DrawStyle.SMOOTH

        for i in range(0, len(faces) + 1):
            shape.colors.append(ColorRGBA(1, 1, 1, 1))

        return shape
