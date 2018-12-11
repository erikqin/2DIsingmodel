# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 16:14:28 2017

@author: Xianan
"""

from numpy import array,random,exp,empty
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

latt = empty([N,N])

for m in range(N):
    for n in range(N):
        if (random.random()<0.5):
            latt[m,n] = 1
        else:
            latt[m,n] = -1

# Set Monte-carlo steps
Ns = 10
for k in range(Ns):
    rdx = int(N*random.random())
    rdy = int(N*random.random())
    deltaE = -2*EnergyCalculator(latt,rdx,rdy)
    p = exp(-deltaE)
    rd = random.random()
    print('Random value = ',rd,' p = ',p)
    if(rd<p):
        latt[rdx,rdy] = -latt[rdx,rdy]
        print('Accepted')
    else:
        print('Not accepted')