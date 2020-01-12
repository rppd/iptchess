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
        self.bg_mat = []
        self.board_mat = []
        background = [[[255,255,255]]]
        transparent = [[[0,0,0,0]]]
        for x in range(8):
            self.bg_mat.append([])
            self.board_mat.append([])
            for y in range(8): 
                rect = self.get_pixels(x,y)
                self.bg_mat[x].append(image(background, rect[0], rect[1], rect[2], rect[3]))
                self.board_mat[x].append(image(transparent, rect[0], rect[1], rect[2], rect[3]))
        
    def get_case(self,px,py):
        """Case contenant une position sur l'écran"""
        cx = (px - self.x)//self.w
        cy = (py - self.y)//self.h
        return [int(cx), int(cy)]
    
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
        self.bg_mat[cx][cy].set_data(img)
        fig.canvas.draw()
        
    def vider_case(self, cx, cy):
        self.board_mat[cx][cy].set_data([[[0,0,0,0]]])
        fig.canvas.draw()
        
    def clear_highlight(self):
        for x in range(8):
            for y in range(8):
                self.bg_mat[x][y].set_data([[[255,255,255]]])
        fig.canvas.draw()

    def draw_pion(self, p):
        """Affiche le pion sur la grille"""
        print("Drawing a {} on ({};{})".format(p.type, p.x, p.y))
        self.board_mat[p.x][p.y].set_data(p.img)

class Pion:
    """Représente chaque pion : position, type et couleur"""
    def __init__(self, x, y, type, color):
        self.x = x
        self.y = y
        self.type = type
        self.color = color
        
        if color == "b": #Si pion noir
            si = 0 #Sprite index
        else:
            si = 6
        si += "pcftqk".find(self.type)
        self.img=sprites[si]
    
    def get_mvts(self, plateau, joueur):
        if self.type == "p":
            if self.color == "w":
                pos = [self.x, self.y+1]
            else:
                pos = [self.x, self.y-1]
            pion = plateau.get_pion(pos[0], pos[1])
            if pion == None or pion.color != joueur:
                return [pos]
            else:
                return []
        elif self.type == "t": #Tour
            pos = []
            dir = [[1,0],[-1,0],[0,1],[0,-1]] #4 directions possibles
            for d in dir:
                x,y = self.x+d[0],self.y+d[1]
                while verif_case(x,y):
                    pion = plateau.get_pion(x, y)
                    if pion != None: #Si il y a un pion
                        if pion.color != joueur: #Si il n'est pas allié
                            pos.append([x,y])
                        break
                    pos.append([x,y])
                    x += d[0]
                    y += d[1]
            return pos
        elif self.type == "c":
            l = [-2,-1,1,2]
            mvts = [[x,y] for x in l for y in l if abs(x)!=abs(y)]
            pos = []
            for m in mvts:
                x = self.x + m[0]
                y = self.y + m[1]
                if verif_case(x,y):
                    pion = plateau.get_pion(x, y)
                    if pion == None or pion.color != joueur:
                        pos.append(x, y)
            return pos
        elif self.type == "f":
            dir = [[1,1],[-1,1],[-1,-1],[1,-1]]
            pos = []
            for d in dir:
                x,y = self.x+d[0],self.y+d[1]
                while verif_case(x,y):
                    pion = plateau.get_pion(x, y)
                    if pion != None:
                        if pion.color != joueur:
                            pos.append([x,y])
                        break
                    pos.append([x,y])
                    x += d[0]
                    y += d[1]
            return pos
        elif self.type == "k": #Roi
            mvts = [[1,0],[-1,1],[0,-1],[-1,-1],[-1,0],[-1,1],[0,1],[1,1]] #4 mouvements possibles
            pos = []
            for m in mvts:
                x = self.x + m[0]
                y = self.y + m[1]
                if verif_case(x, y): #Si la case est dans les limites
                    pion = plateau.get_pion(x, y)
                    if pion == None or pion.color != joueur: #Si il n'y a pas de pion allié
                        pos.append([self.x + m[0], self.y + m[1]])
            return pos
        elif self.type == "q":
            pos = []
            dir = [[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1],[0,1],[1,1]]
            for d in dir:
                x,y = self.x+d[0],self.y+d[1]
                while verif_case(x,y):
                    pion = plateau.get_pion(x, y)
                    if pion != None:
                        if pion.color != joueur:
                            pos.append([x,y])
                        break
                    pos.append([x,y])
                    x += d[0]
                    y += d[1]
            return pos
        
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
            grille.draw_pion(p)
            
    def draw_c(self, cx, cy, grille):
        """Affiche le pion situé sur la case donnée"""
        p = self.get_pion(cx, cy)
        if p != None:
            grille.draw_pion(p)
     
    def get_pion(self, cx, cy):
        """Retourne l'objet Pion situé sur la case"""
        for p in self.pions:
            if p.x == cx and p.y == cy:
                return p
        return None
    
    def bouger_pion(self, p1, x2, y2):
        p2 = self.get_pion(x2, y2)
        if p2 != None:
            i = self.pions.index(p2)
            self.pions.pop(i)
            if p2.type == "k":
                #                   WIN
        grille.vider_case(p1.x, p1.y)
        p1.x = x2
        p1.y = y2
        grille.draw_pion(p1)
        fig.canvas.draw()

