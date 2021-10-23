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
        """
        This function calculates transpose of the caller mat3d object

        Returns:

        Transposed version of new mat3d object
        """

        value = []

        for i in range(4):
            for y in range(4):
                value.append(self.content[y*4 + i])

        return mat3d(value)

    def calc_multiplacation(self,matrix: 'mat3d') -> 'mat3d':
        """
        Calculates multiplacation of two 4x4 matrices, 
        it start multiplacation with parameter mat3d attribute

        Parameters:

        A mat3d object

        Returns:

        A new mat3d object that multiplied with caller mat3d object

        """
        value = []

        for z in range(4):
            for i in range(4):
                total = 0
                for y in range(4):
                    total += matrix.content[z*4+y]*self.content[y*4 + i]
                value.append(total)

        return mat3d(value)