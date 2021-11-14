from datetime import datetime
from .polygon import Polygon

def export_as_obj(polygon: Polygon,filename: str) -> None:
    today = datetime.now()
    date_str = "{}-{}-{}_{}-{}-{}".format(today.year, today.month,
                                            today.day, today.hour,
                                            today.minute, today.second)
    obj_name = filename.split("/")[-1].split(".")[0]
    or_filename = obj_name+"_"+date_str+".obj"

    file = open(or_filename,"w")

    file.write(prepare_obj_header(obj_name,polygon.level))

    for vertex in polygon.vertices_to_vectors():
        file.write("v {} {} {}\n".format(vertex.x,vertex.y,vertex.z))
    
    file.write("\n")

    for link in polygon.vertex_links:
        if(link.level == polygon.level):
            file.write("f {} {} {} {}\n".format(link.links[0]+1,link.links[1]+1,link.links[2]+1,link.links[3]+1))

    file.close()


def prepare_obj_header(obj_name : str,level: int) -> str:
    return "# CENG487 Arif OBJ FILE\n# Assignment 3 November 2021\no "+obj_name+"_level_"+str(level)+"\n"