class Selection:
    def __init__(self, cx, cy, plateau, joueur):
        self.x = cx
        self.y = cy
        self.p = None
        self.mvts = []
        if self.x != None and self.y != None:
            self.p = plateau.get_pion(cx, cy)
            if self.p != None:
                self.mvts = self.p.get_mvts(plateau, joueur)
    
    def exists(self):
         return self.x != None and self.y != None
     
    def draw(self, grille):
        if not self.exists():
            return
        grille.remplir_case(self.x, self.y, "b")
        for pos in self.mvts:
            grille.remplir_case(pos[0], pos[1], "g")

def rect(x1, y1, x2, y2, ax, ec="k", fc="none"):
    ax.add_patch(patches.Rectangle((x1,y1),x2-x1,y2-y1,ec=ec,fc=fc));
    
def new_grille(x1,y1,x2,y2,n):
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
    return plt.imshow(img, extent=[x1,x2,y1,y2])

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
    global sel #pas le choix
    cx, cy = grille.get_case(event.xdata, event.ydata)
    sel = update_selection(cx, cy)
    sel.draw(grille)

def update_selection(cx=None, cy=None):
    global joueur
    """Efface le surlignage de la sélection et affiche la nouvelle en fonction de la case sur laquelle on clique. Retourne un objet Selection pour être stocké dans la variable globale selection"""
    grille.clear_highlight()
    new = Selection(cx, cy, plateau, joueur)
    if new.p != None: #Si il y a un pion sur la case cliqué
        if new.p.color == joueur: #Si il est allié
            if new.p != sel.p: #Si il est pas déjà sélectionné
                return new #Nouvelle sélection
            else:
                return Selection(None, None, plateau, joueur) #Déselectionne
    if [cx, cy] in sel.mvts: #Si la case cliquée est dans les mouvements possibles 
        plateau.bouger_pion(sel.p, cx, cy)
        if joueur == "w":
            joueur = "b"
        else:
            joueur = "w"
        return Selection(None, None, plateau, joueur) #Déselectionne
    return sel
    
    
def verif_case(x, y):
    return x >= 0 and x < 8 and y >= 0 and y < 8

sprites = load_sprites()

fig, ax = plt.subplots()
plt.axis([0,100,0,100])
fig.canvas.mpl_connect("button_press_event", onclick)

grille = new_grille(10,10,90,90,8)
backrow = "tcfkqfct"
plateau = Plateau()
plateau.draw(grille)
plt.show()

joueur = "w"
sel = Selection(None, None, plateau, joueur)





