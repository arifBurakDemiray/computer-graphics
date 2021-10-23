# CENG 487 Assignment1 by
# Arif Burak Demiray
# StudentId: 250201022
# October 2021

class mat3d:
    """
    This class holds a 4x4 matrix

    Please give matrix as an array because of memory access

    [4][1] in matrix
    width(row)*4 + 1 in array implementation

    so in the matrix [x,y] is equal to width(row)*y + x in the array
    """
    content = []

    def __init__(self,content: list[int]) -> 'mat3d':
        self.content = content

    def calc_transpose(self) -> 'mat3d':
        value = []

        for i in range(4):
            for y in range(4):
                value.append(self.content[y*4 + i])

        return mat3d(value)