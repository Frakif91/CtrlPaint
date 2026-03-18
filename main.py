from pygame import Surface, Vector2, Rect, Color
from graphics import *
import graphics
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
    #Bleu,            Violet,               Magenta,            Rouge,               Orange,           Jaune,            Vert,             Vert foncée,      Noir        et    Blanc
    Color("#0000ff"), Color("#aa00ff"), Color("#ff00ff"),Color("#ff0000"), Color("#ff9900"), Color("#ffff00"),  Color("#00ff00"), Color("#008800"), Color("#202020"), Color("#d0d0d0")
]


TAILLE_FENETRE = (1152,648)
TAILLE_CASE = 80
TAILLE_TERRAIN = (TAILLE_FENETRE[0]//TAILLE_CASE, TAILLE_FENETRE[1]//TAILLE_CASE)

def _mesure_time(func : callable, *args) -> float:
    start = time.time()
    func(*args)
    print("Fonction :", func.__name__, "dure", time.time() - start, "ms" )
    return time.time() - start


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
    def __init__(self, raw_data : List[Coord], color : Couleur = (0,0,0), draw_size : int = 5):
        self.type : str = "raw"
        self.raw_data = raw_data
        self.draw_size = draw_size
        self.color = color

    def draw(self, offset : Coord = (0,0)):
        if not hasattr(self,"type"):
            raise NotImplementedError("Type de dessin non implémenté")
        if self.type == "rect":
            if self.width <= 0:
                affiche_rectangle_plein(add_coord(offset,self.start), add_coord(offset,self.end), self.color)
            else:
                affiche_rectangle(add_coord(offset,self.start), add_coord(offset,self.end), self.color, self.width)
        elif self.type == "circle":
            if self.width <= 0:
                affiche_ellipse_plein(add_coord(offset,self.center), self.radiuses, self.color)
            else:
                affiche_ellipse(add_coord(offset,self.center), self.radiuses, self.color, self.width)
        elif self.type == "line":
            affiche_ligne(add_coord(offset,self.start), add_coord(offset,self.end), self.color, max(self.width,1))
        elif self.type == "raw":
            if len(self.raw_data) > 1:
                affiche_lignes([add_coord(offset,coord) for coord in self.raw_data], self.color, self.draw_size)
            elif len(self.raw_data) > 0:
                affiche_cercle(add_coord(offset,self.raw_data[0]), self.draw_size, self.color)

class Canvas:

    def __init__(self, taille : Coord):
        self.taille = taille
        self.corner = (0,0)
        self.draw_history : List[Drawing] = []

    def redraw(self, center_position : Coord = (0,0)):
        self.corner = soustraction_tuple(center_position, multiplication_tuple(self.taille, 0.5))
        affiche_rectangle_plein(self.corner, addition_tuple(self.taille,self.corner), blanc)
        for drawing in self.draw_history:
            drawing.draw(self.corner)

    def add_shape(self, drawing : Drawing):
        self.draw_history.append(drawing)

    def rewind(self, step : int = 1):
        for i in range(len(self.draw_history)-1, max(len(self.draw_history) - step -1 ,-1), -1):
            del self.draw_history[i]


class Button:

    button_list : List = []

    def _update_everyone(last_clic : Coord):
        for button in Button.button_list:
            button.update(last_clic)

    def __init__(self, position : Coord, size : Coord, text : str, color : Couleur, action : callable = lambda : None, font_size : int = 20, font_name : str = "Arial", font_color : Couleur = noir, *callable_args):
        self.position = position
        self.size = size
        self.text = text
        self.color = color
        self.action = action
        self.font_size = font_size
        self.font_name = font_name
        self.font_color = font_color
        self.callable_args = callable_args
        Button.button_list.append(self)
    
    def draw(self):
        affiche_rectangle_plein(self.position, add_coord(self.position, self.size), self.color)
        if self.text != "":
            affiche_texte_centre(self.text, add_coord(self.position, multiplication_tuple(self.size,0.5)), self.font_color, self.font_size, self.font_name)

    def update(self, click_position : Coord):
        x,y = click_position
        if  self.position[0] <= x and x <= self.position[0] + self.size[0] and \
            self.position[1] <= y and y <= self.position[1] + self.size[1]:
            print("|", self, "executing action")
            self.action(*self.callable_args)


class Interface:
    """
    La classe Interface représente l'interface de l'application.
    Elle est chargée de gérer les événements, de mettre à jour l'affichage
    et de gérer l'histoique des actions de l'utilisateur.

    Attribus:
        size (Coord): La taille de la fenêtre.
        chosen_color (Couleur): La couleur actuellement sélectionnée.
        canvas (Canvas): Le canvas sur lequel on dessine.
        background_offset (float): Le décalage de l'arrière-plan.
        chrono_loop (str): Le type de boucle chrono utilisé.
        draw_mode (str): Le type de dessin utilisé.
        is_holding_mouse_click (bool): Vaut-il si le bouton de la souris est enfoncé.
        draw_buffer (List[Drawing]): La liste des formes à dessiner.
        pending_drawing (Drawing): La forme actuellement en train de dessin.
        chosen_color (Couleur): La couleur actuellement sélectionnée.
        undo_button (Button): Le bouton "Undo".

    Methodes:
        __init__(self, size: Coord): Initialise la classe Interface.
        draw_background(self, offset: Coord = (0,0)): Dessine l'arrière-plan en utilisant une grille de carres de deux couleurs.
        init_color_choice(self, offset: Coord = None): Initialise les boutons de sélection de couleurs.
        update(self, last_clic: Coord): Met à jour l'état de l'interface en fonction de la position du clic de la souris.
        main_loop(self): Lance la boucle principale de l'application.
    """

    def __init__(self, size : Coord):
        init_fenetre(size[0], size[1], "Ctrl Paint")
        self.size = size
        self.choosen_color = noir
        self.canvas = Canvas(multiplication_tuple(self.size,0.65))
        self.background_offset = 0.0
        self.chrono_loop = "fpsloop"
        self.draw_mode = "raw"
        self.is_holding_mouse_click = False
        self.draw_buffer = []
        self.pending_drawing : Drawing = None
        self.choosen_color = noir
        self.init_color_choice(soustraction_tuple(self.size, (290,100)))
        self.undo_button = Button((10, self.size[1]-60), (100, 50), "Undo", (150,50,50), self.canvas.rewind, 20, "Arial", blanc, 1)

    def draw_background(self, offset : Coord = (0,0)):
        """
        Dessine le fond de l'interface en utilisant une grille de carres de deux couleurs.
        offset est le decalage par rapport a la position (0,0) de la fenetre.
        """
        time_start = time.time()
        color1 = Color("#388CA5")
        color2 = Color("#38AAB9")
        for x in range(-TAILLE_CASE*3, self.size[0], TAILLE_CASE):
            for y in range(-TAILLE_CASE*3, self.size[1], TAILLE_CASE):
                affiche_rectangle_plein(add_coord(offset,(x,y)), add_coord(offset,(x+TAILLE_CASE,y+TAILLE_CASE)), color1 if (x+y) % (TAILLE_CASE*2) < TAILLE_CASE else color2)
        print("Temps de dessin de l'arriere plan : ", time.time() - time_start, "ms")


    def init_color_choice(self, offset : Coord = None):
        """
        Initialise les boutons de sélection de couleurs.
        
        offset est le decalage par rapport a la position (0,0) de la fenetre.
        """

        self.color_buttons = []
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

                b = Button(add_coord((x,y),offset),(30,30),"",color,self.change_color,10,"Arial",noir,color)
                self.color_buttons.append(b)

    def draw_interface_color(self):

        for b in self.color_buttons:
            b.draw()
        og = self.color_buttons[0].position
        affiche_rectangle(add_coord(og, (-58, 74)), add_coord(og, (-5,20)), blanc if moyenne_array(self.choosen_color) < 128 else noir, 2)
        affiche_rectangle_plein(add_coord(og, (-58, 74)), add_coord(og, (-5,20)), self.choosen_color, 0)
        
            #affiche_rectangle(b.position, add_coord(b.position, b.size), noir, 2)
            #affiche_rectangle(b.position, add_coord(b.position, b.size), blanc if b.color != self.choosen_color else jaune, 1)
            #affiche_rectangle_plein(add_coord(b.position, (1,1)), add_coord(b.position, add_coord(b.size,(-1,-1))), b.color, 0)


    def change_color(self, color : Couleur):
        self.choosen_color = color

    def draw_canvas(self):
        #print("Redrawing canvas : Center is ", multiplication_tuple(self.size,0.25))
        self.canvas.redraw(multiplication_tuple(self.size,0.5))

    def update_interface(self,delta):
        self.background_offset += delta * 30
        self.draw_background((int(self.background_offset) % TAILLE_CASE*2,(self.background_offset*0.5) % TAILLE_CASE*2 ))
        #_mesure_time()
        self.draw_interface_color()
        #_mesure_time()
        self.update_logic()
        #_mesure_time()
        self.draw_canvas()
        if self.pending_drawing:
            #_mesure_time(
            self.pending_drawing.draw(self.canvas.corner)
        self.undo_button.draw()

    def update_logic(self):
        pos = get_mouse_pos()
        clic = get_clicked(0)
        if clic:
            if not self.is_holding_mouse_click:
                Button._update_everyone(pos)
                print("Clicked",pos)
                self.pending_drawing = Drawing([], self.choosen_color)
                self.is_holding_mouse_click = True

            x,y = pos
            if  x > self.canvas.corner[0] and x < self.canvas.corner[0] + self.canvas.taille[0] and \
                y > self.canvas.corner[1] and y < self.canvas.corner[1] + self.canvas.taille[1]:
                if self.pending_drawing.type == "raw":
                    self.pending_drawing.raw_data.append(soustraction_tuple(pos, self.canvas.corner))
                
        else:
            if self.is_holding_mouse_click:
                self.is_holding_mouse_click = False
                print("Unclick")
                if len(self.pending_drawing.raw_data) > 0:
                    self.canvas.add_shape(self.pending_drawing)
                    self.pending_drawing = None
                        
    def main_loop(self):
        init_chrono(self.chrono_loop)
        lance_chrono(self.chrono_loop)

        self.delta_time : float = 0.01
        self.last_chronos_time = 0
        self.frames : int = 0
        self.act_time = 1
        self.frame_array = [0]
        self.displayed_frame_array = [0]
        self.TUFA_last_refresh = 0
        affiche_auto_off()

        while pas_echap():
            self.update_interface(self.delta_time)

            affiche_texte(f"FPS : {round(1/self.delta_time)}/{FPS}",(0,22),blanc,20)
            affiche_texte(f"FPS Avg: {round(moyenne_array(self.displayed_frame_array),1)} - 0.1% Low : {round(min_array(self.displayed_frame_array),1)} - Frames : {self.frames}",(0,0),blanc,20)
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