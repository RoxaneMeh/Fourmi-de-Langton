import pygame
from sys import exit


pygame.init()

titre = ("Basic mode")
basic_font = pygame.font.SysFont(None,50)
nom_font = pygame.font.SysFont(None,25)
longueur_e = 1200
largeur_e = 800
window = pygame.display.set_mode((longueur_e,largeur_e))
pygame.display.set_caption("basic mode")
clock = pygame.time.Clock()
vitesse = 1
fond = pygame.Surface((longueur_e,largeur_e))
fond.fill("White")
cote_carre = 15
plan = {}
orientation = ["haut", "droite", "bas", "gauche"]
ant_img = {}
for orient in orientation :
    ant_img[orient] = pygame.transform.scale(pygame.image.load(f"ant_{orient}.png"),(2*cote_carre,2*cote_carre))

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
        
    def deplacer(self, couleur):
        if couleur == "blanc" :
            pygame.draw.rect(fond,"Black",(self.x,self.y,cote_carre,cote_carre))
            plan[self.pos] = "noir"
            self.droite()
            self.avancer()

        if couleur == "noir" :
            pygame.draw.rect(fond,"White",(self.x,self.y,cote_carre,cote_carre))
            plan[self.pos] = "blanc"
            self.gauche()
            self.avancer()

           
nb_fourmi = int(input("nombre de fourmis souhaité : "))
f = open("listePrenoms.txt", "r")
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
    for fourmi in fourmis :
        if compte > 0 :
            if (fourmi.pos not in plan) or plan[fourmi.pos] == "blanc" :
                fourmi.deplacer("blanc")
            else :
               fourmi.deplacer("noir")
    compte += 1
    window.blit(fond,(0,0))
    for fourmi in fourmis :
        window.blit(fourmi.img, (fourmi.x - cote_carre/2, fourmi.y - cote_carre/2))
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
