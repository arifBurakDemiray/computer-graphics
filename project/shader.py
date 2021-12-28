# CENG 487 Assignment6 by
# Arif Burak Demiray
# StudentId: 250201022
# December 2021


import os


class Shader:

    def __init__(self) -> None:
        self.filenames = ["vertex_shader.glsl", "fragment_shader.glsl"]

    def get_vertex_shader(self) -> None:
        if(not check_file(self.filenames[0])):
            print("You are not in the correct directory. Go to shader's directory")
        f = open("shader/" + self.filenames[0], "r")

        file = f.read()

        f.close()

        return file

    def get_fragment_shader(self) -> None:
        if(not check_file(self.filenames[1])):
            print("You are not in the correct directory. Go to shader's directory")
        f = open("shader/" + self.filenames[1], "r")

        file = f.read()

        f.close()

        return file


def check_file(filename: str) -> bool:
    return filename in os.listdir("shader")
