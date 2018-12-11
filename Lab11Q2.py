# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 19:44:37 2017

@author: Xianan
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 16:14:28 2017

@author: Xianan
"""

from numpy import array,random,exp,empty,mean
from pylab import title,xlabel,ylabel,plot
N = 20
def findneighbor(latt,x,y):
    #Here defined the up, down, left, right neighbors are stored in below 
    #array, neighbor, from [0,0],[0,1],[1,0],[1,1]
    neighbor = empty([2,2],float)
    if (y==0):
        neighbor[1,0] = latt[x,N-1]
    else:
        neighbor[1,0] = latt[x,y-1]    
    if (y==(N-1)):
        neighbor[1,1] = latt[x,0]
    else:
        neighbor[1,1] = latt[x,y+1]
    if (x==0):
        neighbor[0,0] = latt[N-1,y]
    else:
        neighbor[0,0] = latt[x-1,y]
    if (x==(N-1)):
        neighbor[0,1] = latt[0,y]
    else:
        neighbor[0,1] = latt[x+1,y]
    return neighbor
def EnergyCalculator(latt,m,n):
    return sum(sum(-latt[m,n]*findneighbor(latt,m,n)))


#Initiate the lattice
latt = empty([N,N],float)
for m in range(N):
    for n in range(N):
        rd = random.random()
        if (rd<0.5):
            latt[m,n] = 1
        else:
            latt[m,n] = -1

#Number of MC steps
Ns = 1000000
Spin = []
for k in range(Ns):
    rdx = int(N*random.random())
    rdy = int(N*random.random())
    deltaE = -2*EnergyCalculator(latt,rdx,rdy)
    p = exp(-deltaE)
    if(random.random()<p):
        latt[rdx,rdy] = -latt[rdx,rdy]
        #print(p)
    SpinSum = sum(sum(latt))
    Spin.append(SpinSum)
print(sum(sum(latt)))
plot(range(Ns),Spin)
title('spontaneous magnetization')
xlabel('Monte-Carlo steps')
