#Same program as before but using circle drawing method and placing the ants into tigh groups close to each other
import pygame 
from collections import deque 
from random import choice, randrange

class Ant():
    def __init__(self,app,pos,color):
        self.app = app
        self.color = color
        self.x, self.y = pos
        self.increments = deque([(1,0),(0,1),(-1,0),(0,-1)]) #on utilise deque qui réunit les propriétés de la pile et de la file 
#La fourmi peut se déplacer dans 4 directions; (1,0), (0,1), (-1,0), (0,-1)
#deque provides an O(1) time complexity for append and pop operations as compared to a list that provides O(n) time complexity.
    def run(self): #définition des règles que doit suivre la fourmi pour se déplacer 
        value = self.app.grid[self.y][self.x] #position de la fourmi sur l'écran défini par app
        self.app.grid[self.y][self.x] = not value 

        SIZE = self.app.CELL_SIZE #On dessine non plus des carrés mais des ronds
        center = self.x * SIZE, self.y * SIZE
        if value:
            pygame.draw.circle(self.app.screen, self.color, center, SIZE)


        self.increments.rotate(1) if value else self.increments.rotate(-1) #rotate deque de droite à gauche si 1 et gauche à droite si -1, dépend de la case sur laquelle se trouve la fourmi à la position d'avant
#On peut définir la position initiale de façon random
        dx, dy = self.increments[0] #le premier élément de deque est donc l'incrément du prochain pas de la fourmi 
        self.x = (self.x + dx) % self.app.COLS #pour que la fourmi ne quitte pas les frontières du tableau on prend le reste
        self.y = (self.y + dy) % self.app.ROWS

#On supposera que la fourmi commence son déplacement sur une case blanche 


class App():
    def __init__(self,WIDTH=1375,HEIGHT=715,CELL_SIZE=6,COLOR=(0,0,0),SPEED=120,NUMBER=400):
        pygame.init()
        self.screen = pygame.display.set_mode([WIDTH,HEIGHT])
        self.clock = pygame.time.Clock()
        self.screen.fill(COLOR)
        self.speed = SPEED
        self.number = NUMBER

        self.CELL_SIZE = CELL_SIZE
        self.ROWS, self.COLS = HEIGHT//CELL_SIZE, WIDTH//CELL_SIZE
        self.grid = [[0 for col in range(self.COLS)] for row in range(self.ROWS)]

#On crée 2 groupes de fourmis tels que au sein d'un groupe, les fourmis démarrent toutes du même point
        colors1 = [(250, 150, i) for i in range(256)]
        colors2 = [(50, i, 200) for i in range(256)]
        ants1 = [Ant(self, [self.COLS // 3, self.ROWS // 2],
                     choice(colors1)) for i in range(NUMBER//2)]
        ants2 = [Ant(self, [self.COLS - self.COLS // 3, self.ROWS // 2],
                     choice(colors2)) for i in range(NUMBER//2)]
        self.ant = ants1 + ants2

    @staticmethod
    def get_color():
        channel = lambda: randrange(30,220)
        return channel(), channel(), channel() 

    def run(self):
        while True:
            [ant.run() for ant in self.ant]

            [exit() for i in pygame.event.get() if i.type == pygame.QUIT]
            pygame.display.flip()
            self.clock.tick(self.speed)

if __name__ == '__main__':
    app = App()
    app.run()

#Conclusion de ce test
