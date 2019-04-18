from classes.matrix_class import Matrix
from classes.image_class import ImageClass

data_arr = ImageClass.read_img_to_arr("../image_examples/ex1.png")
matrix = Matrix(data_arr)
print(matrix)

# print([(i, j) for i in range(matrix.m) for j in range(matrix.n)])
res = [[matrix.get_det_small(i, j) for i in range(matrix.m)] for j in range(matrix.n)]
print(ImageClass(arr=res))
