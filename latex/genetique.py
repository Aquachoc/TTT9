#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 20 16:49:20 2018

@author: HELENE
"""


def create_batch(n):
    L=[]
    for i in range(n):
        L.append(Player())
    return L

def randomize(players):
    n=len(players[0].pond)-1
    for i in players:
        i.pond[:-1]=np.array([random_range*random()-
              random_range*0.5 for _ in range(n)])

def mutate(players):
    n=len(players)
    k=n//2
    podium(players)
    reset_scores(players)
    p=[]
    m=[]
    for i in range(k):
        p=players[-i-1].pond
        m=mutation(p)
        players[i]=Player(pond=p+m)
        #players[-i].survival+=1


def mutation(pond):
    n=len(pond)
    a=np.array([mut_range*random()-0.5*mut_range for _ in range(n)])
    return a

def generation(n=30,N=[],nb=100):
    if len(N)==0:
        N=create_batch(n)
        randomize(N)
    dummy_tournament(N,nb)
    mutate(N)
    return N

def dummy_tournament(players,n=60):
    b=Player(typ="dummy")
    j=0
    l=0
    w=0
    for i in players:
       print(j)
       j+=1
       for k in range(n):
            if l%(n//10):
               print(l)
            if n%2:
                main=Game(i,b)
            else:
                main=Game(b,i)
            main.auto_play()
            if main.winner==i.tmpId:
                w+=1
    return w
