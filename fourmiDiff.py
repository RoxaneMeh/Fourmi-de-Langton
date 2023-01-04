import pygame
from sys import exit
import random

pygame.init()

titre = ("Mode classique") #titre dépendra du mode choisi, non tous définis pour l'instant


large_font = pygame.font.SysFont(None,50)
small_font = pygame.font.SysFont(None,25)
med_font = pygame.font.SysFont(None,35)
longueur_e = 1400
largeur_e = 800
window = pygame.display.set_mode((longueur_e,largeur_e))
pygame.display.set_caption(titre)
clock = pygame.time.Clock()
fond = pygame.Surface((longueur_e,largeur_e))
fond.fill("White")
plan = {}
orientation = ["haut", "droite", "bas", "gauche"] #liste que sera utilisé comme buffer circulaire
affichage_pause = large_font.render("ll",True,"Black")


#consultation de l'utilisateur pour mode interactif (version sans écran d'accueil)
reponse = "a"
while reponse != "oui" and reponse != "non" :
    reponse = input("\nLe mode interactif consiste à cliquer sur l'écran pour ajouter des carreaux noirs. Si la case est déjà noire, elle devient blanche. \nSouhaitez-vous passer en mode interactif ? (oui/non) \n> ")
if reponse == "oui" :
    interactif = True
    titre = "Mode interactif"
else : interactif = False


#utile à modifier pour mieux voir
vitesse = int(input("\nLa vitesse sera modifiable par la suite à l'aide des touches F (faster) et S (slower). \nvitesse initiale (1 à 60 fps) : "))
cote_carre = 2


#création du dictionnaire contenant les images pour chaque orientation (implémentation à la main), ajustées à la taille des carreaux
ant_img = {}
for orient in orientation :
    ant_img[orient] = pygame.transform.scale(pygame.image.load(f"ant_{orient}.png"),(2*cote_carre,2*cote_carre))


class ant :

    def __init__(self, seq, regles, nom, x = longueur_e/2, y = largeur_e/2):
        self.x = x
        self.y = y
        self.orient = "haut"
        self.nom = nom
        self.affichage_nom = small_font.render(self.nom,True,"Red", "Pink")
        self.pos_nom = self.x - 10, self.y -30
        self.regles = regles #les règles ne sont plus les mêmes pour toutes les fourmis
        self.seq = seq
        self.affichage_seq = small_font.render(f"{self.nom} : {self.seq}", True, "Black")

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
        if dep == "R" :
            self.orient = orientation[(orientation.index(self.orient)+2)%4] #orientation opposée

    def deplacer(self,i):
        self.tourner(self.regles[i][1]) #tourne selon le déplacement correspondant
        new_i = (i + 1)%len(self.regles) #la nouvelle couleur est la couleur suivante dans la liste (-buffer circulaire)
        pygame.draw.rect(fond, self.regles[new_i][0],(self.x,self.y,cote_carre,cote_carre)) #colorie en la nouvelle couleur
        plan[self.pos] = new_i #enregistre nouvelle couleur dans le plan
        self.avancer()

#definir fonction couleur(i, nb_dep) tq couleur(0) = "White", couleur(nb_dep - 1) = "Black"
def couleur(i, n) :
	if i == 0 :
		return "White"
	if i == n -1 :
		return "Black"
	else :
        return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

nb_fourmi = int(input("nombre de fourmis souhaité : "))
f = open("listePrenoms.txt", "r") #fichier contenant des milliers de noms prédéfinis
noms = []
for i in range(nb_fourmi):
    noms.append(f.readline().strip()) #attribue le i-ème nom à la i-ème fourmi (pas aléatoire) pour les distinguer
f.close()

if nb_fourmi > 1 :
    reponse = "a"
    while reponse != "identiques" and reponse != "différentes" :
        reponse = input("\nVoulez des fourmis identiques ou suivant des règles différentes? (identiques/différentes)\n> ")

