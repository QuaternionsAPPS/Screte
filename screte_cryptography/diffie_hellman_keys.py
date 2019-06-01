import pyDH


def diffie_hellman_shared_key(d1_pubkey, d2_pubkey):
    d1 = pyDH.DiffieHellman()
    d2 = pyDH.DiffieHellman()

    d1_sharedkey = d1.gen_shared_key(d2_pubkey)
    d2_sharedkey = d2.gen_shared_key(d1_pubkey)

    return d2_sharedkey


def diffie_hellman_public_key():
    d = pyDH.DiffieHellman()
    sh_key = d.gen_public_key()
    return sh_key
