from pygame import Surface, Vector2, Rect   
from graphics import *
from typing import List, Tuple
import math
import random
import time

Coord = Tuple[int, int]
Pixel = Tuple[int, int]
Couleur = Tuple[int, int, int]

EMPTY_COLOR = Color(0, 0, 0)

TAILLE_FENETRE = (1152,648)
TAILLE_CASE = 40
TAILLE_TERRAIN = (TAILLE_FENETRE[0]//TAILLE_CASE, TAILLE_FENETRE/[1]/TAILLE_CASE)

def grille_vers_fenetre(i,j):
    x = i * TAILLE_CASE
    y = j * TAILLE_CASE
    return (x,y)

def fenetre_vers_grille(x,y):
    i = y // TAILLE_CASE
    j = x // TAILLE_CASE
    return (i,j)


class Drawing:
    def __init__(self, rect : Rect, surf : Surface):
        self.rect = rect
        self.surf = surf


class Layer(Surface):

    def __init__(self, taille : Coord):
        super().__init__(taille, pygame.SRCALPHA)
        self.draw_history : List[Drawing] = []
    
    def draw_shape(self, drawing : Drawing):
        self.draw_history.append(drawing)
        self.refresh()
    
    def rewind(self, step : int = 1):
        for i in range(len(self.draw_history), max(len(self.draw_history) - step ,-1), -1):
            pass

class Canvas