if nb_fourmi == 1 or reponse == "identiques" :
    twin = True
    sequence = input("\nD: droite, G : gauche, A : avance, R : recule\nséquence de D/G/A/R : ")
    affichage_sequence = med_font.render(sequence,True,"Black")
    nb_dep = len(sequence)
    listeCD = [(couleur(i, nb_dep),sequence[i]) for i in range(nb_dep)] #liste contenant tuples (couleur, déplacement associé). Par la suite, on se réferera simplement aux indices pour désigner les couleurs

    print(listeCD)

    fourmis = [ant(sequence, listeCD, noms[k], x = (1+2*k)*(((longueur_e/(nb_fourmi*2))//cote_carre)*cote_carre), y = largeur_e/2) for k in range(nb_fourmi)] #liste des fourmis avec pt de départ répartis uniformément sur la longueur de la fenêtre, en faisant attention à les séparer d'un nombre entier de carreaux
    print("L'équipe est prête !")
    for fourmi in fourmis :
        print(fourmi.nom)

else :
    twin = False
    fourmis = []
    print("entrez des séquences D/G de même longueur")
    for k in range(nb_fourmi) :
        sequence = input(f"{noms[k]} : ")
        if k == 0 :
            nb_dep = len(sequence)
            couleurs = [couleur(i,nb_dep) for i in range(nb_dep)]
        if k > 0 :
            while len(sequence) != nb_dep :
                sequence = input(f"{noms[k]} : ")
        listeCD = [(couleurs[i],sequence[i]) for i in range(nb_dep)]
        #listeCD = [(couleur(i, nb_dep),sequence[i]) for i in range(nb_dep)]
        fourmis.append(ant(sequence, listeCD, noms[k], x = (1+2*k)*(((longueur_e/(nb_fourmi*2))//cote_carre)*cote_carre), y = largeur_e/2))  #liste des fourmis avec pt de départ répartis uniformément sur la longueur de la fenêtre, en faisant attention à les séparer d'un nombre entier de carreaux



def getChoix():
    pygame.display.set_caption("écran choix")
    i = 0
    while i< nb_fourmi :
        texte = med_font.render(f"choisissez la position initiale de {fourmis[i].nom} ({fourmis[i].seq})",True,"Black")
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                ecran_daccueil()
                break
            if event.type == pygame.MOUSEBUTTONDOWN :
                x, y = event.pos
                #il faut réaligner avec le quadrillage :
                x -= x%cote_carre
                y-= y%cote_carre
                fourmis[i].x, fourmis[i].y = (x,y)
                i += 1

        window.blit(fond,(0,0)) #imprimera les fourmis et noms au-dessus du fond

        for fourmi in fourmis[:i] :
            window.blit(fourmi.img, (fourmi.x - cote_carre/2, fourmi.y - cote_carre/2)) #centre fourmi sur carreau
            fourmi.pos_nom = fourmi.x - 10, fourmi.y - 30 #positionne étiquette nom à coté de la fourmi (arbitraire)
            affichage_nom = small_font.render(fourmi.nom,True,"Red", "Pink")
            window.blit(affichage_nom, fourmi.pos_nom)

        window.blit(texte,(0,0))
        pygame.display.update()

#consultation de l'utilisateur pour les positions initiales
reponse = "a"
while reponse != "oui" and reponse != "non" :
    reponse = input("\nSouhaitez-vous choisir les positions initales ? (oui/non)\n> ")
if reponse == "oui" :
    getChoix()

def ecran_daccueil():
    pygame.display.set_caption("accueil")
    fond.fill("White")
    while True :
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                pygame.quit()
                exit()

        window.blit(fond,(0,0))
        window.blit(large_font.render("écran d'accueil", True, "Blue"), (longueur_e/2, largeur_e/2))
        pygame.display.update()



def start(nom_mode, vitesse, fourmis, interactif) :
    pygame.display.set_caption(nom_mode)
    Run = True #variable pour mettre en pause
    Aff = True #variable pour afficher ou non les détails autres que le fond
    compte = -1

    while True :

        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                ecran_daccueil()
                break
            if interactif and event.type == pygame.MOUSEBUTTONDOWN : #interactif
                x, y = event.pos
                #il faut réaligner avec le quadrillage :
                x -= x%cote_carre
                y-= y%cote_carre
                if (x,y) in plan and plan[(x,y)] == nb_dep-1 :
                    plan[(x,y)] = 0
                    pygame.draw.rect(fond, "White",(x,y,cote_carre,cote_carre))
                else :
                    plan[(x,y)] = nb_dep-1 #couleur noire
                    pygame.draw.rect(fond, "Black",(x,y,cote_carre,cote_carre))

            if event.type == pygame.KEYDOWN :

                if event.key == pygame.K_SPACE :
                    Run = not Run

                if event.key == pygame.K_a :
                    Aff = not Aff

                if event.key == pygame.K_f :
                    vitesse *= 2

                if event.key == pygame.K_s :
                    vitesse /= 2

        if Run :
            compte += 1
            if compte > 0  : #permet d'inclure l'état initial dans la boucle??
                for fourmi in fourmis :
                    if (fourmi.pos in plan) :
                        fourmi.deplacer(plan[fourmi.pos])
                    else :
                        fourmi.deplacer(0) #le fond de l'écran (blanc) n'est pas encore enregistré dans le plan

        window.blit(fond,(0,0)) #imprimera les fourmis et noms au-dessus du fond

        if Aff :
            for fourmi in fourmis :
                window.blit(fourmi.img, (fourmi.x - cote_carre/2, fourmi.y - cote_carre/2)) #centre fourmi sur carreau
                if vitesse < 10 or compte%(vitesse//10) == 0: # ne met pas à jour le nom à chaque signal d'horloge sinon illisible
                    fourmi.pos_nom = fourmi.x - 10, fourmi.y - 30 #positionne étiquette nom à coté de la fourmi (arbitraire)
                window.blit(fourmi.affichage_nom, fourmi.pos_nom)
                if not twin :
                    window.blit(fourmi.affichage_seq, (0, 20*fourmis.index(fourmi) + 50))

            affichage_compte = large_font.render(str(compte),True,"Black")
            window.blit(affichage_compte,(0,0))
            if twin :
                window.blit(affichage_sequence,(0,50))
            if not Run :
                window.blit(affichage_pause, (longueur_e - 50, 0))
        if vitesse < 60 or not Run or compte*10%vitesse == 0 : #permet d'aller plus vite en n'affichant pas les dépacements 1 par 1 mais n'affiche plus pause
            pygame.display.update()
        clock.tick(vitesse)

start(titre, vitesse, fourmis, interactif)

#créer écran d'accueil

#créer jeu, prenant en paramètres des fourmis et des couleurs, vitesse
#basic mode : fourmi de Langton originale, vitesse lente
#mode intermédiaire : choix de pattern et couleurs, nombre de fourmis, vitesse moyenne
#mode pro : choix illimité, vitesse max, rendu graphique limité
#mode interactif
#problème : compte = 0 trop rapide (à peine visible avant passage à 1)

#définir une fonction qui vérifie si un séquence entrée est de la bonne forme
#est-ce que c'est bien que le plan soit un dictionaire où il faut vérifier si la position est dedans ? (en terme de compexité) réfléchir à tableau si on autorise sortie de l'écran