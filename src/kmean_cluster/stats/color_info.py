'''
Color data contains in a image
Includes the percentage of a color
And RGB data of the color
'''


class ColorInfo:

    def __init__(self, percent, RGB):
        # percentage of certain color
        self.percent = percent
        # the color RGB value as a tuple
        self.RGB = RGB

    def __str__(self):
        return "Color [{}, {}, {}] of {:.5f}". \
            format(self.RGB[0], self.RGB[1], self.RGB[2], self.percent)

    def __eq__(self, other):
        return self.percent == other.percent

    def __lt__(self, other):
        return self.percent < other.percent
