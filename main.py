from pygame import Surface, Vector2, Rect, Color
from graphics import *
from typing import List, Tuple, overload
import math
import random
import time

Coord = Tuple[int, int]
Pixel = Tuple[int, int]
Couleur = Tuple[int, int, int]

EMPTY_COLOR = (0, 0, 0)
AVAILABLE_COLOR : List[Color] = [
    #Bleu,            Violet,           Magenta,          Rouge,            Orange,           Jaune,            Vert,             Vert foncée,      Noir        et    Blanc
    Color("#0000dd"), Color("#8800dd"), Color("#dd00dd"), Color("#dd0000"), Color("#dd8800"), Color("#00dd00"), Color("#005500"), Color("#000000"), Color("#d0d0d0")
]


TAILLE_FENETRE = (1152,648)
TAILLE_CASE = 40
TAILLE_TERRAIN = (TAILLE_FENETRE[0]//TAILLE_CASE, TAILLE_FENETRE[1]//TAILLE_CASE)

def grille_vers_fenetre(i,j):
    x = i * TAILLE_CASE
    y = j * TAILLE_CASE
    return (x,y)

def fenetre_vers_grille(x,y):
    i = y // TAILLE_CASE
    j = x // TAILLE_CASE
    return (i,j)

def add_coord(coord1 : Coord, coord2 : Coord) -> Coord:
    return (coord1[0] + coord2[0], coord1[1] + coord2[1])

def clampf(v : float, minv : float, maxv : float):
    return min(max(v,minv),maxv)

def get_rgb(color : Color) -> Couleur:
    return (color.r, color.g, color.b)


def lerpf(v1 : float, v2 : float, w : float) -> float:
    return (v1 + ((v2-v1)*w))

def lerpi(i1 : int, i2 : int, w : float) -> int:
    return int(i1 + ((i2-i1)*w))

def lerp_color(color1 : Couleur, color2 : Couleur, w : float) -> Color:
    if color1 is pygame.Color and color1 is pygame.Color:
        color1 = get_rgb(color1)
        color2 = get_rgb(color2)
    
    r = lerpi(color1[0], color2[0], w)
    g = lerpi(color1[1], color2[1], w)
    b = lerpi(color1[2], color2[2], w)    
    return Color(r,g,b)

def addt(t1 : Tuple[float], t2 : Tuple[float]) -> Tuple[float]:
    assert len(t1) == len(t2), "Les tuples doivent avoir la mâme taille"
    return [t1[i] + t2[i] for i in range(len(t1))]

class Drawing:

    """Rectangle"""
    def __init__(self, rect : Rect, color : Couleur, width : int = 1):
        self.type : str = "rect"
        self.rect = rect
        self.color = color
        self.width = width

    """Circle"""
    def __init__(self, center : Coord, radius_horizontal : int, radius_vertical : int, color : Couleur, width : int = 1):
        self.type : str
        self.color = color
        self.radiuses = (radius_horizontal, radius_vertical)
        self.width = width

    """Line"""
    def __init__(self, start : Coord, end : Coord, color : Couleur, width : int = 1):
        self.type : str
        self.color = color
        self.width = width

    def draw(self, surf) -> Surface:
        if not hasattr(self,"type"):
            raise NotImplementedError("Type de dessin non implémenté")
        if self.type == "rect":
            if self.width <= 0:
                affiche_rectangle_plein(self.start, self.end, self.color, surf)
            else:
                affiche_rectangle(self.start, self.end, self.color, self.width, surf)
        elif self.type == "circle":
            if self.width <= 0:
                affiche_ellipse_plein(self.center, self.radiuses, self.color, surf)
            else:
                affiche_ellipse(self.center, self.radiuses, self.color, self.width, surf)
        elif self.type == "line":
            affiche_ligne(self.start, self.end, self.color, max(self.width,1), surf)

class Canvas(Surface):

    def __init__(self, taille : Coord):
        super().__init__(taille, pygame.SRCALPHA)
        self.draw_history : List[Drawing] = []

    def refresh(self):
        affiche_rectangle_plein((0,0), self.get_size(), blanc, self)
        for drawing in self.draw_history:
            drawing.draw(self)

    def draw_shape(self, drawing : Drawing):
        self.draw_history.append(drawing)
        self.refresh()

    def rewind(self, step : int = 1):
        for i in range(len(self.draw_history), max(len(self.draw_history) - step ,-1), -1):
            pass

class Interface:

    def __init__(self, size : Coord):
        init_fenetre(size[0], size[1], "Ctrl Paint")
        self.size = size
        self.choosen_color = noir
        self.canvas = Canvas(size)

    def draw_background(self, offset : Coord = (0,0)):
        color1 = Color("#388CA5")
        color2 = Color("#38AAB9")
        for x in range(0, self.size[0], TAILLE_CASE):
            for y in range(0, self.size[1], TAILLE_CASE):
                affiche_rectangle_plein(addt(offset,(x,y)), addt(offset,(x+TAILLE_CASE,y+TAILLE_CASE)), color1 if (x+y) % 80 == 0 else color2)

    def draw_interface_color(self):
        offset : Coord = (10,10)
        fade_scale = 0.4
        for x in range(0, 32*len(AVAILABLE_COLOR), 32):
            for y in range(0, 32*3, 32):
                color : pygame.Color = AVAILABLE_COLOR[x//32]
                if y == 0:
                    color = lerp_color(blanc, color, fade_scale)
                elif y == 64:
                    color = lerp_color(noir, color, fade_scale)

                affiche_rectangle((x,y), (x+30,y+30), noir, 2)
                affiche_rectangle((x,y), (x+30,y+30), blanc, 1)
                affiche_rectangle_plein((x+1,y+1), (x+29,y+29), color, 0)

    def draw_canvas(self):
        self.canvas.refresh()

def main():
    affiche_auto_off()
    interface = Interface(TAILLE_FENETRE)
    interface.draw_background()
    interface.draw_interface_color()
    interface.draw_canvas()
    affiche_tout()
    wait_clic()


if __name__ == "__main__":
    main()