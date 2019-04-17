from classes.matrix_class import Matrix
from classes.image_class import ImageClass

data_arr = ImageClass.read_img_to_arr("../image_examples/ex1.png")
m = Matrix(data_arr)
print(m)

