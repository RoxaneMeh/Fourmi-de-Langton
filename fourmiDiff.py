import pygame
from sys import exit
import random
from ecran_resol import InputBox

#les fichiers suivant sont des versions alternatives du programme principal, seulement utilisées dans bibliothèque
from ant_marie import App
import colonies_painting_ant
import l2nnl1l2l1_ant

pygame.init()



maxi_font = pygame.font.SysFont("Courier New", 80)
large_font = pygame.font.SysFont("Courier New",31)
cpt_font = pygame.font.SysFont("Courier New",35, True)
small_font = pygame.font.SysFont("Courier New",18, bold = True)
med_font = pygame.font.SysFont("Courier New",25, bold = True)
#longueur_e = 1400
#largeur_e = 800
#window = pygame.display.set_mode((longueur_e,largeur_e))
window = pygame.display.set_mode()
longueur_e, largeur_e = window.get_size()
F_fond_fourmi = pygame.image.load('Fond_fourmi.png')
F_fond_fourmi = pygame.transform.scale(F_fond_fourmi, (longueur_e, largeur_e))
clock = pygame.time.Clock()
fond = pygame.Surface((longueur_e,largeur_e))
fond.fill("White")
orientation = ["haut", "droite", "bas", "gauche"] #liste que sera utilisé comme buffer circulaire
affichage_pause = cpt_font.render("||",True,"Black")



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

    def deplacer(self,i, plan):
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

def loadAnt(cote_carre):
    global ant_img
    ant_img = {}
    for orient in orientation :
        ant_img[orient] = pygame.transform.scale(pygame.image.load(f"ant_{orient}.png"),(2*cote_carre,2*cote_carre))


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
            window.blit(fourmi.affichage_nom, fourmi.pos_nom)

        window.blit(texte,(0,0))
        pygame.display.update()


