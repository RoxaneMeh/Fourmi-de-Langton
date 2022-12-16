import pygame
from sys import exit
import ast


pygame.init()

titre = ("Basic mode")
basic_font = pygame.font.SysFont(None,50)
nom_font = pygame.font.SysFont(None,25)
longueur_e = 1200
largeur_e = 800
window = pygame.display.set_mode((longueur_e,largeur_e))
pygame.display.set_caption("basic mode")
clock = pygame.time.Clock()
vitesse =20
fond = pygame.Surface((longueur_e,largeur_e))
fond.fill("White")
cote_carre = 10
plan = {}
orientation = ["haut", "droite", "bas", "gauche"]
ant_img = {"haut": pygame.image.load("ant_haut.png"), "droite": pygame.image.load("ant_droite.png"), "bas": pygame.image.load("ant_bas.png"), "gauche": pygame.image.load("ant_gauche.png")}

liste_couleur = []


class ant :
    
    def __init__(self, x = longueur_e/2, y = largeur_e/2, i=0):
        self.x = x
        self.y = y
        self.orient = "haut"
        self.nom = noms[i]
        self.pos_nom = self.x - 10, self.y -30

    @property
    def pos(self):
        return (self.x, self.y)
    

    @property
    def img(self) :
        return ant_img[self.orient]
    
    def avancer(self):
        if self.orient == "haut" :
            self.y -= cote_carre
        if self.orient == "droite" :
            self.x += cote_carre
        if self.orient == "bas" :
            self.y += cote_carre
        if self.orient == "gauche" :
            self.x -= cote_carre
            
    def droite(self):
        self.orient = orientation[(orientation.index(self.orient)+1)%4]

    def gauche(self):
        self.orient = orientation[(orientation.index(self.orient)-1)%4]
#ICI, le programme ne marche que pour le déplacement RLR        
    def deplacer(self, couleur): #definir deplacement couleur ; Liste des couleurs doit se faire en fonction du nombre de déplacement
        if couleur == "blanc" :
            pygame.draw.rect(fond,liste_couleur[0],(self.x,self.y,cote_carre,cote_carre))
            plan[self.pos] = "noir"
            self.droite()
            self.avancer()

        if couleur == "noir" :
            pygame.draw.rect(fond,liste_couleur[1],(self.x,self.y,cote_carre,cote_carre))
            plan[self.pos] = "choix_couleur"
            self.gauche()
            self.avancer()

        if couleur == "choix_couleur" :
            pygame.draw.rect(fond,liste_couleur[2],(self.x,self.y,cote_carre,cote_carre))
            plan[self.pos] = "blanc"
            self.droite()
            self.avancer()

pattern = input("Indiquez le déplacement souhaité : ") # Demander pattern deplacement, str()
nb_color = len(pattern)
k = 0
while k < len(pattern):
    choix_couleur = ast.literal_eval(input("Entrer la couleur souhaitée : "))
    liste_couleur.append(choix_couleur)
    k += 1
nb_fourmi = int(input("nombre de fourmis souhaité : "))
f = open("fichier_noms.txt", "r")
noms = []
for i in range(nb_fourmi):
    noms.append(f.readline().strip())
f.close()
fourmis = [ant(x = (1+2*k)*longueur_e/(nb_fourmi*2), y = largeur_e/2, i = k) for k in range(nb_fourmi)]
for fourmi in fourmis :
    print(fourmi.nom)


compte = 0

def ecran_daccueil():
    pygame.display.set_caption("accueil")
    while True :
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                pygame.quit()
                exit()
        fond.fill("White")
        window.blit(fond,(0,0))
        window.blit(basic_font.render("écran d'accueil", True, "Blue"), (longueur_e/2, largeur_e/2))
        pygame.display.update()
        clock.tick(vitesse)
    
while True :
    affichage_compte = basic_font.render(str(compte),True,"Black")
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            ecran_daccueil()
            break
    for fourmi in fourmis : # A modifier pour les couleurs
        if compte > 0 :
            if (fourmi.pos not in plan) or plan[fourmi.pos] == "blanc" :
                fourmi.deplacer("blanc")
            elif plan[fourmi.pos] == "noir" :
                fourmi.deplacer("noir")
            else :
               fourmi.deplacer("choix_couleur")
    compte += 1
    window.blit(fond,(0,0))
    for fourmi in fourmis :
        window.blit(fourmi.img, (fourmi.x - 10, fourmi.y - 8))
        if vitesse < 10 or (compte-1)%(vitesse/10) == 0:
            fourmi.pos_nom = fourmi.x - 10, fourmi.y - 30
        affichage_nom = nom_font.render(fourmi.nom,True,"Red", "Pink")
        window.blit(affichage_nom, fourmi.pos_nom)
    window.blit(affichage_compte,(0,0))
    pygame.display.update()
    clock.tick(vitesse)


    
#créer écran d'accueil
#créer classe fourmi, attributs positions 
#créer classe couleur. attribut nom, R/L, fonctions pour déplacement ?
#créer jeu, prenant en paramètres des fourmis et des couleurs, vitesse
#attention aux possibilités de positions/nombre des fourmis !! sur cases
#pygame.transform.rotate()
#pygame.transform.scale
#basic mode : fourmi de Langton originale, vitesse lente
#mode intermédiaire : choix de pattern et couleurs, nombre de fourmis, vitesse moyenne
#mode pro : choix illimité, vitesse max, rendu graphique limité
#mode interactif
