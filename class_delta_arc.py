#-*- coding: utf-8 -*-
from math import *

from Proection import Proection


class Delta_long_lat(Proection):
    def __init__(self, proection, lat, long, inc_lat, inc_long):

        super().__init__(name=proection)

        self.p1 = super().Point(lat, long)

        self.inc_lat, self.inc_long = inc_lat, inc_long

        # Delta of X, 1st method. Длина долготы в (м/градусы)
        p2 = self.Point(self.p1['B'] + inc_lat, self.p1['L'] + inc_long)

        m0 = self.proection['a'] * (1 - self.e1_2)
        m2 = (3 / 2) * self.e1_2 * m0
        m4 = (5 / 4) * self.e1_2 * m2
        m6 = (7 / 6) * self.e1_2 * m4

        a0 = m0 + (m2 / 2) + (3 / 8) * m4
        a2 = (m2 / 2) + (m4 / 2) + (15 / 32) * m6
        a4 = (m4 / 8) + (3 / 16) * m6
        a6 = m6 / 32

        self.mi = (m0, m2, m4, m6)
        self.ai = (a0, a2, a4, a6)

        X1 = a0 * self.p1['B'] - (a2 / 2) * sin(2 * self.p1['B']) + (
            a4 / 4) * sin(4 * self.p1['B']) - (a6 / 6) * sin(6 * self.p1['B'])

        X2 = a0 * p2['B'] - (a2 / 2) * sin(2 * p2['B']) + (a4 / 4) * sin(
            4 * p2['B']) - (a6 / 6) * sin(6 * p2['B'])

        self.delta_x = X2 - X1

        # Delta of X, 2nd method, Дельта долготы по формуле Симпсона

        Bmid = (p2['B'] + self.p1['B']) / 2

        p_mid = self.Point(Bmid, self.p1['L'])

        self.delta_Simpson = (inc_lat / 6) * (
            self.p1['M'] + 4 * p_mid['M'] + p2['M'])

        # 3rd method
        self.delta_x_3rd = p_mid['M'] * inc_lat

        # Delta of Y (delta len of latitude) latitude - 1, Длина параллели на 1ой широте

        self.delta_Y_1 = self.p1['N'][0] * cos(self.p1['B']) * inc_long

        # Delta of Y (delta len of latitude) latitude - 2, Длина параллели на 2ой широте

        self.delta_Y_2 = p2['N'][0] * cos(p2['B']) * inc_long

        #
    def __str__(self):

        sep = '_' * 20 + '|' + '_' * 20 + '|' + '_' * 20 + '|' + '_' * 20 + '|' + '_' * 20 + '|\n'

        labels = ("longitude 1st method", "longitude 2nd method",
                  "longitude 3rd method", "lat B1", "lat B2")
        val = (self.delta_x, self.delta_Simpson, self.delta_x_3rd,
               self.delta_Y_1, self.delta_Y_2)
        txt = 80 * '^' + '\n'
        txt += str(self.name) + ':\n'
        txt += 'Delta latitude: ' + str(degrees(self.inc_lat)) + '\n'
        txt += 'Delta latitude: ' + str(degrees(self.inc_long)) + '\n'

        for lab in labels:
            txt += lab.center(20) + '|'
        txt += ('\n' + sep)
        for v in val:
            txt += str(v).center(20) + '|'
        return txt


if __name__ == '__main__':
    n = int(input('Введите пожалуйста свой номер варианта: '))
    mod_n = n % 6
    grads_of_var = n // 6

    B = radians(55 + grads_of_var + ((10 + mod_n * 10) / 60))
    L = radians(37.5)
    for proection in Proection.list:

        delta_1grad = Delta_long_lat(proection, B, L, radians(1), radians(1))
        delta_1min = Delta_long_lat(proection, B, L, radians(1 / 60),
                                    radians(1 / 60))
        delta_1sec = Delta_long_lat(proection, B, L, radians(1 / 3600),
                                    radians(1 / 3600))
        for i in range(len(delta_1grad.mi)):
            print(
                ('m' + str(i * 2) + ': ' + str(delta_1grad.mi[i])).center(30) +
                ' | ' +
                ('a' + str(i * 2) + ": " + str(delta_1grad.ai[i])).center(30))
        labels = ("Меридиан 1 метод", "Меридиан 2 метод", "Меридиан 3 метод",
                  "Параллель B1", "Параллель B2")
        attrs = ('delta_x', 'delta_Simpson', 'delta_x_3rd', 'delta_Y_1',
                 'delta_Y_2')
        print('^' * 90 + '|')
        print(proection, ':')
        for lab, attr in zip(labels, attrs):
            print(
                lab.center(20), '|',
                str(getattr(delta_1grad, attr)).center(20), '|',
                str(getattr(delta_1min, attr)).center(20), '|',
                str(getattr(delta_1sec, attr)).center(20), '|')
        print('^' * 91)
