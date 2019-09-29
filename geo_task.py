from math import *

from Proection import Proection


class Geo_task_direct(Proection):
    '''Прямая геодезическая задача, принимает Q1-точку с координатами B1,L1 и азимутом A1-2,
    Так же принимает в себя S1 - расстояние до точки Q2'''

    def __init__(self, proec, B1, L1, A1, S1):
        'Однострочный конструктор, все парам-ры переданы в экземпляр'
        self.__dict__.update({k: v for k, v in locals().items() if k != 'self'})
        super().__init__(name=proec)
        self.beta = 1.25 * self.e2_2
        #S0 - для всех вычислений 1 (функция не требуется)
        #self.S0 = radians(self.S1 / self.c)/360 
        self.S0 = 0.0322304

        # Оформим вычисления в виде lambda функций

        self.gamma = lambda B: self.beta * cos(B)**2
        self.V = lambda gamma: (1 + 0.6 * self.gamma(B1)) / (1 + 0.2 * self.gamma(B1))
        self.delta_B = lambda V, A: self.S0 * (V**3) * cos(A)
        self.delta_L = lambda V, A, B: self.S0 * V * (sin(A) / cos(B))

        #Вычисляем все приближения и сами Bi и Ai


        #dA1 = dL1 + sin(B1)
        self.V1 = self.V(self.gamma(self.B1))
        self.dB1 = self.delta_B(self.V1, self.A1)
        self.B2 = B1 + (1 / 2) * self.dB1
        self.dL1 = self.delta_L(self.V1, A1, B1)
        self.dA1 = self.dL1 + sin(B1)

        self.A2 = A1 + 1 / 2 * self.dA1
        self.V2 = self.V(self.gamma(self.B2))
        self.dL2 = self.delta_L(self.V2, self.A2, self.B2)

        #dA2 = dL2 * B2
        #Но т.к. как dL2 = self.deltaL2, dL2 - уже есть (найдено выше)
        self.dA2 = self.dL2 * self.B2

        #B3 = B1 + 1/4 * (dB1 + dB2)
        self.dB2 = self.delta_B(self.V2, self.A2)
        self.B3 = B1 + (1 / 4) * (self.dB1 + self.dB2)
        
        #A3 = A1 + 1/4 * (dA1 + dA2)
        self.A3 = A1 + 1 / 4 * (self.dA1 + self.dA2)

        #B4 = B1 - dB2 + 2dB3
        self.V3 = self.V(self.gamma(self.B3))
        self.dB3 = self.delta_B(self.V3, self.A3)
        self.B4 = B1 - self.dB2 + 2 * self.dB3
        #A4 = A1 - dA2 + 2*dA3
        self.dA3 = self.delta_L(self.V3, self.A3, self.B3) * sin(self.B3)
        self.A4 = A1 - self.dA2 + 2 * self.dA3
        self.dA4 = self.delta_L(self.V(self.gamma(self.B4)), self.A4, self.B4)
        #Вычисления dB4
        self.V4 = self.V(self.gamma(self.B4))
        self.dB4 = self.delta_B(self.V4, self.A4)

        # Вычисления dL3,dL4
        self.dL3 = self.delta_L(self.V3, self.A3, self.B3)
        self.dL4 = self.delta_L(self.V4, self.A4, self.B4)
        # Т.к. добавочные Ai и Bi  используются, как переменные
        # Добавим в итоговый экземпляр класса все парамтры точки Q2
        # Q2 => [B2,L2,A2]
        self.B2_work = B1 + 1 / 6 * (self.dB1 + 4 * self.dB3 + self.dB4)
        self.L2_work = self.L1 + 1 / 6 * (self.dL1 + 4 * self.dL3 + self.dL4)
        self.A2_work = A1 + 1 / 6 * (self.dA1 + 4 * self.dA3 + self.dA4)
        self.Q2 = {'B': self.B2_work, 'L': self.L2_work, 'A': self.A2_work}

        # Объединим все вычисления Bi в одну функцию (аргументы которой вычисляются вложенными функциями)

        # 2 часть лабораторной работы

    def __str__(self):
        sep = '-' * 130 + '\n'
        txt = 'Результаты вычислений приближений для алгоритма Бесселя:\n' + sep
        Ai = list(map(degrees,[A1, self.A2, self.A3, self.A4]))
        Bi = list(map(degrees,[B1, self.B2, self.B3, self.B4]))
        Vi = [self.V1,self.V2,self.V3,self.V4]
        Vi3 = [self.V1**3,self.V2**3,self.V3**3,self.V4**3]
        dBi = [self.dB1/360,self.dB2,self.dB3,self.dB4]
        dLi = [self.dL1,self.dL2,self.dL3,self.dL4]
        dAi = [self.dA1,self.dA2,self.dA3,self.dA4]
        txt += str('№ i'.center(5) + '|' 
                + '1'.center(30) + '|' 
                + '2'.center(30) + '|' 
                + '3'.center(30) + '|'
                + '4'.center(30) + '|\n')
        txt += sep
        rows = {'Ai':Ai,'Bi':Bi,'Vi':Vi,'Vi3':Vi3,'dBi':dBi,'dLi':dLi,'dAi':dAi}
        for key, row in rows.items():
            txt+='%s|' % key.center(5)
            for i in range(4):
                val = rows[key][i]
                if key == 'Ai' or key == 'Bi':
                    txt += ( str(int(val)) + ' grad ' 
                        + str(int((val % 1) * 60)) + ' min ' 
                        + str(round((((val - int(val)) * 60) - int(((val - int(val)) * 60))) * 60, 4)) + ' sec').center(30)
                elif key == 'Vi' or key == 'Vi3':
                    txt += str(val).center(30)
                else:
                    txt += ( str(degrees(val)*360) + ' sec').center(30)
                txt+='|'
            txt+='\n'
            txt += sep
        return txt
    

if __name__ == '__main__':
    n = int(input('Введите ваш вариант: '))
    B1 = radians(50 + 7 / 60 + 40 / 360)
    L1 = radians(23 + 45 / 60 + 14 / 360)
    A1 = radians(3 + n + 30 / 60 + 0 / 360)
    S1 = 281260.18
    task = Geo_task_direct('WGS-84', B1, L1, A1, S1)

    print(task)
