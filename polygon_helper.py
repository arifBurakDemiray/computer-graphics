from vec3d import vec3d
from mat3d import mat3d

def vectors_to_matrices(vectors: list[vec3d]) -> mat3d:
    content = []

    vectors_len = len(vectors)

    for i in range(vectors_len):

        temp = vectors[i]

        content.extend([temp.x,temp.y,temp.z,temp.w])
    
    content.extend([0,0,0,1])

    return mat3d(content)