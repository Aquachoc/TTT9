# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 15:31:16 2018
@author: PEUSTACHE
"""
from tkinter import *
import numpy as np
from random import random
import math
x=0
y=0
mut_range=6
random_range=10
def bToG(grid): #binaire -> tableau
    G=[]
    L=[] #grille annexe
    for i in range(3):
        L=[]
        for j in range(3):
            L.append(bgElem(grid, i,j))
        G.append(L)
    return G

def bgElem(grid,i,j): # renvoie l'élément (i,j) d'une bg
    return (grid>>((i*3+j)*2))%4

def gToB(grid): 
    G=0
    for i in range(3):
        for j in range(3):
            G<<=2
            print(G)
            G+=grid[2-i][2-j]
    return G

def setBg(bgrid,k,e): # met le k^e element a e
    b=bgrid%(4**(k-1))
    print(bin(b))
    a=bgrid>>(2*k)
    print(bin(a))
    a<<=2
    a+=e
    return (a<<2*(k-1))+b

def isWon(grid) : #pour une grille array
    for i in range(3):
        if([grid[i][j] for j in range(3)] in [[1 for j in range (3)], [2 for j in range (3)]]): #si toute un ligne est pareille
            return grid[i][0] #prendre la couleur du vaiqueur
        if([grid[j][i] for j in range(3)] in [[1 for j in range (3)], [2 for j in range (3)]]): #si toute un ligne est pareille
            return grid[0][i]
    if([grid[i][i] for i in range(3)] in [[1 for j in range (3)], [2 for j in range (3)]]):
        return grid[0][0]
    if([grid[-i-1][i] for i in range(3)] in [[1 for j in range (3)], [2 for j in range (3)]]):
        return grid[0][-1]
    k=0
    for i in range(3):
        for j in range(3):
            k+=(grid[i][j]>0)
    if k==9:
        return -1
    return 0

#class App:
#
#    def __init__(self, master):
#
#        frame = Frame(master)
#        frame.pack()
#
#        self.button = Button(
#            frame, text="QUIT", fg="red", command=frame.quit
#            )
#        self.button.pack(side=LEFT)
#
#        self.hi_there = Button(frame, text="Hello", command=self.say_hi)
#        self.hi_there.pack(side=LEFT)
#
#    def say_hi(self):
#        print("Hello world!")

def gprint(grid):
    
    root = Tk()
    w = Canvas(root, width=900, height=900)
    w.pack()
    for i in range(1,9):
        if i%3:
            w.create_line(0,i*100,900,i*100)
            w.create_line(i*100,0,i*100,900)
        else:
            w.create_line(0,i*100,900,i*100, fill = "red", width=5)
            w.create_line(i*100,0,i*100,900, fill = "red", width=5)
    for k in range(3):
        for l in range(3):
            for i in range(3):
                for j in range(3):
                    if grid[k][l][i][j]==2:
                        circle(w,k,l,i,j)
                        print("circle",i,j,k,l,'\n')
                    elif grid[k][l][i][j]==1:
                        cross(w,k,l,i,j)
                        print("cross",i,j,k,l,'\n')
    metaGrid=winGrid(grid)
    for i in range(3):
        for j in range(3):
            if metaGrid[i][j]==2:
                bigCircle(w,i,j)
            elif metaGrid[i][j]==1:
                bigCross(w,i,j)
            
    
    root.mainloop()
    root.destroy()
    
            
            
def gridPos(k,i=1,j=1):
    return ((50+100*j+(k//3)*300),(50+100*(i%3)+300*(k%3)))

def circle(w,k,l,i,j,r=35,wi=10,d=(5,1)):
    x,y=gridPos(l*3+k,i,j)
    w.create_oval(x-r, y-r, x+r, y+r, outline="blue", width=wi,dash=d)
def cross(w,k,l,i,j,r=35,wi=10,d=(5,1)):
    x,y=gridPos(l*3+k,i,j)
    w.create_line(x-r, y-r, x+r, y+r, fill="green", width=wi, dash=d)
    w.create_line(x-r, y+r, x+r, y-r, fill="green", width=wi,dash=d)

def winLine(w,win,i,j):
    x=gridPos(i)
    y=gridPos(j)
    c=""
    if(win==1):
        c="blue"
    else :
        c="green"
    w.create_line(x[0],x[1],y[0],y[1], fill=c, width = 15)
    
    
def bigCircle(w,k,l):
    circle(w,k,l,1,1,r=130,wi=25,d=(2,4))

def bigCross(w,k,l):
    cross(w,k,l,1,1,r=130, wi=25,d=(2,4))
    
def winGrid(grid):
    L=[]
    M=[]
    for i in range(3):
        M=[]
        for j in range(3):
            M.append(isWon(grid[i][j]))
        L.append(M)
    return L

def findZ(grid): #find 0 for 3*3
    L=[]
    for i in range(3):
        for j in range(3):
            if not grid[i][j]:
                L.append([i,j])
    return L
        
def possible(grid, last, mgrid=[]):
    if last==[3,3]:
        a=np.where(grid==0)
        b= list(zip(a[0],a[1],a[2],a[3]))
    else:
        g=np.array(grid[last[0]][last[1]])
        a=np.where(g==0)
        n=len(a[0])
        b=zip(last[0]*np.ones(n,dtype=int),last[1]*np.ones(n,dtype=int),a[0],a[1])
        b= list(b)
    if len(mgrid)>0:    
        k=0
        while k<len(b):
            if mgrid[b[k][0]][b[k][1]]:
                del(b[k])
            else:
                k+=1
    return b
        
        
        

class Game:
    def __init__(self,p1,p2,IA=0):
        self.p1=p1
        self.p2=p2
        self.mgrid=np.zeros((3,3),dtype=int)
        self.grid=np.zeros((3,3,3,3),dtype=int)
        self.winner=0
        self.actual=1
        self.last=[3,3]
        self.dispo=np.ones((3,3,3,3), dtype=int)
        self.hist=[]  
        self.gagnable=np.ones((2,3,3),dtype=int)
        self.p1.tmpId=1
        self.p2.tmpId=2
        self.p1.gAct=self.p2.gAct=self
        self.turn=-1
        self.mHist=np.zeros((3,3),dtype=int)
    def move(self,m):
        i,j,k,l=m
        vict=0
        histM=0
        if not self.grid[i][j][k][l]:
            if (self.last==[i,j] or self.last==[3,3]): # and self.grid[i][j][k][l]==0
                self.grid[i][j][k][l]=self.actual
                self.last=[k,l]
                histM=isWon(self.grid[i][j])
                self.mgrid[i][j]=histM
                if histM>0:
                    self.mHist[i][j]=self.turn
                vict=isWon(self.mgrid)              #grosse amélioration possible
                if vict:
                    self.winner=vict
                    return vict
                if self.mgrid[k][l]:
                    self.last=[3,3]
            else :
                print("Coup", m, "invalide`\n")
                
    def auto_play(self):
        while self.winner==0:
            self.turn+=1
            if self.actual==1:
                m=self.p1.move()
                
            else:
                m=self.p2.move()
            if m!=None:
                self.move(m)
                self.hist.append(m)
                self.actual=1+self.actual%2
            else:
                self.winner=-1
                
        if self.winner==1:
            self.p1.score+=1
        elif self.winner==2:
            self.p2.score+=1
        else:
            self.p1.score+=0.5
            self.p2.score+=0.5

class Player:
    name=0
    def __init__(self,pond=[3,2,1,1,1,1,1,1,1,1,1, math.inf],typ="normal"):
        self.score=0
        self.name=Player.name
        Player.name+=1
        self.pond=np.array(pond)
        self.tmpId=0
        self.gAct=None
        self.typ=typ
    def move1(self,grid,last,mgrid):
        poss=possible(grid,last,mgrid)
        n=len(poss)
        if not n:
            return None
        k=n*random()
        k=int(k)
        return poss[k]
    
    def move2(self):
        poss=possible(self.gAct.grid,self.gAct.last,self.gAct.mgrid)
        i=-math.inf
        n=len(poss)
        M=None
        s=0
        if not n:
            return None
        for m in poss:
            s=self.eurist(m)
            if s>i:
                M=m
                i=s
        return M
    
    
    def move(self):
        if self.typ=="dummy":
            return self.move1(self.gAct.grid, self.gAct.last, self.gAct.mgrid)
        return self.move2()
    
    def indicateurs(self,m):
        g=self.gAct
        k=m[0:2]
        m=m[2:]
        tmp=np.array(g.grid)
        tmp[k[0]][k[1]][m[0]][m[1]]=self.tmpId
        won=isWon(tmp[k[0]][k[1]])
        adv_winnable=winnable(tmp[k[0]][k[1]], 1+self.tmpId%2)
        mGrid=winGrid(tmp)
        capture=(mGrid[k[0]][k[1]]==self.tmpId)*1
        victory=isWon(mGrid)
        return[1*center_flag(m), 1*corner_flag(m), 1*border_flag(m),  nbPions(g.grid[m[0]][m[1]],self.tmpId,m), nbPions(g.grid[m[0]][m[1]], 1+(self.tmpId%2), m), 1*(g.mgrid[m[0]][m[1]]!=0), 1*winnable(g.grid[m[0]][m[1]]), int(winnable(g.grid[m[0]][m[1]], 1+self.tmpId%2)),won, int(adv_winnable), capture, victory]
    
    def eurist(self,m):
        flags=np.array(self.indicateurs(m))
        if not flags[-1]:
            score=sum(flags[:-1]*self.pond[:-1])
        else:
            score=sum(flags*self.pond)
        return score
    
def conti(event):
    n=len(event.widget.g.hist)
    c=event.widget.count
    if c%2==1 and c<=n:
        h=event.widget.g.hist[c-1]
        a=cross(event.widget,h[0],h[1],h[2],h[3])
        event.widget.tmp.append(a)
        if event.widget.g.mHist[h[0]][h[1]]==c-1:
            event.widget.mTmp.append(bigCross(event.widget,h[0],h[1]))
        else:
            event.widget.mTmp.append(None)
        event.widget.count+=1
    else:
        h=event.widget.g.hist[c-1]
        event.widget.tmp.append(circle(event.widget,h[0],h[1],h[2],h[3]))
        if event.widget.g.mHist[h[0]][h[1]]==c-1:
            event.widget.mTmp.append(bigCircle(event.widget,h[0],h[1]))
        else:
            event.widget.mTmp.append(None)
        event.widget.count+=1
    return 1
    
        
#    def eva(grid,move)
def gHist(game):
        root = Tk()
        w = Canvas(root, width=900, height=900)
        w.pack()
        w.tmp=[]
        w.mTmp=[]
        w.count=1
        w.g=game
        w.root=root
        w.bind("<Button-1>", conti)
        w.bind("<Button-3>", prev)
        for i in range(1,9):
            if i%3:
                w.create_line(0,i*100,900,i*100)
                w.create_line(i*100,0,i*100,900)
            else:
                w.create_line(0,i*100,900,i*100, fill = "red", width=5)
                w.create_line(i*100,0,i*100,900, fill = "red", width=5)
        root.mainloop()  
        print(len(w.tmp))
            
def prev(event):
    n=len(event.widget.g.hist)
    c=event.widget.count
    if n>0:
        event.widget.count-=1
        if event.widget.mTmp[-1]!=None:
            event.widget.delete(event.widget.mTmp[-1])
            del(event.widget.mTmp[-1])
        event.widget.delete(event.widget.tmp[-1])
        del(event.widget.tmp[-1])
    event.widget.root.update()
    return 1

def create_batch(n):
    L=[]
    for i in range(n):
        L.append(Player())
    return L
            
def score_ext(player):
    return player.score

        
def reset_scores(players):
    for i in players:
        i.score=0

def recap(players):
    n=len(players)
    for i in range(n):
        print(players[i].score,players[i].name,"\n")
        
def tournament(players,typ='f'):
    if typ=='f':
        n=len(players)
        tot=n*(n-1)/2
        c=0
        for i in range(n):
            for j in range(i):
                main=Game(players[i],players[j])
                main.auto_play()
                del(main)
                c+=1
                print('{0:4f}'.format(c/tot))
            
            
def podium(players):
    players.sort(key=score_ext)

def winnable(grid,player=0): #0=both
    if player :    
        g=np.array(grid)
        g[g==0]=player
        a=(isWon(g)==player)
    if not player :
        player=1
        g=np.array(grid)
        g[g==0]=player
        a=(isWon(g)==player)
        g=np.array(grid)
        g[g==0]=1+player%2
        
        b=(isWon(g)==1+player%2)
        return a*b
    return a

def corner_flag(m):
    return((m in [[0,2],[2,0],[0,0],[2,2]]))

def border_flag(m):
    return((m in [[0,1],[1,0],[2,1],[1,2]]))

def center_flag(m):
    return (m == [1,1])

def nbPions(grid, nbPlayer, m=[]):
    if not len(m):
        k=-1
        for i in range(3):
            for j in range(3):
                k = max(k,nbPions(grid,nbPlayer, [i,j]))
        
    else:
        k=0
        for i in range(3):
            for j in range(3):
                if grid[i][j]==nbPlayer:
                    k+=1
    return k

def randomize(players):
    n=len(players[0].pond)-1
    for i in players:
        i.pond[:-1]=np.array([random_range*random()-random_range*0.5 for _ in range(n)])

def mutate(players):
    n=len(players)
    k=n//2
    podium(players)
    reset_scores(players)
    players[:k]=create_batch(k)
    for i in range(k):
        players[i].pond=players[-i].pond
        mutation(players[i])


def mutation(player):
    n=len(player.pond)-1
    a=np.array([mut_range*random()-0.5*mut_range for _ in range(n)])
    player.pond[:-1]+=a

def generation(n,N=[]):
    if len(N)==0:
        N=create_batch(n)
        randomize(N)
    dummy_tournament(N)
    mutate(N)
    return N

def dummy_tournament(players,n=100):
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
    
    
a=Player()
b=Player()
main=Game(a,b)
main.last=[0,1]


