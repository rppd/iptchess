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
from copy import deepcopy
import time


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
        
    def vider_case(self, cx, cy):
        self.board_mat[cx][cy].set_data([[[0,0,0,0]]])
    
    def vider(self):
        for x in range(self.n):
            for y in range(self.n):
                self.vider_case(x, y)
    
    def clear_highlight(self):
        for x in range(8):
            for y in range(8):
                self.bg_mat[x][y].set_data([[[255,255,255]]])

    def draw_pion(self, p):
        """Affiche le pion sur la grille"""
        self.board_mat[p.x][p.y].set_data(p.img)

class Action:
    def __init__(self, p, x, y, plateau, joueur):
        self.p = p
        self.x = x
        self.y = y
        self.plateau = plateau.get_copy() #Etat du plateau après l'action
        plateau.bouger_pion(p, x, y)
        self.joueur = joueur
        self.score = 0 #Pour comparer les actions entre elles
        """
        roi_joueur = False
        roi_oppose = False
        for p in plateau.pions:
            if p.type=="p":
                value = 1
            elif p.type=="c" or p.type=="f":
                value = 3
            elif p.type=="t":
                value=5
            elif p.type=="q":
                value=9
            elif p.type=="k":
                if p.color == joueur:
                    roi_joueur = True
                else:
                    roi_oppose = True
            self.score += value
        if not roi_oppose:
            self.score = 100
        if not roi_joueur:
            self.score = -100
        """

    def next_rec(self, n):
        self.next_actions = self.plateau.get_actions(self.joueur)
        if n > 0:
            for a in self.next_actions:
                a.next_rec(n-1)
    
    def get_rec(self):
        if self.next_actions != None:
            arr = []
            for a in self.actions:
                arr.append(a.get_rec())
            return arr
        else:
            return self

class Pion:
    """Représente chaque pion : position, type et couleur"""
    def __init__(self, x, y, type, color):
        self.x = x
        self.y = y
        self.type = type
        if self.type == "p":
            self.moved = False
        self.color = color
        
        if color == "b": #Si pion noir
            si = 0 #Sprite index
        else:
            si = 6
        si += "pcftqk".find(self.type)
        self.img=sprites[si]
    
    def get_mvts(self, plateau):
        """Donne tous les mouvements possibles du pion sur le plateau"""
        if self.type == "p": #Pion
            if self.color == "w":
                diags = [[self.x-1, self.y+1],[self.x+1, self.y+1]] #Mouvements possibles de diagonales
                faces = [[self.x, self.y+1]] #Mouvements possibles de face
                if not self.moved: #Si le pion n'a pas encore bougé de la partie
                    faces.append([self.x, self.y+2])
            else:
                diags = [[self.x-1, self.y-1], [self.x+1, self.y-1]]
                faces = [[self.x, self.y-1]] #Mouvements possibles de 
                if not self.moved:
                    faces.append([self.x, self.y-2])
            pos = [] #Position de déplacement validées
            for d in diags:
                if verif_case(d[0], d[1]): #Si la case est sur le plateau 
                    pion = plateau.get_pion(d[0],d[1])
                    if pion != None and pion.color != self.color: #Si il y a un pion ennemi
                        pos.append(d)
            for f in faces: 
                if verif_case(f[0],f[1]):
                    pion = plateau.get_pion(f[0], f[1])
                    if pion == None: #Si il n'y a pas de pion
                        pos.append(f)
            return pos
        elif self.type == "t": #Tour
            pos = []
            dir = [[1,0],[-1,0],[0,1],[0,-1]] #4 directions possibles
            for d in dir:
                x,y = self.x+d[0],self.y+d[1] #Projection de position
                while verif_case(x,y): #Tant que (x, y) est sur le plateau
                    pion = plateau.get_pion(x, y)
                    if pion != None: #Si il y a un pion
                        if pion.color != self.color: #Si il n'est pas allié
                            pos.append([x,y])
                        break
                    pos.append([x,y])
                    x += d[0]
                    y += d[1]
            return pos
        elif self.type == "c": #Cavalier
            l = [-2,-1,1,2]
            mvts = [[x,y] for x in l for y in l if abs(x)!=abs(y)]
            pos = []
            for m in mvts:
                x = self.x + m[0]
                y = self.y + m[1]
                if verif_case(x,y):
                    pion = plateau.get_pion(x, y)
                    if pion == None or pion.color != self.color:
                        pos.append([x, y])
            return pos
        elif self.type == "f": #Fou
            dir = [[1,1],[-1,1],[-1,-1],[1,-1]]
            pos = []
            for d in dir:
                x,y = self.x+d[0],self.y+d[1]
                while verif_case(x,y):
                    pion = plateau.get_pion(x, y)
                    if pion != None:
                        if pion.color != self.color:
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
                if verif_case(x, y):
                    pion = plateau.get_pion(x, y)
                    if pion == None or pion.color != self.color:
                        pos.append([self.x + m[0], self.y + m[1]])
            return pos
        elif self.type == "q": #Dame
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
        self.pionsliste = []
        for x in range(8):
            self.pions.append([])
            for y in range(8):
                self.pions[x].append(None)
        for i in range(8):
            self.add_pion(Pion(i,0,backrow[i],"w"))
            self.add_pion(Pion(i,7,backrow[i],"b"))
            self.add_pion(Pion(i,1,"p","w"))
            self.add_pion(Pion(i,6,"p","b"))
    
    def draw(self, grille):
        """Affiche tous les pions"""
        grille.clear_highlight()
        for x in range(8):
            for y in range(8):
                self.draw_c(x, y, grille)
            
    def draw_c(self, cx, cy, grille):
        """Affiche le pion situé sur la case donnée"""
        p = self.get_pion(cx, cy)
        if p != None:
            grille.draw_pion(p)
        else:
            grille.vider_case(cx, cy)
 
    def get_pion(self, cx, cy):
        """Retourne l'objet Pion situé sur la case"""
        return self.pions[cx][cy]
    
    def bouger_pion(self, p1, x2, y2):
        """Déplace le pion p1 vers (x2, y2), supprime éventuellement un pion adverse"""
        global game_ended
        p2 = self.get_pion(x2, y2)
        if p2 != None:
            i = self.pionsliste.index(p2)
            self.pionsliste.pop(i)
            if p2.type == "k":
                game_ended = True
        self.pions[x2][y2] = p1
        self.pions[p1.x][p1.y] = None
        p1.x = x2
        p1.y = y2
        if p1.type == "p":
            p1.moved = True
        
    def get_actions(self, joueur):
        """Donne toutes les actions possibles pour le joueur sur le plateau"""
        actions = []
        if joueur == "w":
            j2 = "b"
        else:
            j2 = "w"
        for p in self.pionsliste:
            start = time.time()
            if p.color == joueur:
                mvts = p.get_mvts(self)
                for m in mvts:
                    actions.append(Action(p, m[0], m[1], self.get_copy(), j2))
            print(p.type, "{:.4f}".format(time.time()-start), len(mvts), len(actions))
        return actions
        
    def get_copy(self):
        copy = Plateau()
        copy.pions = deepcopy(self.pions)
        return copy
    
    def add_pion(self, p):
        """Ajoute un pion au plateau"""
        self.pions[p.x][p.y] = p
        self.pionsliste.append(p)
    
    def disp(self):
        print("-------------------")
        for x in range(8):
            line = ""
            for y in range(8):
                p = self.pions[x][y]
                if p == None:
                    line += "n "
                else:
                    line += p.type+" "
            print(line)
                    

