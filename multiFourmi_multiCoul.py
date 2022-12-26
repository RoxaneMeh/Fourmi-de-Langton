import pygame
from sys import exit
import random

pygame.init()

titre = ("Basic mode")
basic_font = pygame.font.SysFont(None,50)
nom_font = pygame.font.SysFont(None,25)
longueur_e = 1400
largeur_e = 800
window = pygame.display.set_mode((longueur_e,largeur_e))
pygame.display.set_caption(titre)
clock = pygame.time.Clock()
vitesse = int(input("vitesse : "))
fond = pygame.Surface((longueur_e,largeur_e))
fond.fill("White")
cote_carre = 10
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
        return (self.x, self.y) #mise à jour tuple position


    @property
    def img(self) :
        return ant_img[self.orient] #met automatiquement à jour le rendu image quand l'orientation change

    def avancer(self): #les x augmentent vers la droite et les y vers le bas
        if self.orient == "haut" :
            self.y -= cote_carre
        if self.orient == "droite" :
            self.x += cote_carre
        if self.orient == "bas" :
            self.y += cote_carre
        if self.orient == "gauche" :
            self.x -= cote_carre

    def tourner(self, dep):
        if dep == "D" :
            self.orient = orientation[(orientation.index(self.orient)+1)%4] #passe à l'orientation suivante (liste rangée de telle sorte)
        if dep == "G" :
            self.orient = orientation[(orientation.index(self.orient)-1)%4] #orientation précédente

    def deplacer(self,i,liste):
        self.tourner(liste[i][1]) #tourne selon le déplacement correspondant
        new_i = (i + 1)%len(liste) #la nouvelle couleur est la couleur suivante dans la liste (-buffer circulaire)
        pygame.draw.rect(fond, liste[new_i][0],(self.x,self.y,cote_carre,cote_carre)) #colorie en la nouvelle couleur
        plan[self.pos] = new_i #enregistre nouvelle couleur dans le plan
        self.avancer()


nb_fourmi = int(input("nombre de fourmis souhaité : "))
f = open("listePrenoms.txt", "r") #fichier contenant des milliers de noms prédéfinis
noms = []
for i in range(nb_fourmi):
    noms.append(f.readline().strip()) #attribue le i-ème nom à la i-ème fourmi (pas aléatoire) pour les distinguer
f.close()
fourmis = [ant(x = (1+2*k)*(((longueur_e/(nb_fourmi*2))//cote_carre)*cote_carre), y = largeur_e/2, i = k) for k in range(nb_fourmi)] #liste des fourmis avec pt de départ répartis uniformément sur la longueur de la fenêtre, en faisant attention à les séparer d'un nombre entier de carreaux
for fourmi in fourmis :
    print(fourmi.nom)

#definir fonction couleur(i, nb_dep) tq couleur(0) = "White", couleur(nb_dep - 1) = "Black"
def couleur(i, n) :
	if i == 0 :
		return "White"
	if i == n -1 :
		return "Black"
	else :
		return (random.randint(0,255),random.randint(0,255),random.randint(0,255))


sequence = input("séquence de D/G : ")
nb_dep = len(sequence)
listeCD = [] #liste contenant tuples (couleur, déplacement associé)
for i in range(nb_dep) :
	listeCD.append((couleur(i,nb_dep),sequence[i]))

print(listeCD)




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


compte = 0

while True :
    affichage_compte = basic_font.render(str(compte),True,"Black")
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            ecran_daccueil()
            break
    for fourmi in fourmis :
        if compte > 0 : #permet d'inclure l'état initial dans la boucle
            if (fourmi.pos in plan) :
                fourmi.deplacer(plan[fourmi.pos], listeCD)
            else :
                fourmi.deplacer(0, listeCD) #le fond de l'écran (blanc) n'est pas encore enregistré dans le plan
    compte += 1
    window.blit(fond,(0,0)) #imprimera les fourmi et noms au-dessus du fond
    for fourmi in fourmis :
        window.blit(fourmi.img, (fourmi.x - cote_carre/2, fourmi.y - cote_carre/2)) #centre fourmi sur carreau
        if vitesse < 10 or (compte-1)%(vitesse/10) == 0: # ne met pas à jour le nom à chaque signal d'horloge sinon illisible
            fourmi.pos_nom = fourmi.x - 10, fourmi.y - 30 #positionne étiquette nom à coté de la fourmi (arbitraire)
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
