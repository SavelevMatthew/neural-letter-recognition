import numpy as np
from PyQt5.QtGui import QImage
from PyQt5.QtCore import Qt

import matplotlib.pyplot as plt


class ImageCropper:
    def __init__(self, width, height):
        self.w = width
        self.h = height

    def handle_image(self, image):
        trimmed = self.trim_image(image)
        pixels = []
        w_step = int(trimmed.width() / self.w)
        h_step = int(trimmed.height() / self.h)
        for j in range(self.h):
            for i in range(self.w):
                counter = 0
                for x in range(i * w_step, (i + 1) * w_step):
                    for y in range(j * h_step, (j + 1) * h_step):
                        if trimmed.pixelColor(x, y) == Qt.white:
                            counter += 1
                res = (1 - float(counter) / (w_step * h_step)) * 0.99 + 0.01
                pixels.append(res)
        return np.asfarray(pixels)

    def trim_image(self, image):
        w_s, w_f = self.horizontal_trim(image)
        h_s, h_f = self.vertical_trim(image)
        return image.copy(w_s, h_s, w_f - w_s, h_f - h_s)

    def vertical_trim(self, image):
        start = -1
        finish = -1
        for h in reversed(range(image.height())):
            for w in range(image.width()):
                if image.pixelColor(w, h) == Qt.black:
                    start = h
                    break
        for h in range(image.height()):
            for w in range(image.width()):
                if image.pixelColor(w, h) == Qt.black:
                    finish = h
                    break
        return (start, finish)

    def horizontal_trim(self, image):
        start = -1
        finish = -1
        for w in reversed(range(image.width())):
            for h in range(image.height()):
                if image.pixelColor(w, h) == Qt.black:
                    start = w
                    break
        for w in range(image.width()):
            for h in range(image.height()):
                if image.pixelColor(w, h) == Qt.black:
                    finish = w
                    break
        return (start, finish)
