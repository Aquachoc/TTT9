# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 15:31:16 2018
@author: PEUSTACHE
"""
from tkinter import *
import numpy as np
from random import random
import time
import math
from copy import deepcopy
MOVE=[-1,-1,-1,-1] #global buffer for the user inputed move
mut_range=6 #scale for genetic mutation 
random_range=10 #range for genetic initialisation

def isWon(grid) : #grid 3*3 return idplayer or -1
    for i in range(3):
        if([grid[i][j] for j in range(3)] in [[1 for j in range (3)], [2 for j in range (3)]]): #check by row
            return grid[i][0] #prendre la couleur du vaiqueur
        if([grid[j][i] for j in range(3)] in [[1 for j in range (3)], [2 for j in range (3)]]): #check by column
            return grid[0][i]
    if([grid[i][i] for i in range(3)] in [[1 for j in range (3)], [2 for j in range (3)]]): #check diag
        return grid[0][0]
    if([grid[-i-1][i] for i in range(3)] in [[1 for j in range (3)], [2 for j in range (3)]]):#check diag
        return grid[0][-1]
    k=0
    for i in range(3): #If the grid is full yet unclaimed
        for j in range(3):
            k+=(grid[i][j]!=0)
    if k==9:
        return -1
    return 0


def gprint(grid): #One-shot print of the grid
    
    root = Tk()
    w = Canvas(root, width=900, height=900)
    w.pack() #Create and display simple screen
    for i in range(1,9): #Basic lines
        if i%3:#check diag
            w.create_line(0,i*100,900,i*100)
            w.create_line(i*100,0,i*100,900)
        else:
            w.create_line(0,i*100,900,i*100, fill = "red", width=5)
            w.create_line(i*100,0,i*100,900, fill = "red", width=5)
    for k in range(3): #print all squares one by one
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
    for i in range(3): #Print the metaSquares
        for j in range(3):
            if metaGrid[i][j]==2:
                bigCircle(w,i,j)
            elif metaGrid[i][j]==1:
                bigCross(w,i,j)
            
    
    root.mainloop() #build the frame
    
            
            
def gridPos(k,i=1,j=1): #simple converter
    return ((50+100*j+(k//3)*300),(50+100*(i%3)+300*(k%3)))

def circle(w,k,l,i,j,r=35,wi=10,d=(5,1)): #draws a circle
    x,y=gridPos(l*3+k,i,j)
    w.create_oval(x-r, y-r, x+r, y+r, outline="blue", width=wi,dash=d)
def cross(w,k,l,i,j,r=35,wi=10,d=(5,1)): #draws a cross
    x,y=gridPos(l*3+k,i,j)
    w.create_line(x-r, y-r, x+r, y+r, fill="green", width=wi, dash=d)
    w.create_line(x-r, y+r, x+r, y-r, fill="green", width=wi,dash=d)

def winLine(w,win,i,j): #draws a line
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
    
def winGrid(grid): #3**4 -> 3*3 metaGrid
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

def vide_check(grid): #9*9
    for i in grid:
        for j in i:
            for k in j:
                for l in k:
                    if l:
                        return False
    return True
def possible(grid, last, mgrid=[]): #return list of 4moves
    if last==[3,3]: #if no restriction
        a=np.where(grid==0) #take all zeroes
        b= list(zip(a[0],a[1],a[2],a[3])) #pack them all together
    else:
        g=np.array(grid[last[0]][last[1]])
        a=np.where(g==0)
        n=len(a[0])
        b=zip(last[0]*np.ones(n,dtype=int),last[1]*np.ones(n,dtype=int),a[0],a[1]) #same here but with case contrain
        b= list(b)
    if len(mgrid)>0: #if a mGrid is provided
        k=0
        flag=vide_check(grid)
        while k<len(b):
            if flag and not([b[k][0],b[k][1]] in [[0,0],[0,1],[1,1]]): #Remove symetrical plays for first play
                del(b[k])
                
            elif mgrid[b[k][0]][b[k][1]]: #If a mSquare is finished remove
                del(b[k])
            else:
                k+=1
    return b #return the list
        
        
def pix_to_case(x,y): #pix to 3**4
    print(x//300,y//300,(x//100)%3,(y//100)%3)
    return(x//300,y//300,(x//100)%3,(y//100)%3)  

def human_move(event): #get move when clicked
    global MOVE
    y,x = event.x, event.y
    MOVE=pix_to_case(x,y)
    print(MOVE)
    
class Game:
    def __init__(self,p1,p2):
        self.p1=p1 #ref the two players
        self.p2=p2
        self.mgrid=np.zeros((3,3),dtype=int) 
        self.grid=np.zeros((3,3,3,3),dtype=int)
        self.winner=0 
        self.actual=1 #actual player
        self.last=[3,3] #3,3 = no constrains
        self.dispo=np.ones((3,3,3,3), dtype=int)
        self.hist=[]   #keep an history
#        self.gagnable=np.ones((2,3,3),dtype=int)
        self.p1.tmpId=1 #sets for the player their order of turn
        self.p2.tmpId=2
        self.p1.gAct=self.p2.gAct=self #creates a ref to the game for the player
        self.turn=-1 #turn count
        self.mHist=np.zeros((3,3),dtype=int)-1 #hist for mGrid
        if self.p1.IA*self.p2.IA: self.auto_play() # plays
        elif self.p1.IA:
            self.versus(self.p2, self.p1)
        else: self.versus(self.p1, self.p2)
        
        
    def move(self,m):
        i,j,k,l=m
        vict=0
        histM=0
        if not self.grid[i][j][k][l]:
            if (self.last==[i,j] or self.last==[3,3]): # and self.grid[i][j][k][l]==0 #checks for coherence
                self.grid[i][j][k][l]=self.actual #places a mark
                self.last=[k,l] #actualises the last move
                histM=isWon(self.grid[i][j]) #checks if the played square is won
                self.mgrid[i][j]=histM
                if histM>0:
                    self.mHist[i][j]=self.turn
                vict=isWon(self.mgrid) #checks for end-game condition
                if vict:
                    self.winner=vict
                    return vict
                if self.mgrid[k][l]: #if plays on a taken square remove constrains
                    self.last=[3,3]
            else :
                print("Coup", m, "invalide`\n") #check for errors

    def get_human_move(self,w,p):
        global MOVE
        flag=False #is MOVE possible ?
        poss = possible(self.grid, self.last, self.mgrid) #creates the move_list
        while not flag: #as long as no acceptable move is inputed
            # print(w.cache)
            time.sleep(0.2)
            w.root.update() #actualise the events queues
            m=MOVE #if user clicked, MOVE has changed
            print(m)
            MOVE=[-1,-1,-1,-1] #regardless, reset move buffer
            print(poss) #debug
            print(m) #debug
            print(m in poss) #debug
            if m in poss: #checks if the given move is acceptable
                flag=True
        return m
    
        
    def hist(self): #invokes the move-by move printer
        gHist(self.hist)

    def versus(self,p,bot): #human vs IA
        global MOVE
        MOVE=[-1,-1,-1,-1] #resets buffer in case
        root=Tk()
        w = Canvas(root, width=900, height=900)
        w.pack()
        w.bind("<Button-1>", human_move)
        w.bind("<Return>", kill_tk)
        w.root=root #allows to call the mainloop more freely
        for i in range(1,9): #basic display structure
            if i%3:
                w.create_line(0,i*100,900,i*100)
                w.create_line(i*100,0,i*100,900)
            else:
                w.create_line(0,i*100,900,i*100, fill = "red", width=5)
                w.create_line(i*100,0,i*100,900, fill = "red", width=5)
        root.update()
        while self.winner==0: #game loop
            self.turn+=1
            time.sleep(0.5) #easier to follow when the AI Plays
            if self.actual==p.tmpId: #different methods for diff types of player
                m=self.get_human_move(w,p)
            else:
                m=bot.move()
            
            if m!=None: #checks for errrors
                self.move(m)
                self.hist.append(m) #plays
                
                if self.actual==1: #displays
                    cross(w, m[0],m[1],m[2],m[3])
                    if self.mHist[m[0]][m[1]]==self.turn:
                        bigCross(w,m[0],m[1])
                else:
                    circle(w, m[0],m[1],m[2],m[3])
                    if self.mHist[m[0]][m[1]]==self.turn:
                        bigCircle(w,m[0],m[1])

                self.actual=1+self.actual%2 #change players
                w.update() #upload display
           
            else:
                o=isWon(self.mgrid) #checks for win
                self.winner=(-1 if o==0 else o)
        time.sleep(4)
        w.root.destroy()        
        if self.winner==1: #scores 
            self.p1.score+=1
            self.p1.wins+=1
        elif self.winner==2:
            self.p2.score+=1
            self.p2.wins+=1
        else:
            self.p1.score+=0.5
            self.p2.score+=0.5
                
                
    def auto_play(self): #see versus above
        while self.winner==0:
            self.turn+=1
#            print(self.turn)
            if self.actual==1:
                m=self.p1.move()
                
            else:
                m=self.p2.move()
            #print(m)
            if m!=None:
                self.move(m)
                self.hist.append(m)
                self.actual=1+self.actual%2
            else:
                o=isWon(self.mgrid)
                self.winner=(-1 if o==0 else o)
                
        if self.winner==1:
            self.p1.score+=1
            self.p1.wins+=1
        elif self.winner==2:
            self.p2.score+=1
            self.p2.wins+=1
        else:
            self.p1.score+=0.5
            self.p2.score+=0.5

def max_play(grid, mgrid, last, pId, pond, depth): #maxplay for the minimax negamax
    if depth==0: #terminaison
        return 0
    poss=possible(grid, last, mgrid) #all moves
    ltmp=[] #buffers for next move grids
    tmp=[]
    mtmp=[]
    res=0
    punaise=0 #rage debug about infinity 
    best=-math.inf #classical initialisation for minimax
    for m in poss:
        i,j,k,l=m 
        mtmp=np.array(mgrid)
        ltmp=last
        if not grid[i][j][k][l]: #if accepatable, play inside the buffer
            if (last==[i,j] or last==[3,3]): # and self.grid[i][j][k][l]==0
                tmp=applyM(grid,m,pId)
                ltmp=[k,l]
                mtmp[i][j]=isWon(tmp[i][j])
                if isWon(mtmp)==pId:
                    return math.inf
                punaise =heurist(grid, mgrid, pond, pId,m)
                if punaise +1 == punaise: #if a move is infinite,do not bother
                    return punaise
                if mtmp[k][l]:
                    ltmp=[3,3]
                    if depth==1:
                        return punaise #easier return
                res=-max_play(tmp, mtmp, ltmp, 1+pId%2, pond, depth-1) +heurist(grid, mgrid, pond, pId,m) #negamax
                if best<res:
                    best=res
    return best

class Player:
    name=0 #name by order of creation
    def __init__(self,pond=[3,2,1,1,1,1,1,1,1,1,1, math.inf],typ="heuri",IA=1):
        self.score=0 
        self.IA=IA
        self.name=Player.name
        Player.name+=1
        self.wins=0
        self.pond=np.array(pond) #heurisitic
        self.tmpId=0
        self.gAct=None
        self.typ=typ
        self.survival=0
    def move1(self,grid,last,mgrid): #random moves
        poss=possible(grid,last,mgrid)
        n=len(poss)
        if not n:
            return None
        k=n*random()
        k=int(k)
        return poss[k]
    
    def move2(self): #heuristic
        poss=possible(self.gAct.grid,self.gAct.last,self.gAct.mgrid)
        i=-math.inf
        n=len(poss)
        M=None
        s=0
        if not n:
            return None
        for m in poss:
            s=self.heurist(m)
            if s>i:
                M=m
                i=s
        return M
    
    def move3(self, depth): #negamax see above
        global FLAG
        grid=np.array(self.gAct.grid)
        mgrid=np.array(self.gAct.mgrid)
        last=self.gAct.last
        ltmp=[]
        poss=possible(self.gAct.grid, self.gAct.last, self.gAct.mgrid)
        #print(len(poss))
        best=-math.inf
        tmp=[]
        mtmp=[]
        res=0
        if len(poss)==0:
            FLAG.append(deepcopy(self))
            print("poss vide")
            return None
        move=poss[0]
        for m in poss:
            i,j,k,l=m
            mtmp=mgrid
            ltmp=last
            if not grid[i][j][k][l]:
                if (last==[i,j] or last==[3,3]): # and self.grid[i][j][k][l]==0
                    tmp=applyM(grid,m,self.tmpId)
                    ltmp=[k,l]
                    mtmp[i][j]=isWon(tmp[i][j])
                    if isWon(mtmp)==self.tmpId:
                        return m
                    if mtmp[k][l]:
                        ltmp=[3,3]
                    o=heurist(grid, mgrid,self.pond,self.tmpId,m)
                    if o==math.inf:
                        return m
                    res=-max_play(tmp, mtmp, ltmp, 1+self.tmpId%2, self.pond, depth-1)+o
                    if best<res:
                        move=m
                        best=res
                else :
                    print("Coup", m, "invalide`\n")
        return move
    
    
    def move(self): #generic move function
        
        if self.typ=="dummy":
            return self.move1(self.gAct.grid, self.gAct.last, self.gAct.mgrid)
        if self.typ=="heuri":
            return self.move2()
        return self.move3(4)

    
    def indicateurs(self,m): #computes flags vector for the heuristic
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
        # the center ? a corner ? a border ? do I have pawns in newt square ? does he ? is it giving him a free move ? Will he play a square he can win ? anybody can win ? Do I block him ? Do I capture ? Do I win ?
    def heurist(self,m): #basically scalar product of "indicateurs" by their weight
        flags=np.array(self.indicateurs(m))
        if not flags[-1]:
            score=sum(flags[:-1]*self.pond[:-1])
        else:
            score=sum(flags*self.pond)
        return score
    
def conti(event): #next step for history print
    n=len(event.widget.g.hist)
    c=event.widget.count
    if c%2==1 and 0<c<=n:
        h=event.widget.g.hist[c-1] #creates a pawn and store it in the canvas for future implementation of a backward procedure
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
def gHist(game): #play by play move
        root = Tk() #creates frame
        w = Canvas(root, width=900, height=900)
        w.pack()
        w.tmp=[]
        w.mTmp=[]
        w.count=1
        w.g=game
        w.root=root
        w.bind("<Button-1>", conti) #binds click to next move
       # w.bind("<Button-3>", prev)
        for i in range(1,9):
            if i%3:
                w.create_line(0,i*100,900,i*100)
                w.create_line(i*100,0,i*100,900)
            else:
                w.create_line(0,i*100,900,i*100, fill = "red", width=5)
                w.create_line(i*100,0,i*100,900, fill = "red", width=5)
        root.mainloop()  
        print(len(w.tmp)) #debug
            
#def prev(event):
#    n=len(event.widget.g.hist)
#    c=event.widget.count
#    if n>0:
#        event.widget.count-=1
#        if event.widget.mTmp[-1]!=None:
#            event.widget.delete(event.widget.mTmp[-1])
#            del(event.widget.mTmp[-1])
#        event.widget.delete(event.widget.tmp[-1])
#        del(event.widget.tmp[-1])
#    event.widget.root.update()
#    return 1

def create_batch(n): #creates a new generation
    L=[]
    for i in range(n):
        L.append(Player())
    return L
            
def score_ext(player): #gives score
    return player.score

        
def reset_scores(players): #reset stats for a list of Player instances
    for i in players:
        i.score=0
        i.wins=0

def recap(players): #gives a recap of a list
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
                Game(players[i],players[j])
                del(main)
                c+=1
                print('{0:4f}'.format(c/tot))
    else:
        dummy_tournament(players)
            
def kill_tk(event): #tool to kill canvas
    print("killed")
    event.widget.root.destroy()
               
def podium(players): #self explainatory
    players.sort(key=score_ext)

def winnable(grid,player=0): #0=both players
    if player :    #winnable by a player = if all blacks are the players' he has won
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

def corner_flag(m): #is the play in a corner ?
    return((m in [[0,2],[2,0],[0,0],[2,2]]))

def border_flag(m): #is the play in a border ?
    return((m in [[0,1],[1,0],[2,1],[1,2]]))

def center_flag(m): #is the play in the center
    return (m == [1,1])

def nbPions(grid, nbPlayer, m=[]): #how many pawns already in the targer square
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

def randomize(players): #randomizes the ponderation of a Players generation
    n=len(players[0].pond)-1
    for i in players:
        i.pond[:-1]=np.array([random_range*random()-random_range*0.5 for _ in range(n)])

def mutate(players): #mutation step
    n=len(players)
    k=n//2
    podium(players) #sorts the players
    reset_scores(players) #reset them
    p=[]
    m=[]
    for i in range(k): #we only keep the best half
        p=players[-i-1].pond
        m=mutation(p)
        players[i]=Player(pond=p+m) #mutated baby
        #players[-i].survival+=1


def mutation(pond): #returns a random mutation. the argument is used to determine the right size
    n=len(pond)
    a=np.array([mut_range*random()-0.5*mut_range for _ in range(n)])
    return a

def generation(n=30,N=[],nb=100): #creates a generation, or a 1 generation period
    if len(N)==0:
        N=create_batch(n)
        randomize(N)
    dummy_tournament(N,nb) #compares AI
    mutate(N) #mutates them
    return N 

def dummy_tournament(players,n=60): #makes all the players play n games against the random AI, taking turns beginning
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

def recap_pond(players): #recap ponderations
    for i in players:
        print(i.pond)

def applyM(grid,move,playerId): #return the grid is m is played
    a=deepcopy(grid)
    if len(move)>2:
        a[move[0]][move[1]][move[2]][move[3]]=playerId
    else :
        a[move[0]][move[1]]=playerId
    return a

def indicateurs(grid,mgrid,playerId,m): #non class equivalent for minimax convenience
        k=m[0:2]
        m=m[2:]
        tmp=np.array(grid)
        tmp[k[0]][k[1]][m[0]][m[1]]=playerId
        won=isWon(tmp[k[0]][k[1]])
        adv_winnable=winnable(tmp[k[0]][k[1]], 1+playerId%2)
        mGrid=winGrid(tmp)
        capture=(mGrid[k[0]][k[1]]==playerId)*1
        victory=isWon(mGrid)
        return[1*center_flag(m), 1*corner_flag(m), 1*border_flag(m),  nbPions(grid[m[0]][m[1]],playerId,m), nbPions(grid[m[0]][m[1]], 1+(playerId%2), m), 1*(mgrid[m[0]][m[1]]!=0), 1*winnable(grid[m[0]][m[1]]), int(winnable(grid[m[0]][m[1]], 1+playerId%2)),won, int(adv_winnable), capture, victory]
    
def heurist(grid,mgrid,pond,playerId,m): #non class equivalent for minimax convenience
        flags=np.array(indicateurs(grid,mgrid,playerId,m))
        if not flags[-1]:
            score=sum(flags[:-1]*pond[:-1])
        else:
            score=sum(flags*pond)
        return score    


def training(nb, gen, nb_games):
    A=[]
    for _ in range(gen):
        A=generation(nb,A, nb_games)
    return A
    
a=Player(pond = [ -0.99403255, -28.00149821,  37.97525959,  -6.9197625 ,
       -16.63066428,  -8.17460181,  -2.63418722, -29.41853052,
        43.87076219,   4.6322527 ,   6.23818578,          math.inf], typ="heuri")
b=Player(IA=0)
main=Game(a,b)
#b=Player(pond=a.pond, typ="euri")
#d=Player(pond=a.pond, typ="euri")
#f=Player(typ="dummy")
#w=0
#for _ in range(200):
#    main=Game(f,a)
#    if main.winner==2:
#        w+=1
#    print(_)
#c=Player()
#main=Game(c,b)
#b=Player()
#main=Game(a,b)
#main.last=[0,1]


