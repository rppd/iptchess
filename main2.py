#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 23:10:40 2019

@author: robin
"""

from matplotlib import pyplot as plt
from matplotlib import patches
from matplotlib import image as mimg
from os import chdir

class Grille:
    """Intermédiaire entre coordonnées par pixels et par cases"""
    def __init__(self, x1, y1, x2, y2, n):
        self.x = x1
        self.y = y1
        self.w = (x2-x1)/n
        self.h = (y2-y1)/n
    
    def get_case(self,px,py):
        """Case contenant une position sur l'écran"""
        cx = (px - self.x)//self.w
        cy = (py - self.y)//self.h
        return [cx, cy]
    
    def get_pixels(self,cx,cy):
        """Position d'une case sur l'écran"""
        px = self.x + self.w*cx
        py = self.y + self.h*cy
        return [px, py, px+self.w, py+self.h]
    
    def remplir_case(self, cx, cy, color=[0,0,0]):
        if color == "k":
            color=[0,0,0]
        elif color == "r":
            color=[255,0,0]
        elif color == "g":
            color=[0,255,0]
        elif color == "b":
            color=[0,0,255]
        elif color == "w":
            color=[255,255,255]
        img = [[color]*int(self.w)]*int(self.h)
        image_grille(img, cx, cy, self)

class Pion:
    """Représente chaque pion : position, type et couleur"""
    def __init__(self, x, y, type, color):
        self.x = x
        self.y = y
        self.type = type
        self.color = color
        
        if color == "w":
            si = 0 #Sprite index
        else:
            si = 6
        si += "pcftqk".find(self.type)
        self.img=sprites[si]
    
    def get_mvts(self):
        if self.type == "p":
            if self.color == "w":
                return [[self.x, self.y+1]]
            else:
                return [[self.x, self.y-1]]
        elif self.type == "t":
            pos = []
            dir = [[1,0],[-1,0],[0,1],[0,-1]]
            for d in dir:
                x,y = self.x+d[0],self.y+d[1]
                while verif_case(x,y):
                    pos.append([x,y])
                    x += d[0]
                    y += d[1]    
            return pos
        elif self.type == "c":
            l = [-2,-1,1,2]
            mvts = [[x,y] for x in l for y in l if abs(x)!=abs(y)]
            pos = []
            for m in mvts:
                if verif_case(self.x + m[0], self.y + m[1]):
                    pos.append([self.x + m[0], self.y + m[1]])
            return pos
        elif self.type == "f":
            dir = [[1,1],[-1,1],[-1,-1],[1,-1]]
            pos = []
            for d in dir:
                x,y = self.x+d[0],self.y+d[1]
                while verif_case(x,y):
                    pos.append([x,y])
                    x += d[0]
                    y += d[1] 
            return pos
        elif self.type == "k":
            mvts = [[1,0],[0,1],[-1,0],[-1,0]]
            pos = []
            for m in mvts:
                if verif_case(self.x + m[0], self.y + m[1]):
                    pos.append([self.x + m[0], self.y + m[1]])
            return pos
        elif self.type  == "q":
            pos = []
            dir = [[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1],[0,1],[1,1]]
            for d in dir:
                x,y = self.x+d[0],self.y+d[1]
                while verif_case(x,y):
                    pos.append([x,y])
                    x += d[0]
                    y += d[1]    
            return pos
            
    def draw(self, grille):
        """Affiche le pion sur la grille"""
        print(self.type, self.x, self.y)
        image_grille(self.img,self.x, self.y, grille)
        
class Plateau:
    def __init__(self):
        self.pions = []
        for i in range(8):
            self.pions.append(Pion(i,0,backrow[i],"w"))
            self.pions.append(Pion(i,7,backrow[i],"b"))
            self.pions.append(Pion(i,1,"p","w"))
            self.pions.append(Pion(i,6,"p","b"))
    
    def draw(self, grille):
        """Affiche tous les pions"""
        for p in self.pions:
            p.draw(grille)
            
    def draw_c(self, cx, cy, grille):
        """Affiche le pion sur la case donnée"""
        p = self.get_pion(cx, cy)
        if p != None:
            p.draw(grille)
     
    def draw_mvts(self, cx, cy, grille):
        pion = self.get_pion(cx, cy)
        if pion == None:
            return
        pos = pion.get_mvts()
        print(pos)
        for p in pos:
            if self.get_pion(p[0], p[1]) == None:
                grille.remplir_case(p[0], p[1], "g")
            
            
    def get_pion(self, cx, cy):
        for p in self.pions:
            if p.x == cx and p.y == cy:
                return p
        return None

def rect(x1, y1, x2, y2, ax, ec="k", fc="none"):
    ax.add_patch(patches.Rectangle((x1,y1),x2-x1,y2-y1,ec=ec,fc=fc));
    
def new_grille(x1,y1,x2,y2,n,ax):
    """Affiche une grille avec les paramètres donnés et les stocke dans un objet grille"""
    w = (x2-x1)/n
    h = (y2-y1)/n
    x = x1
    y = y1
    for i in range(n):
        rect(x1,y1,x,y,ax,"k","none")
        rect(x,y,x2,y2,ax,"k","none")
        x += w
        y += h
    return Grille(x1,y1,x2,y2,n)
        
def image(img, x1, y1, x2, y2):
    """Affiche une image dans le rectangle donné"""
    plt.imshow(img, extent=[x1,x2,y1,y2])

def image_grille(img, x, y, grille):
    """Affiche une image dans la case désignée"""
    x1 = grille.x+x*grille.w
    y1 = grille.y+y*grille.h
    image(img,x1,y1,x1+grille.w,y1+grille.h)
        
def load_sprites(dir="/home/robin/workspace/python/ipt/chess/sprites"):
    """Charge tous les sprites dans une liste"""
    arr = []
    chdir(dir)
    for i in range(12):
        img = mimg.imread("sprite_"+"{:0>2d}".format(i)+".png")
        arr.append(img)
    return arr

def onclick(event):
    """Quand le joueur clique sur l'écran"""
    global cs #pas le choix
    cx, cy = grille.get_case(event.xdata, event.ydata)
    cs = update_selection(cx, cy)

def update_selection(cx=None, cy=None):
    if cx == None or cy==None:
        return cs
    grille.remplir_case(cs[0], cs[1], "w")
    for p in plateau.pions:
        if p.x == cs[0] and p.y == cs[1]:
            plateau.draw_c(p.x, p.y, grille)
    grille.remplir_case(cx, cy, "b")
    plateau.draw_c(cx, cy, grille)
    plateau.draw_mvts(cx, cy, grille)
    return [cx, cy]
    
def verif_case(x, y):
    return x >= 0 and x < 8 and y >= 0 and y < 8

sprites = load_sprites()

fig, ax = plt.subplots()
plt.axis([0,100,0,100])
fig.canvas.mpl_connect("button_press_event", onclick)

grille = new_grille(10,10,90,90,8,ax)
cs = [0,0]
backrow = "tcfkqfct"
plateau = Plateau()
plateau.draw(grille)





