from PIL import Image
import numpy as np


class ImageClass:

    @classmethod
    def read_img_to_arr(cls, img_path):
        """ Read raw image file and return as 2-dimentional array."""

        img = Image.open(img_path).convert('L')
        data = list(img.getdata())                                                        # img --> list of all pixels

        img_width, img_height = img.size

        img_arr = [data[i:(i+img_width)] for i in range(0, len(data), img_width)]                 # list.__len__(data)
        return img_arr


    def __init__(self, path='', arr=None):
        if path:
            self.data = ImageClass.read_img_to_arr(path)
        elif arr:
            np_arr = np.asarray(arr)
            self.data = Image.fromarray(np_arr.astype('uint8'), 'L')
            self.data.save("your_file.jpeg")

    def __str__(self):
        self.data.show()
        return ''

