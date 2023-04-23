from PIL import Image


class ImageProcessor:
    def __init__(self, filename):
        self.image = Image.open(filename)
        self.width, self.height = self.image.size
        self.num_bit_planes = len(self.image.mode)

    def get_pixel(self, x, y):
        return self.image.getpixel((x, y))

    def set_pixel(self, x, y, pixel):
        self.image.putpixel((x, y), pixel)

    def save(self, filename):
        self.image.save(filename)
