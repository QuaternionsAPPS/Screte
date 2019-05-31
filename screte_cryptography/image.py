import cv2
import numpy as np
import hashlib
from statistics import mean
import pyDH


PRIME_NUMBER = 257


def diffie_hellman_key(d1_pubkey, d2_pubkey):
    d1 = pyDH.DiffieHellman()
    d2 = pyDH.DiffieHellman()

    d1_sharedkey = d1.gen_shared_key(d2_pubkey)
    d2_sharedkey = d2.gen_shared_key(d1_pubkey)

    return d2_sharedkey


def form_secret_key(img, user_info):
    uses_hash = int(hashlib.md5(user_info.encode('utf-8')).hexdigest(), 16) % (2 ** 32 - 1)
    np.random.seed(uses_hash)
    b, g, r = cv2.split(img)
    secret_key = np.random.randint(1, 255, size=b.shape)

    return secret_key


class ImageLoaderAndSaver:
    @classmethod
    def load_image_locally(cls, path):
        return cv2.imread(path)

    @classmethod
    def load_uploaded_image(cls, req_img):
        return cv2.imdecode(np.fromstring(req_img.read(), np.uint8), cv2.IMREAD_UNCHANGED)

    @classmethod
    def load_image_by_url(cls, path):
        pass

    @classmethod
    def save_image_locally(cls, img, path):
        cv2.imwrite(path, img)

    @classmethod
    def save_image_by_url(cls, path):
        pass


class Image:
    @staticmethod
    def encrypt_layer(layer, secret_key):
        layer = np.array(layer, int)
        encrypted_layer = (((layer + 1) * secret_key) % PRIME_NUMBER) % 256

        for i, row in enumerate(encrypted_layer):
            for j, el in enumerate(row):
                if (el == 0) and ((layer[i][j] != 0) or (layer[i][j] != 255)):
                    encrypted_layer[i][j] = (((layer[i][j]) * secret_key[i][j]) % PRIME_NUMBER) % 256

        return encrypted_layer

    @classmethod
    def encrypt_img(cls, img, secret_key):
        b, g, r = cv2.split(img)
        encrypted_b = Image.encrypt_layer(b, secret_key)
        encrypted_g = Image.encrypt_layer(g, secret_key)
        encrypted_r = Image.encrypt_layer(r, secret_key)
        rgb_img = cv2.merge([encrypted_b, encrypted_g, encrypted_r])
        return rgb_img

    @staticmethod
    def decrypt_layer(layer, reverse_key):
        layer = np.array(layer, int)
        decrypted_layer = (layer * reverse_key - 1) % PRIME_NUMBER
        return decrypted_layer

    @classmethod
    def decrypt_img(cls, img, secret_key):
        b, g, r = cv2.split(img)

        reverse_key = np.ones(secret_key.shape)
        for i in range(PRIME_NUMBER - 2):
            reverse_key = reverse_key * secret_key % PRIME_NUMBER

        encrypted_b = Image.decrypt_layer(b, reverse_key)
        encrypted_g = Image.decrypt_layer(g, reverse_key)
        encrypted_r = Image.decrypt_layer(r, reverse_key)
        brg_img = cv2.merge([encrypted_b, encrypted_g, encrypted_r])
        return brg_img

    @staticmethod
    def smooth_layer(layer):
        height, width = layer.shape
        new_layer = np.ones(layer.shape)

        for i in range(2, height - 1):
            for j in range(2, width - 1):
                new_layer[i][j] = mean([layer[i - 1][j - 1], layer[i - 1][j], layer[i - 1][j + 1],
                                        layer[i][j - 1], layer[i][j], layer[i][j+1],
                                        layer[i + 1][j - 1], layer[i + 1][j], layer[i + 1][j + 1]])

        return new_layer

    @classmethod
    def smooth_img(cls, img):
        b, g, r = cv2.split(img)
        new_b = Image.smooth_layer(b)
        new_g = Image.smooth_layer(g)
        new_r = Image.smooth_layer(r)

        brg_img = cv2.merge([new_b, new_g, new_r])
        return brg_img
