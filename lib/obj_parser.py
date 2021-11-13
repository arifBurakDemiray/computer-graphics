

from lib_arif.polygon import Polygon
from lib_arif.vec3d import Vec3d
from lib_arif.vertex_color import RGBA, VertexLink


class Parser:

    file_name : str

    def __init__(self, file_name : str) -> None:
        self.file_name = file_name

    def parse(self) -> Polygon:
        pass

class QuadParser(Parser):

    def __init__(self,file_name : str) -> None:
        super().__init__(file_name)

    def __parse_vertex(self,line: str) -> Vec3d:
        data : list[str] = line.split(" ")
        return Vec3d(float(data[1]),float(data[3]),float(data[2]),1)
    
    def __parse_link(self,line: str) -> VertexLink:
        data : list[str] = line.split(" ")
        return VertexLink([int(data[1])-1,int(data[2])-1,int(data[3])-1,int(data[4])-1],[RGBA(1,1,1)])

    def parse(self) -> Polygon:
        vertices : list[Vec3d] = []
        links : list[VertexLink] = []

        file = open(self.file_name,"r")

        for line in file:
            if(len(line)<1):
                continue
            if(line[0]=="v"):
                vertices.append(self.__parse_vertex(line))
            elif(line[0]=="f"):
                links.append(self.__parse_link(line))
        
        file.close()

        return Polygon(vertices,links)
