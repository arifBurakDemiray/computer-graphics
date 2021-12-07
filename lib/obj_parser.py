# CENG 487 Assignment3 by
# Arif Burak Demiray
# StudentId: 250201022
# November 2021

from lib.polygon import Edge, Polygon
from lib.vec3d import Vec3d
from lib.vertex_color import RGBA, VertexLink
from lib.list_helper import add_generic


class Parser:

    file_name : str

    def __init__(self, file_name : str) -> None:
        self.file_name = file_name

    def parse(self) -> Polygon:
        pass

class QuadParser(Parser):
    """
    This class parses quad objects
    """

    def __init__(self,file_name : str) -> None:
        super().__init__(file_name)

    def __parse_vertex(self,line: str) -> Vec3d:
        data : 'list[str]' = line.split(" ")
        return Vec3d(float(data[1]),float(data[3]),float(data[2]),1)
    
    def __parse_link(self,line: str) -> VertexLink:
        data : 'list[str]' = line.split(" ")
        return VertexLink([int(data[1])-1,int(data[2])-1,int(data[3])-1,int(data[4])-1],[RGBA(1,1,1)])

    def parse(self) -> Polygon:
        vertices : 'list[Vec3d]' = []
        links : 'list[VertexLink]' = []
        edges : 'list[Edge]' = []
        face_adjacents : 'list[Edge]' = []
        vertex_adjacents : 'list[Edge]' = []

        file = open(self.file_name,"r")

        for line in file:
            if(len(line)<1):
                continue
            if(line[0]=="v"):  #if vertex add vertices
                vertices.append(self.__parse_vertex(line))
            elif(line[0]=="f"):
                links.append(self.__parse_link(line))
        
        file.close()

        for i in range(len(links)):
            face_adjacents.append(Edge([],[],[]))
        for i in range(len(vertices)):
            vertex_adjacents.append(Edge([],[],[]))

        for link in links:
            idx = links.index(link)
            for i in range(4):
                edge = Edge([link.links[i % 4],link.links[(i+1) % 4]],[],[])
                index = add_generic(edges,edge)
                add_generic(edges[index].faces,link)
                face_adjacents[idx] = edges[index]
                vertex_adjacents[link.links[i % 4]] = edges[index]
                vertex_adjacents[link.links[(i+1) % 4]] = edges[index]

        for edge in edges:
            if(len(edge.faces)!=2):
                print("FACE ERROR")


        for edge in edges:
            for i in range(len(edges)):
                if(edge != edges[i] and edge.is_neighbour(edges[i])):
                    add_generic(edge.edges,edges[i])

        for edge in edges:
            if(len(edge.edges)!=4):
                print("EDGE ERROR")

        return Polygon(vertices,links).with_edges(edges).with_vertices(vertex_adjacents).with_faces(face_adjacents)

       

class TriParser(Parser):
    """
    This class parses quad objects
    """

    def __init__(self,file_name : str) -> None:
        super().__init__(file_name)

    def __parse_vertex(self,line: str) -> Vec3d:
        data : 'list[str]' = line.split(" ")
        return Vec3d(float(data[1]),float(data[3]),float(data[2]),1)
    
    def __parse_link(self,line: str) -> 'list[VertexLink]':
        data : 'list[str]' = line.split(" ")
        return [VertexLink([int(data[1])-1,int(data[2])-1,int(data[3])-1],[RGBA(1,1,1)]),
        VertexLink([int(data[1])-1,int(data[3])-1,int(data[4])-1],[RGBA(1,1,1)])]

    def parse(self) -> Polygon:
        vertices : 'list[Vec3d]' = []
        links : 'list[VertexLink]' = []
        edges : 'list[Edge]' = []
        face_adjacents = []
        vertex_adjacents = []

        file = open(self.file_name,"r")

        for line in file:
            if(len(line)<1):
                continue
            if(line[0]=="v"):  #if vertex add vertices
                vertices.append(self.__parse_vertex(line))
            elif(line[0]=="f"):
                links.extend(self.__parse_link(line))
        
        file.close()

        for i in range(len(links)):
            face_adjacents.append(-1)
        for i in range(len(vertices)):
            vertex_adjacents.append(-1)

        for link in links:
            len_links = len(link.links)
            for i in range(len_links):
            
                edge = Edge([link.links[i % len_links],link.links[(i) % len_links]],
                [links.index(link)],[])
                index = add_generic(edges,edge)
                if(index!=len(edges)-1):
                    add_generic(edges[index].faces,links.index(link))
                face_adjacents[links.index(link)] = index
                vertex_adjacents[link.links[i % len_links]] = index
                vertex_adjacents[link.links[(i) % len_links]] = index

        for edge in edges:
            for i in range(len(edges)):
                if(edge.is_neighbour(edges[i])):
                    edge.edges.append(i)

        return Polygon(vertices,links).with_edges(edges).with_vertices(vertex_adjacents).with_faces(face_adjacents)

                # face_point = Vec3d(0,0,0,0)
                # for i in links[-1].links:
                #     face_point+=vertices[i]
                # face_point=face_point.multiply(1/len(links[-1].links))
                # links[-1].face_point = face_point