from graphics import *
from math import sqrt, cos, sin, acos, asin
from pygame import Color

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

def coord_vers_direction(positon_du_joueur,coordonnée):
    coordx, coordy = coordonnée
    pos_j_x, pos_j_y = positon_du_joueur
    deltax, deltay = (coordx - pos_j_x, coordy - pos_j_y)
    hypothenus = sqrt((deltax**2) + (deltay**2))
    angle = acos(deltax/hypothenus)


    """Obtiens une direction mono-directionnel via des coordonnée d'écran"""


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

