#-*- coding: utf-8 -*-
from math import *


class Proection:
    list = ('Kras', 'WGS-84', 'PZ-90')

    def __init__(self, name='WGS-84'):
        self.name = name
        self.proections = {
            "Kras": {
                'a': 6378245,
                'alpha': 1 / 298.3
            },
            'WGS-84': {
                'a': 6378137,
                'alpha': 1 / 298.25
            },
            'PZ-90': {
                'a': 6378136,
                'alpha': 1 / 298.257839
            }
        }
        self.proection = self.proections[self.name]
        self.b = round(self.proection['a'] * (1 - self.proection['alpha']),
                       4)  # *Округление до 4х знаков после запятой

        self.e1_2 = round(
            self.proection['alpha'] * (2 - self.proection['alpha']),
            10)  # Квадрат первого эксцентриситета

        self.e2_2 = round(self.e1_2 / (1 - self.e1_2),
                          10)  # Квадрат второго эксцентриситета

        self.c = round(self.proection['a']**2 / self.b,
                       4)  #Значение полярного радиуса

        self.points = [
        ]  # Рассматриваемые точки в географических координатах (радианы) с параметрами

    def Point(self, B, L) -> dict:

        W = sqrt(1 - (self.e1_2 * (sin(B))**2))
        V = sqrt(1 + (self.e2_2 * (cos(B))**2))

        #Значения главных радиусов кривизны главных нормальных сечений и среднего радиуса кривизны: меридиана - М, первого вертикала - N, радиуса кривизны - Rср
        M = self.c / pow(V, 3)
        #3 способа вычисления 'N'

        N = [
            self.c / V, self.proection['a'] / W,
            self.proection['a'] / (1 - self.e1_2 * pow(sin(B), 2))**(1 / 2)
        ]

        Rmid = sqrt(M * N[0])  # Радиус кривизны

        U = atan((1 - self.e1_2)**(1 / 2) * tan(B))  # Приведённая широта

        x = round(self.proection['a'] * cos(U) * cos(L), 4)
        y = round(self.proection['a'] * cos(U) * sin(L), 4)
        z = round(self.b * sin(U), 4)
        parameters = {
            'B': B,
            'L': L,
            'W': W,
            'V': V,
            'M': M,
            'N': N,
            'Rmid': Rmid,
            'U': U,
            'x': x,
            'y': y,
            'z': z
        }
        self.points += parameters
        return parameters