def start(nom_mode, interactif, cote_carre, vitesse, fourmis, twin) :

    pygame.display.set_caption(nom_mode)
    Run = True #variable pour mettre en pause
    Aff = True #variable pour afficher ou non les détails autres que le fond
    plan = {} #le dictionnaire permet aux fourmis de sortir de l'écran mais n'est pas forcément une structure très efficace
    compte = -1
    nb_dep = len(fourmis[0].regles)
    while True :

        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                pygame.quit()
                exit()

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

                if event.key == pygame.K_ESCAPE :
                    ecran_daccueil()

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
                        fourmi.deplacer(plan[fourmi.pos], plan)
                    else :
                        fourmi.deplacer(0, plan) #le fond de l'écran (blanc) n'est pas encore enregistré dans le plan

        window.blit(fond,(0,0)) #imprimera les fourmis et noms au-dessus du fond

        if Aff :
            for fourmi in fourmis :
                window.blit(fourmi.img, (fourmi.x - cote_carre/2, fourmi.y - cote_carre/2)) #centre fourmi sur carreau
                if vitesse < 10 or compte%(vitesse//10) == 0: # ne met pas à jour le nom à chaque signal d'horloge sinon illisible
                    fourmi.pos_nom = fourmi.x - 10, fourmi.y - 30 #positionne étiquette nom à coté de la fourmi (arbitraire)
                window.blit(fourmi.affichage_nom, fourmi.pos_nom)
                if not twin :
                    window.blit(fourmi.affichage_seq, (0, 20*fourmis.index(fourmi) + 50))

            affichage_compte = cpt_font.render(str(compte),True,"Black")
            window.blit(affichage_compte,(0,0))
            if twin :
                window.blit(affichage_sequence,(0,50))
            if not Run :
                window.blit(affichage_pause, (longueur_e - 50, 0))
        if vitesse < 100 or not Run or compte*10%vitesse == 0 : #permet d'aller plus vite en n'affichant pas les dépacements 1 par 1, et affiche instantanément pause
            pygame.display.update()
        clock.tick(vitesse)



class bouton :

    def __init__(self, texte, centre_x, centre_y, couleur = "Brown"):
        self.texte = texte
        self.l, bouton.h = large_font.size(texte)
        self.x = centre_x - self.l/2
        self.y = centre_y - self.h/2
        self.pos = self.x, self.y
        self.surface = large_font.render(texte, True, "White", couleur)

    def collide(self, pos):
        if self.x <= pos[0] and pos[0] <= self.x + self.l and self.y <= pos[1] and pos[1] <= self.y + self.h :
            return True
        return False

#Attention presque tout est mis en variable globale



bouton_retour = bouton(" <--", 20, 20, couleur = "Black")


def OuiNon(phrases, preced):
    bouton_oui = bouton(" OUI ", 200, 300, couleur = (0,120,50))
    bouton_non = bouton(" NON ", 500, 300, couleur = "Brown")
    fond.fill("White")
    window.blit(F_fond_fourmi, (0, 0))
    for i in range(len(phrases)) :
        window.blit(med_font.render(phrases[i], True, "Black"), (100,50+i*40))
    window.blit(bouton_oui.surface,  bouton_oui.pos)
    window.blit(bouton_non.surface,  bouton_non.pos)
    window.blit(bouton_retour.surface,  bouton_retour.pos)
    pygame.display.update()
    while True :
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN :
                if bouton_oui.collide(event.pos) :
                    return True
                if bouton_non.collide(event.pos) :
                    return False
                if bouton_retour.collide(event.pos) :
                    preced()
                    break

def ChoixClavier(texte, inputB, preced):

    while inputB.reponse == None :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and bouton_retour.collide(event.pos) :
                preced()
            inputB.handle_event(event)
        inputB.update()
        window.blit(F_fond_fourmi, (0, 0))
        inputB.draw(window)
        window.blit(bouton_retour.surface,  bouton_retour.pos)
        window.blit(med_font.render(texte, True, "Black"), (100,50))
        pygame.display.update()
    return inputB.reponse

def IdentiquesQuestion():
    phrases = ["Voulez-vous des fourmis suivant des règles différentes?"]
    return not OuiNon(["Voulez-vous des fourmis suivant des règles différentes?"], ChoixFourmi)#il est plus naturel de répondre à la question dans ce sens

def ChoixFourmi():

    global fourmis, nb_fourmi, affichage_sequence

    texte = "Choisissez le nombre de fourmis (recommandé entre 1 et 15)"
    input_fourmi = InputBox(100, 200, 140, 32, "nombre de fourmis souhaité :", exp = "[0-9]+")

    nb_fourmi = int(ChoixClavier(texte, input_fourmi, ChoixVitesse))

    f = open("liste_Prenoms.txt", "r") #fichier contenant des milliers de noms prédéfinis
    noms = []
    for i in range(nb_fourmi):
        noms.append(f.readline().strip()) #attribue le i-ème nom à la i-ème fourmi (pas aléatoire) pour les distinguer
    f.close()
    if nb_fourmi > 1 :
        twin = IdentiquesQuestion()
    else : twin = True
    print(twin)
    if twin :
        input_seq = InputBox(100, 200, 140, 32, "séquence :")
        sequence = ChoixClavier("D: droite, G : gauche, A : avance, R : recule", input_seq, ChoixFourmi)
        affichage_sequence = med_font.render(sequence,True,"Black")
        nb_dep = len(sequence)
        listeCD = [(couleur(i, nb_dep),sequence[i]) for i in range(nb_dep)] #liste contenant tuples (couleur, déplacement associé). Par la suite, on se réferera simplement aux indices pour désigner les couleurs

        print(listeCD)

        fourmis = [ant(sequence, listeCD, noms[k], x = (1+2*k)*(((longueur_e/(nb_fourmi*2))//cote_carre)*cote_carre), y = largeur_e/2) for k in range(nb_fourmi)] #liste des fourmis avec pt de départ répartis uniformément sur la longueur de la fenêtre, en faisant attention à les séparer d'un nombre entier de carreaux
        print("L'équipe est prête !")
        for fourmi in fourmis :
            print(fourmi.nom)

    else :
        fourmis = []
        texte = "D: droite, G : gauche, A : avance, R : recule. Entrez des séquences de même longueur."
        for k in range(nb_fourmi) :
            if k == 0 :
                input_seq = InputBox(100, 200, 140, 32, f"séquence pour {noms[k]} :")
                sequence = ChoixClavier(texte, input_seq, ChoixFourmi)
                nb_dep = len(sequence)
                print(nb_dep)
                couleurs = [couleur(i,nb_dep) for i in range(nb_dep)]
            if k > 0 :
                input_seq = InputBox(100, 200, 140, 32, f"séquence pour {noms[k]} :", exp = "(D|G|A|R){%s}"%nb_dep) #sequence de meme longueur
                print(input_seq.exp)
                sequence = ChoixClavier(texte, input_seq, ChoixFourmi)
            listeCD = [(couleurs[i],sequence[i]) for i in range(nb_dep)]
            fourmis.append(ant(sequence, listeCD, noms[k], x = (1+2*k)*(((longueur_e/(nb_fourmi*2))//cote_carre)*cote_carre), y = largeur_e/2))

    if OuiNon(["Souhaitez-vous choisir les positions initiales ?"],ChoixFourmi) :
        getChoix()
    start(nom_mode, interactif, cote_carre, vitesse, fourmis, twin)



def ChoixVitesse():

    global vitesse

    texte = "La vitesse sera modifiable à l'aide des touches F (faster) et S (slower). "
    input_vitesse = InputBox(100, 200, 140, 32, "vitesse initiale (en fps) :", exp = "[0-9]+")
    vitesse = int(ChoixClavier(texte, input_vitesse, ChoixCarre))
    ChoixFourmi()



def ChoixCarre() :

    global cote_carre
    global ant_img

    boutons = [bouton(" PETIT ", 150, 300, couleur = "Black"), bouton(" MOYEN ", 350, 300, couleur = "Black"), bouton(" GRAND ", 550, 300, couleur = "Black"), bouton_retour]
    window.blit(F_fond_fourmi, (0, 0))
    window.blit(med_font.render("Choississez la taille des carreaux.", True, "Black"), (100,50))
    for B in boutons :
        window.blit(B.surface,  B.pos)
    pygame.display.update()
    A = 0
    while A == 0 :
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN :

                if boutons[0].collide(event.pos) :
                    cote_carre = 2
                    A = 1

                if boutons[1].collide(event.pos) :
                    cote_carre = 10
                    A = 1

                if  boutons[2].collide(event.pos) :
                    cote_carre = 25
                    A = 1

                if bouton_retour.collide(event.pos) :
                    interactifQuestion()
                    A = 2
    if A == 1 :
        #création du dictionnaire contenant les images pour chaque orientation (implémentation à la main), ajustées à la taille des carreaux
        loadAnt(cote_carre)
        ChoixVitesse()

def interactifQuestion():

    global interactif, nom_mode


    phrases = ["Le mode interactif consiste à cliquer sur l'écran pour ajouter des carreaux noirs.", "Si la case est déjà noire, elle devient blanche.", "Souhaitez-vous passer en mode interactif ?"]
    interactif = OuiNon(phrases, ecran_daccueil)
    if interactif :
        nom_mode = "mode interactif"
    else :
        nom_mode = "mode classique"
    ChoixCarre()

def bibliotheque():

    while True :
        #Motifs pour la grille rectangulaire
        boutonsBase = {"DGD" : bouton("DGD", 300, 300, couleur = "Black"), "DGGD" : bouton("DGGD", 300, 350, couleur = "Black"), "GGDD" : bouton("GGDD", 300, 400, couleur = "Black"), "GDDDDDGGD" : bouton(" GDDDDDGGD ", 300, 450, couleur = "Black"),"GGDDDGDGDGGD" : bouton(" GGDDDGDGDGGD ", 550, 300, couleur = "Black"), "DDGGGDGGGDDD" : bouton(" DDGGGDGGGDDD ", 550, 350, couleur = "Black"), "DGGGGDDDGGG" : bouton(" DGGGGDDDGGG ", 550, 400, couleur = "Black"), "GGGGGGGDDDGD" : bouton(" GGGGGGGDDDGD ", 550, 450, couleur = "Black")}
        bouton_hexagone = bouton("L2NNL1L2L1 (bêta)",900, 400, couleur = "Brown")
        bouton_colonies = bouton(" Interaction de 2 colonies ", 500, 500, couleur = "Black")
        window.blit(F_fond_fourmi, (0, 0))
        window.blit(med_font.render("Sélectionner le motif que vous souhaitez visualiser.", True, "Black"), (100,50))
        for B in boutonsBase.values() :
            window.blit(B.surface,  B.pos)
        window.blit(bouton_hexagone.surface,  bouton_hexagone.pos)
        window.blit(bouton_colonies.surface,  bouton_colonies.pos)
        window.blit(bouton_retour.surface,  bouton_retour.pos)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN :
                for seq in boutonsBase.keys() :
                    if boutonsBase[seq].collide(event.pos) :
                        print(seq)
                        app = App(seq)
                        app.run()

                if bouton_hexagone.collide(event.pos):
                    l2nnl1l2l1_ant.App().run()

                if bouton_retour.collide(event.pos) :
                    ecran_daccueil()

                if bouton_colonies.collide(event.pos):
                    colonies_painting_ant.App().run()






def commandes():
    comm = ["A : affiche ou efface les details autres que le fond coloré", "S : ralentit", "F : accélère. Si trop rapide, affichage mis à jour ponctuellement", "espace : met en pause ou relance", "échappe : retourne à l'écran d'acceuil depuis écran fourmis", "x : quitte le programme", "bouton <-- : retourne au paramétrage précédent", "Cliquer sur les zones de texte pour entrer une réponse"]
    window.blit(F_fond_fourmi, (0, 0))
    window.blit(bouton_retour.surface,  bouton_retour.pos)
    for i in range(len(comm)) :
         window.blit(med_font.render(comm[i], True, "Black"), (100,50*(i+1)))
    pygame.display.update()
    while True :
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and bouton_retour.collide(event.pos):
                ecran_daccueil()




def ecran_daccueil():
    bouton_originale = bouton("Fourmi originale", longueur_e/2, largeur_e/2-200)
    bouton_parametres = bouton("Paramètres", longueur_e/2, largeur_e/2 - 100)
    bouton_bibliotheque = bouton("Bibliothèque", longueur_e/2, largeur_e/2)
    bouton_commandes = bouton("Commandes", longueur_e/2, largeur_e/2 + 100)
    pygame.display.set_caption("accueil")
    fond.fill("White")
    window.blit(F_fond_fourmi, (0, 0))
    window.blit(maxi_font.render("FOURMI DE LANGTON", True, "Brown"), (longueur_e/2 - maxi_font.size("ECREAN D'ACCUEIL")[0]/2 , 0))
    window.blit(bouton_originale.surface,  bouton_originale.pos)
    window.blit(bouton_parametres.surface,  bouton_parametres.pos)
    window.blit(bouton_bibliotheque.surface,  bouton_bibliotheque.pos)
    window.blit(bouton_commandes.surface,  bouton_commandes.pos)
    pygame.display.update()
    while True :
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN :
                if bouton_originale.collide(event.pos) :
                    global cote_carre
                    cote_carre = 25
                    loadAnt(25)
                    start("fourmi de Langton originale", False, 30, 1, [ant("DG", [('White', 'D'), ('Black', 'G')], "ami")], False)
                elif bouton_parametres.collide(event.pos) :
                    pygame.display.set_caption("Paramètres")
                    interactifQuestion()
                elif bouton_bibliotheque.collide(event.pos):
                    pygame.display.set_caption("Bibliothèque")
                    bibliotheque()
                elif bouton_commandes.collide(event.pos) :
                    pygame.display.set_caption("Commandes")
                    commandes()



ecran_daccueil()


#problème : compte = 0 trop rapide (à peine visible avant passage à 1)
