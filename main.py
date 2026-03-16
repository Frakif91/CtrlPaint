from pygame import Surface, Vector2, Rect, Color
from graphics import *
from typing import List, Tuple, Dict, overload
import math
import random
import time
from utilitaire import *

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

def mix(color1, color2, t) -> Tuple[int,int,int]:
    return tuple(
        int(c1 * (1 - t) + c2 * t)
        for c1, c2 in zip(color1, color2)
    )

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
        self.type : str = "circle"
        self.color = color
        self.radiuses = (radius_horizontal, radius_vertical)
        self.width = width

    """Line"""
    def __init__(self, start : Coord, end : Coord, color : Couleur, width : int = 1):
        self.type : str = "line"
        self.color = color
        self.width = width
        self.start : Coord = start
        self.end : Coord = end

    """raw
    format ->  dict((pixel_x,pixel_y)) = color
    and the dict must be the same size as the canvas"""
    def __init__(self, raw_data : Dict[Coord,Couleur]):
        self.type : str = "Raw"

    def draw(self, surf):
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

class Canvas:

    def __init__(self, taille : Coord):
        self.taille = taille
        self.draw_history : List[Drawing] = []

    def redraw(self, center_position : Coord = (0,0)):
        corner = soustraction_tuple(center_position, multiplication_tuple(self.taille, 0.5))
        affiche_rectangle_plein(corner, addition_tuple(self.taille,corner), blanc)
        for drawing in self.draw_history:
            drawing.draw(self, corner)

    def add_shape(self, drawing : Drawing):
        self.draw_history.append(drawing)

    def rewind(self, step : int = 1):
        for i in range(len(self.draw_history), max(len(self.draw_history) - step ,-1), -1):
            del self.draw_history[i]


class Button:

    button_list : List = []

    def _update_everyone(last_clic : Coord):
        for button in Button.button_list:
            button.update(last_clic)

    def __init__(self, position : Coord, size : Coord, text : str, color : Couleur, action : callable = lambda : None, font_size : int = 20, font_name : str = "Arial", font_color : Couleur = noir):
        self.position = position
        self.size = size
        self.text = text
        self.color = color
        self.action = action
        self.font_size = font_size
        self.font_name = font_name
        self.font_color = font_color
    
    def draw(self):
        affiche_rectangle_plein(self.position, add_coord(self.position, self.size), self.color)
        affiche_texte(self.text, add_coord(self.position, (self.size[0]//2, self.size[1]//2)), self.font_color, self.font_size, self.font_name)

    def update(self, click_position : Coord):
        if self.position[0] <= click_position[0] <= self.position[0] + self.size[0] and self.position[1] <= click_position[1] <= self.position[1] + self.size[1]:
            self.action()


class Interface:

    def __init__(self, size : Coord):
        init_fenetre(size[0], size[1], "Ctrl Paint")
        self.size = size
        self.choosen_color = noir
        self.canvas = Canvas(multiplication_tuple(self.size,0.5))
        self.background_offset = 0.0
        self.chrono_loop = "fpsloop"

    def draw_background(self, offset : Coord = (0,0)):
        color1 = Color("#388CA5")
        color2 = Color("#38AAB9")
        for x in range(-TAILLE_CASE*3, self.size[0], TAILLE_CASE):
            for y in range(-TAILLE_CASE*3, self.size[1], TAILLE_CASE):
                affiche_rectangle_plein(add_coord(offset,(x,y)), add_coord(offset,(x+TAILLE_CASE,y+TAILLE_CASE)), color1 if (x+y) % 80 == 0 else color2)

    def draw_interface_color(self, offset : Coord = None):
        """
        Affiche les couleurs disponibles pour le dessin
        dans un carre avec un gradient de blanc a noir
        pour indiquer la selection de la couleur
        offset est le decalage du carre par rapport a la position (0,0) de la fenetre
        """
        if offset is None:
            offset : Coord = (10,10)
        fade_scale = 0.4
        for x in range(0, 32*len(AVAILABLE_COLOR), 32):
            for y in range(0, 32*3, 32):
                color : pygame.Color = AVAILABLE_COLOR[x//32]
                if y == 0:
                    color = lerp_color(blanc, color, fade_scale)
                elif y == 64:
                    color = lerp_color(noir, color, fade_scale)

                affiche_rectangle(add_coord((x,y),offset), add_coord((x+30,y+30),offset), noir, 2)
                affiche_rectangle(add_coord((x,y),offset), add_coord((x+30,y+30), offset), blanc, 1)
                affiche_rectangle_plein(add_coord((x+1,y+1),offset), add_coord((x+29,y+29),offset), color, 0)

    def draw_canvas(self):
        print("Redrawing canvas : Center is ", multiplication_tuple(self.size,0.25))
        self.canvas.redraw(multiplication_tuple(self.size,0.5))

    def update_interface(self,delta):
        self.background_offset += 1
        self.draw_background((self.background_offset % TAILLE_CASE*2,(self.background_offset*0.5) % TAILLE_CASE*2 ))
        self.draw_interface_color()
        self.draw_canvas()
    

    def main_loop(self):
        init_chrono(self.chrono_loop)
        lance_chrono(self.chrono_loop)

        self.delta_time : float = 0.01
        self.last_chronos_time = 0
        self.frames : int = 0
        self.act_time = 0
        self.frame_array = [0]
        self.displayed_frame_array = [0]
        self.TUFA_last_refresh = 0
        affiche_auto_off()

        while pas_echap():
            
            
            self.update_interface(self.delta_time)

            affiche_texte(f"FPS : {round(1/self.delta_time)}/{FPS}",(0,22),blanc,20)
            affiche_texte(f"FPS Avg: {round(moyenne_array(self.displayed_frame_array),1)} - 0.1% Low : {min_array(self.displayed_frame_array)} - Frames : {self.frames}",(0,0),blanc,20)
            # Gestion de la framerate
            frame_handling(self)



def main():
    affiche_auto_off()
    interface = Interface(TAILLE_FENETRE)
    interface.draw_background()
    interface.draw_interface_color()
    interface.draw_canvas()
    interface.main_loop()



if __name__ == "__main__":
    main()