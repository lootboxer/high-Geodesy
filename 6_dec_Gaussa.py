from math import *
from Proection import Proection

def invert(txt):
  txt = ''.join(txt.split())
  txt = txt.replace(',','.')
  return float(txt)

A0 = '6 367 558, 497','6 367 449,147','6 367 446,861'
A2 = '32 072,960', '32 077,017', '32 076,935'
A4 = '67,312', '67,330', '67,330'
A6 = '0,132', '67,330', '0,130'
A0 = list(map(invert,A0))
A2 = list(map(invert,A2))
A4 = list(map(invert,A4))
A6 = list(map(invert,A6))

def nu (e2_2,B): 
  res = sqrt(e2_2*(cos(B)**2))
  return res
#формулы a0 воообще нет в помине нигде!!!!!
def a0(A2,B):
  res = A2-(135.3302-(0.7092-0.004*(cos(B)**2))*cos(B)**2)*cos(B)**2
  return res
def a2 (N,B): 
  res = (1/2)*N*sin(B)*cos(B)
  return res
def a4 (N,B,e2_2): 
  nu1 = nu(e2_2,B)
  print(nu1**4*4)
  res = (1/24)*sin(B)*(cos(B)**3)*(5-tan(B)**2+9*nu1**2-4*nu1**4)
  return res
def a6 (N,B,e2_2): 
  res = 1/720*N*sin(B)*cos(B)**5*(61-58*tan(B)**2+tan(B)**4+270*(nu(e2_2,B)**2)-330*(nu(e2_2,B)**2)*tan(B)**2)
  return res
def b1 (N,B): 
  res = N*cos(B)
  return res
def b3 (N,B,e2_2): 
  res = 1/6*N*cos(B)**3*(1-tan(B)**2+nu(e2_2,B))
  return res
def b5 (N,B,e2_2): 
  res = 1/120*N*cos(B)**5*(5-18*tan(B)**2+tan(B)**4+14*(nu(e2_2,B)**2)-58*nu(e2_2,B)*tan(B)**2)
  return res


class Dec_Gauss(Proection):
  def __init__(self,proec_name,B,L):
    super().__init__(proec_name)
    self.B = B
    self.L = L
    proec = Proection(proec_name)
    if proec.name == 'Kras':
      self.numb_proec = 1
    elif proec.name == 'WGS-84':
      self.numb_proec = 2
    elif proec.name == 'PZ-90':
      self.numb_proec = 3
    self.N = proec.Point(B,L)['N'][0]
    self.li = L-radians(27)
    self.a0 = A0[0]
    self.a2 = a2(self.N,B)
    self.a4 = a4(self.N,B,self.e2_2)
    self.a6 = a6(self.N,B,self.e2_2)
    self.x =  self.a0+ self.a2*self.li**2 + self.a4*self.li**4 + self.a6*self.li**6
    self.y = b1(self.N,B)*self.li + b3(self.N,B,self.e2_2) + b5(self.N,B,self.e2_2)


if __name__ == '__main__':
  B = [51,38,43.9]
  L = [24,2,13.136]
  B = radians(B[0]+B[1]/60+B[2]/360)
  L = radians(L[0]+L[1]/60+L[2]/360)
  gauss = Dec_Gauss('Kras',B,L)
  print(gauss.x)
  print(gauss.y) #Переход по формуле y=NcosB...