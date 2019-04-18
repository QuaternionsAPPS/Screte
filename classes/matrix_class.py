class Matrix:
    def __init__(self, arr, m=None, n=None):
        self.flags = dict()
        self.arr = arr
        if m and n:
            self.m, self.n = m, n
        else:
            self.m = len(arr)
            self.n = len(arr[0])

    def get_size(self):
        return self.m, self.n

    def get_col(self, c_ind):
        if c_ind < self.n:
            return [row[c_ind] for row in self.arr]

    def get_cols(self):
        return [self.get_col(i) for i in range(self.n)]

    def __getitem__(self, coords):
        row, col = coords
        return self.arr[row][col]

    def __mul__(self, other):
        if type(other) is Matrix:
            if self.n == other.m:
                res = [
                    [sum(row[j] * other.get_col(i)[j] for j in range(self.n)) for row in self.arr]
                                                                                              for i in range(other.n)]
                return Matrix(res)

            raise ArithmeticError(" incompatible sizes of operands ")
        raise TypeError(" incompatible types of operands ")

    def __repr__(self):
        return ', '.join(str(row) for row in self.arr)

    def __str__(self):
        print("\n{}x{} matrix \n".format(self.m, self.n))
        return '\n'.join('  '.join(["{:>4}".format(e) for e in row]) for row in self.arr)

    def is_invertible(self):
        pass

    def is_horizontal(self):
        return self.m < self.n

    def is_vertical(self):
        return self.m > self.n

    def is_square(self):
        return self.m == self.n

    def get_sub_matrix(self, from_coords, to_coords):
        if type(from_coords) == type(to_coords) == tuple:
            sub = [[row[j] for j in range(from_coords[1], to_coords[1])] for row in self.arr[from_coords[0]:to_coords[0]]]
            return Matrix(sub)
        raise TypeError(" tuples of ints are expected ")

    def get_det_small(self, i, j):
        if i < self.m-1 and j < self.n-1:
            print(i, j, "---", self.m, self.n)
            print(self.arr[i][j], self.arr[i+1][j+1], self.arr[i][j] * self.arr[i+1][j+1])
            return (self.arr[i][j] * self.arr[i+1][j+1]) - (self.arr[i][j+1] * self.arr[i+1][j])
        elif i == self.m or j == self.n:
            return self.arr[i][j]
        else:
            return 0
