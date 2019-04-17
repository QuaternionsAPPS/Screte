from classes.matrix_class import Matrix
from classes.image_class import ImageClass


if __name__ == "__main__":
    m_1 = Matrix([[1, 2, 3], [111, 11, 1], [2, 1, 3]])
    m_2 = Matrix([[3, 2, 3], [1, 112, 1], [1, 1, 1]])
    v_0 = Matrix([ [3, 2, 3] ])
    v_1 = Matrix([ [3], [2], [3] ])

    # print(m_1.m, m_1.n)
    # print(m_1 * m_2)

    print(v_0.m, v_0.n)
    print(v_1.m, v_1.n)
    print(v_0 * v_1)
