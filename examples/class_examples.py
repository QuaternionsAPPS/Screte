from classes.matrix_class import Matrix
from classes.image_class import ImageClass


if __name__ == "__main__":

    # matrix multiplication example
    m_1 = Matrix([[1, 2, 3], [111, 11, 1], [2, 1, 3]])
    m_2 = Matrix([[3, 2, 3], [1, 112, 1], [1, 1, 1]])
    print(m_1 * m_2)

    # vector multiplication
    v_0 = Matrix([ [3, 2, 3] ])
    v_1 = Matrix([ [3], [2], [3] ])
    print(v_0 * v_1)

    # image read example: !!!
    data_arr = ImageClass.read_img_to_arr("../image_examples/ex1.png")
    m = Matrix(data_arr)
    print(m)

