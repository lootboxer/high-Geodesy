#-*- coding: utf-8 -*-
from math import *

from class_delta_arc import Delta_long_lat


class Frame(Delta_long_lat):
    """Вычисление длины рамок  и площади съемочной трапеции
        масштаба m, относительно точки с широтой B и долготой L
        "left-bottom corner of Frame, (type: Geoid.Point)" """

    def __init__(self, proection, scale, B, L):

        self.scale = scale
        self.scales = {
            1000000: (radians(4), radians(6)),
            500000: (radians(2), radians(3)),
            200000: (radians(2 / 3), radians(1)),
            100000: (radians(1 / 3), radians(1 / 2)),
            50000: (radians(1 / 6), radians(1 / 4)),
            25000: (radians(1 / 12), radians(1 / 8)),
            10000: (radians(1 / 24), radians(1 / 16)),
            5000: (radians(1 / 48), radians(1 / 32))
        }
        self.delta_B = self.scales[scale][0]
        self.delta_L = self.scales[scale][1]

        super().__init__(proection, B, L, self.delta_B, self.delta_L)
        self.proection = proection
        self.c = (self.delta_x * 100) / scale
        self.a1 = (self.delta_Y_1 * 100) / scale
        self.a2 = (self.delta_Y_2) * 100 / scale
        self.d = sqrt(self.a1 * self.a2 + self.c**2)

        first = 2 / 3 * self.e1_2 * (sin(B + self.delta_B)**3 - (sin(B))**3)
        second = 3 / 5 * self.e1_2**2 * (sin(B + self.delta_B)**5 -
                                         (sin(B))**5)
        third = 4 / 7 * self.e1_2**3 * (sin(B + self.delta_B)**7 - (sin(B))**7)

        self.square = ((self.b**2) * self.delta_L * (
            sin(B + self.delta_B) - sin(B) + first + second + third)) / (10**6)

    def __str__(self):
        labels = ('c', 'a1', 'a2', 'd', 'square')
        vals = (self.c, self.a1, self.a2, self.d, self.square)
        txt = str(self.proection) + ':\n'
        for lab, val in zip(labels, vals):
            txt += lab + ': ' + str(val) + '\n'
        return txt


if __name__ == '__main__':
    n = int(input('Введите пожалуйста свой номер варианта: '))
    mod_n = n % 6
    grads_of_var = n // 6

    B = radians(50 + grads_of_var + ((10 + mod_n * 10) / 60))
    L = radians(37.5)

    for proection in Frame.list:
        frame = Frame(proection, 50000, B, L)
        print(frame)
