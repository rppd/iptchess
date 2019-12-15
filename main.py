from matplotlib import pyplot as plt
from matplotlib import patches
from matplotlib import image as mimg
from os import chdir
from time import time

class Grille:
    """Intermédiaire entre coordonnées par pixels et cases"""
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
    
    def get_pixels(self,cx, cy):
        """Position d'une case sur l'écran"""
        px = self.x + self.w*cx
        py = self.y + self.h*cy
        return [px, py, px+self.w, py+self.h]

class Pion:
    """Représente chaque pion : position et type"""
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
    
    def draw(self, grille):
        """Affiche le pion sur la grille"""
        image_grille(self.img,self.x, self.y)

def rect(x1, y1, x2, y2, ax, ec="k", fc="none"):
    ax.add_patch(patches.Rectangle((x1,y1),x2-x1,y2-y1,ec=ec,fc=fc));
    plt.show()
    
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
    if typeof(event.xdata)=="NoneType" | typeof(event.ydata)=="NoneType":
        selection = None
    cx, cy = grille.get_case(event.xdata, event.ydata)
    xy = grille.get_pixels(cx, cy)
    selection = [cx, cy]
    rect(xy[0], xy[1], xy[2], xy[3], ax, fc="b")
    plt.draw()

sprites = load_sprites()

fig, ax = plt.subplots()
plt.axis([0,100,0,100])
fig.canvas.mpl_connect("button_press_event", onclick)

grille = new_grille(10,10,90,90,8,ax)
plt.show()

selection = None
pions = []

for x in range(8):
    for y in range(8):
        image_grille(sprites[(x+y)%12],x,y,grille)
        plt.draw()
        plt.pause(0.05)





