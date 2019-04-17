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

    def get_minor(self):
        pass

    def try_invese(self):
        pass
