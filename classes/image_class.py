from PIL import Image


class ImageClass:

    @classmethod
    def read_img_to_arr(cls, img_path):
        """ Read raw image file and return as 2-dimentional array."""

        img = Image.open(img_path).convert('L')
        data = list(img.getdata())                                                        # img --> list of all pixels

        img_width, img_height = img.size

        img_arr = [data[i:(i+img_width)] for i in range(0, len(data), img_width)]                 # list.__len__(data)
        return img_arr

    def __init__():
        pass



if __name__ == "__main__":
    # ex:
    ImageClass.read_img_to_arr("../image_examples/ex1.png")
