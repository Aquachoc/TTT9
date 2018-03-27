# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 15:31:16 2018

@author: PEUSTACHE
"""

def bToG(grid):
    G=[]
    L=[] #grilel annexe
    for i in range(3):
        L=[]
        for j in range(3):
            L.append(bgElem(grid, i,j))
        G.append(L)
    return G

def bgElem(grid,i,j):
    return (grid>>((i*3+j)*2))%4

def bgToB(grid):
    G=0
    for i in range(3):
        for j in range(3):
            G<<=2
            print(G)
            G+=grid[2-i][2-j]
    return G

def setBg(bgrid,k,e):
    b=bgrid%(4**(k-1))
    print(bin(b))
    a=bgrid>>(2*k)
    print(bin(a))
    a<<=2
    a+=e
    return (a<<2*(k-1))+b
    
