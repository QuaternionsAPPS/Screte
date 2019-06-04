from pyDH import DiffieHellman


class MyDiffieHellman(DiffieHellman):
    def __init__(self):
        super().__init__()

    def set_private_key(self, a):
        self._DiffieHellman__a = a


def diffie_hellman_shared_key(d1_prikey, d2_prikey):
    d1 = MyDiffieHellman()
    d2 = MyDiffieHellman()
    d1.set_private_key(d1_prikey)
    d2.set_private_key(d2_prikey)
    d1_shared_key = d1.gen_shared_key(d2.gen_public_key())

    return d1_shared_key


def diffie_hellman_private_key():
    d = DiffieHellman()
    sh_key = d.get_private_key()
    return sh_key
