from math import *

from Proection import Proection


class Triangle(Proection):
    "Вычисление сторон треугольника на поверхности эллипсоида, способом аддитаментов"

    def __init__(self, proection, b, A, B, C):
        """Дан сферический треугольник на поверхности эллипсоида
        с известной стороной  b и сферическими углами A, B, C"""

        # Нам потребуются параметры проекций, для этого передаём в экземпляр
        # Название проекции и передаём параметры в соответствии с проекцией
        # Т.к есть 1 известная нам сторона, а остальные находим =>, кроме параметр b из (Proection) нам ничего не нужно

        # Сфероидическая длина стороны обозначаются чере s_... (длина именуемой стороны)
        self.s_b = b

        self.A = radians(A[0] + A[1] / 60 + A[2] / 360)
        self.B = radians(B[0] + B[1] / 60 + B[2] / 360)
        self.C = radians(C[0] + C[1] / 60 + C[2] / 360)
        super().__init__(name=proection)
        self.k = 409 * pow(10, -8)

        # A с индексом стороны означает Аддимент
        self.Ab = self.k * ((self.s_b / 1000)**3)
        self.bt = self.s_b - self.Ab

        # В общем виде self.f_B = ((180/pi)*60**2)/2*(self.Rmid)

        #Для РФ:
        self.f_B = 0.00253

        self.epsilon = (self.f_B * (self.s_b / 1000)**2 * sin(self.A) * sin(
            self.C)) / sin(self.B)
        # Невязка по углам
        self.W = self.A + self.B + self.C - pi - self.epsilon

        # Стороны a,c плоского треугольника
        self.at = self.bt * (sin(self.A) / sin(self.B))
        self.ct = self.bt * (sin(self.C) / sin(self.B))

        # Аддитменты
        self.Aa = self.k * ((self.at / 1000)**3)
        self.Ac = self.k * ((self.ct / 1000)**3)

        # Cтороны (сферические)
        self.s_Aa = self.at + self.Aa + self.W / 3
        self.s_Ac = self.ct + self.Ac + self.W / 3
        self.s_Ab = self.s_b + self.W / 3

        # 2я часть работы "Решение треугольника по теореме Лежандра"

        self.A1 = self.A - radians(self.epsilon / 3) / 360
        self.B1 = self.B - radians(self.epsilon / 3) / 360
        self.C1 = self.C - radians(self.epsilon / 3) / 360

        #С исправленными за сферический избыток углами с длиной исходной сферической стороны
        #по теореме синусов для плоского треугольника находят значение длины остальных
        #сферических сторон треугольника.

        self.s_a = self.s_b * sin(self.A1) / sin(self.B1)
        self.s_c = self.s_b * sin(self.C1) / sin(self.B1)

    def __str__(self):
        txt = ''.center(20) + '|' + 'Плоские углы'.center(
            20) + '|' + 'sin углов'.center(
                20) + '|' + 'Плоская сторона'.center(20) + '|' + 'A,м'.center(
                    20) + '|' + 'Сферич. сторона, м'.center(20) + '|\n'

        for i in (('A', degrees(self.A), sin(self.A), self.at, self.Aa,
                   self.s_Aa), ('B', degrees(self.B), sin(self.B), self.bt,
                                self.Ab, self.s_b), ('C', degrees(self.C),
                                                     sin(self.C), self.ct,
                                                     self.Ac, self.s_Ac)):
            for k in i:
                txt += '%s' % str(round(
                    (k), 5) if not type(k) == str else k).center(20) + '|'
            txt += '\n'
        txt += '_' * 125 + '\nepsilon: {0}\nW: {1}\n'.format(
            self.epsilon, self.W)
        txt += "\n" + ''.center(20) + '|' + 'Сферические углы'.center(
            20) + '|' + '-epsilon / 3, sec'.center(
                20) + '|' + 'плоские углы'.center(
                    20) + '|' + 'sin углов'.center(
                        20) + '|' + 'Сферич. сторона, м'.center(20) + '|\n'
        for i in (('A', degrees(self.A1), self.epsilon / 3, degrees(self.A),
                   sin(self.A), self.s_a),
                  ('B', degrees(self.B1), self.epsilon / 3, degrees(self.B),
                   sin(self.B), self.s_b), ('C', degrees(self.C1),
                                            self.epsilon / 3, degrees(self.A),
                                            sin(self.C), self.s_c)):
            for k in i:
                txt += '%s' % str(round(
                    (k), 5) if not type(k) == str else k).center(20) + '|'
            txt += '\n'
        txt += 'Сравнение 2х способов:\n' + '_' * 125 + '\n'
        txt += "\n" + ''.center(20) + '|' + '-epsilon / 3, sec'.center(
            20) + '|' + 'плоские углы'.center(20) + '|' + 'sin углов'.center(
                20) + '|' + 'Сферич. сторона, м'.center(20) + '|\n'
        for i in (('A', self.epsilon / 3, degrees(self.A), sin(self.A),
                   self.s_a - self.s_Aa), ('B', self.epsilon / 3,
                                           degrees(self.B), sin(self.B),
                                           self.s_b - self.s_b),
                  ('C', self.epsilon / 3, degrees(self.A), sin(self.C),
                   self.s_c - self.s_Ac)):
            for k in i:
                txt += '%s' % str(round(
                    (k), 5) if not type(k) == str else k).center(20) + '|'
            txt += '\n'
        txt += '_' * 105 + '\n'
        return txt


if __name__ == '__main__':
    n = int(input('Введите вариант: '))
    for proec in Proection.list:
        tri = Triangle(proec, 45897.282 + n * 100, [62, 12, 45.257],
                       [50, 20, 20.552], [67, 26, 59.701])
        print(tri.at)
        print(proec + ':')
        print(str(tri))