class Selection:
    def __init__(self, cx, cy, plateau):
        self.x = cx
        self.y = cy
        self.p = None
        self.mvts = []
        if self.x != None and self.y != None:
            self.p = plateau.get_pion(cx, cy)
            if self.p != None:
                self.mvts = self.p.get_mvts(plateau)
    
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
    if game_ended:
        plt.close()
        exit
    global sel #pas le choix
    cx, cy = grille.get_case(event.xdata, event.ydata)
    sel = update_selection(cx, cy)
    sel.draw(grille)

def update_selection(cx=None, cy=None):
    global joueur
    """Efface le surlignage de la sélection et affiche la nouvelle en fonction de la case sur laquelle on clique. Retourne un objet Selection pour être stocké dans la variable globale selection"""
    grille.clear_highlight()
    new = Selection(cx, cy, plateau)
    if new.p != None: #Si il y a un pion sur la case cliqué
        if new.p.color == joueur: #Si il est allié
            if new.p != sel.p: #Si il est pas déjà sélectionné
                return new #Nouvelle sélection
            else:
                return Selection(None, None, plateau) #Déselectionne
    if [cx, cy] in sel.mvts: #Si la case cliquée est dans les mouvements possibles 
        plateau.bouger_pion(sel.p, cx, cy)
        if joueur == "w":
            joueur = "b"
        else:
            joueur = "w"
        return Selection(None, None, plateau ) #Déselectionne
    plateau.draw(grille)
    return sel
    
def get_actions_rec(plateau, joueur, n):
    actions_plateau = plateau.get_actions(joueur)
    actions_rec = []
    if joueur == "w":
        joueur == "b"
    else:
        joueur == "w"
    for a in actions_plateau:
        actions_rec.append(get_actions_rec(a.plateau, joueur, n-1))
    if n == 1:
        return actions_rec
    
def verif_case(x, y):
    return x >= 0 and x < 8 and y >= 0 and y < 8


def printdelta(start, label):
    print(label, "{:.4f}".format(time.time()-start))

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
sel = Selection(None, None, plateau)
game_ended = False





