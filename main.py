from pygame import Surface, Vector2
from graphics import *
from typing import List, Tuple
import math
import random
import time

Coord = Tuple[int, int]
Pixel = Tuple[int, int]
Couleur = Tuple[int, int, int]

COLOR_HERBE_1 = Color("#28b463")
COLOR_HERBE_2 = Color("#27ae60")

TAILLE_FENETRE = (480,270)
TAILLE_CASE = 40
TAILLE_TERRAIN = (TAILLE_FENETRE//TAILLE_CASE, TAILLE_FENETRE//TAILLE_CASE)

TYPE_SOL = 0
TYPE_MUR = 1
TYPE_PORTE = 2

CONTENUE_NONE = 0
CONTENUE_ENNEMIE = 1

#Case stock :
#  type de sol = int

def init_cases():
    cases = []
    for y in range(TAILLE_FENETRE[1]//TAILLE_CASE):
        cases.append([])
        for x in range(TAILLE_FENETRE[0]//TAILLE_CASE):
            cases[y].append(TYPE_SOL)
    return cases

def generer_terrain(cases):
    for y, ligne in enumerate(cases):
        for x, case in enumerate(ligne):
            print(case,end="")
        print("")

def grille_vers_fenetre(i,j):
    x = i * TAILLE_CASE
    y = j * TAILLE_CASE
    return (x,y)

def fenetre_vers_grille(x,y):
    i = y // TAILLE_CASE
    j = x // TAILLE_CASE
    return (i,j)

def affiche_jeu():
    affiche_terrain()
    affiche_ennemies()
    affiche_joueur()
    affiche_hud()

def affiche_ennemies(ennemies):
    pass

def affiche_terrain():
    global cases
    for cy, ligne in enumerate(cases):
        for cx, _case in enumerate(ligne):
            typesol, contenue = _case
            fx, fy = grille_vers_fenetre(cx,cy)
            couleur = noir
            if typesol == TYPE_SOL:
                couleur = COLOR_HERBE_1
                if (cx+cy)%2==0:
                    couleur = COLOR_HERBE_2
            elif typesol == TYPE_MUR:
                couleur = violet
            elif typesol == TYPE_PORTE:
                couleur = blanc
            affiche_rectangle_plein((fx,fy),(fx+TAILLE_CASE,fy+TAILLE_CASE),couleur)

def comportement_ennemies(ennemies):
    """Cette fonction gère le comportement de l'énnemie et de son déplacement"""
    pass

def comportement_joueur():
    """Cette fonction gère le comportement du joueur et de son déplacement
    Elle gère le comportement qui peu être : Collision avec les murs, ennemie, porte, etc..."""
    deplacement_joueur()

def deplacement_joueur():
    pass


def fermer_jeu():
    remplir_fenetre(blanc)
    affiche_texte_centre("Fin du Jeu",(TAILLE_FENETRE[0]/2,TAILLE_FENETRE[1]/2)/2,noir,48,"calibri")

def comportement_initial():
    """"""
    pass

def main():
    init_fenetre(*TAILLE_FENETRE,"Hello guys !")
    cases = init_cases()
    position_joueur = init_joueur(cases)
    positions_ennemies = init_ennemies(cases)
    fermer_jeu = False
    affiche_jeu()

    while not fermer_jeu:
        comportement_joueur()
        comportement_ennemies()


if __name__ == "__main__":
    main()

from graphics import *
import time

FPS = 300
DPF = 1/FPS
TIME_UNTIL_FPS_AVERAGE = 1.0
UNLIMITED_FRAME = True

chrono_loop = "chrono_loop"

def millis_to_second(millis):
    return millis*(10**-3)

def step(cercle,delta_time):
    if cercle[0] > 480:
        cercle[0] = cercle[0] % 480
    else:
        cercle[0] += delta_time * 300

    affiche_cercle_plein(cercle,10,bleu)

def moyenne_array(array):
    return sum(array)/len(array)

def min_array(array):
    mini = array[0]
    for i in range(1,len(array)):
        mini = min(mini, array[i])
    return mini

def frame_handling(act_time,TUFA_last_refresh,delta_time,last_chronos_time,frames,frame_array,displayed_frame_array):
    act_time = millis_to_second(lire_chrono(chrono_loop))
    if act_time - TUFA_last_refresh > TIME_UNTIL_FPS_AVERAGE:
        displayed_frame_array = frame_array.copy()
        TUFA_last_refresh = act_time
        frame_array.clear()
    
    time.sleep(max(DPF - (act_time - last_chronos_time),0))
    delta_time = act_time - last_chronos_time
    last_chronos_time = act_time
    if len(frame_array) >= FPS:
        frame_array.pop(0)
    frame_array.append(1/delta_time)
    frames += 1
    affiche_tout()

    return (act_time,TUFA_last_refresh,delta_time,last_chronos_time,frames,frame_array,displayed_frame_array)


def main():
    init_fenetre(480,400,"Fenêtre de Test")

    init_chrono(chrono_loop)
    lance_chrono(chrono_loop)

    delta_time = 0.01
    last_chronos_time = 0
    frames = 0
    act_time = 0
    frame_array = [0]
    displayed_frame_array = [0]
    TUFA_last_refresh = 0
    affiche_auto_off()

    cercle = [0,200]

    while pas_echap():
        # Code Ici
        remplir_fenetre(blanc)
        step(cercle,delta_time)
        affiche_texte(f"FPS : {round(1/delta_time)}/{FPS}",(0,22),rouge,20)
        affiche_texte(f"FPS Avg: {round(moyenne_array(displayed_frame_array),1)} - 0.1% Low : {min_array(displayed_frame_array)} - Frames : {frames}",(0,0),rouge,20)
        # Gestion de la framerate

        (act_time,TUFA_last_refresh,delta_time,last_chronos_time,frames,frame_array,displayed_frame_array) = frame_handling(act_time,TUFA_last_refresh,delta_time,last_chronos_time,frames,frame_array,displayed_frame_array)







main()

