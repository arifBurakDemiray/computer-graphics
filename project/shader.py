# CENG 487 Assignment5 by
# Arif Burak Demiray
# StudentId: 250201022
# December 2021

class Shader:

    
    def __init__(self) -> None:
        self.filenames = ["vertex_shader.glsl","fragment_shader.glsl"]    

    def get_vertex_shader(self) -> None:
        f = open(self.filenames[0],"r")

        file = f.read()

        f.close()

        return file

    def get_fragment_shader(self) -> None:
        f = open(self.filenames[1],"r")

        file = f.read()

        f.close()

        return file