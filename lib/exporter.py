# CENG 487 Assignment3 by
# Arif Burak Demiray
# StudentId: 250201022
# November 2021

from datetime import datetime
from .polygon import Polygon

def export_as_obj(polygon: Polygon,filename: str) -> None:
    """
    Exports given polygon object to .obj format

    Parameters:

    polygon that is going to be exported
    """
    today = datetime.now()
    date_str = "{}-{}-{}_{}-{}-{}".format(today.year, today.month,
                                            today.day, today.hour,
                                            today.minute, today.second)
    obj_name = filename.split("/")[-1].split(".")[0]  #preparing file name
    or_filename = obj_name+"_"+date_str+".obj"

    file = open(or_filename,"w")

    file.write(__prepare_obj_header(obj_name,polygon.level))  #write file headers

    for vertex in polygon.vertices_to_vectors():
        file.write("v {} {} {}\n".format(vertex.x,vertex.y,vertex.z)) #write vertices
    
    file.write("\n")

    for link in polygon.vertex_links:
        if(link.level == polygon.level): #write faces
            file.write("f {} {} {} {}\n".format(link.links[0]+1,link.links[1]+1,link.links[2]+1,link.links[3]+1))

    file.close()


def __prepare_obj_header(obj_name : str,level: int) -> str:
    return "# CENG487 Arif OBJ FILE\n# Assignment 3 November 2021\no "+obj_name+"_level_"+str(level)+"\n"