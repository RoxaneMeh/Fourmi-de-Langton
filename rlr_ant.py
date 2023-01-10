import pygame 
from collections import deque 
from random import randint

class Ant():
    def __init__(self,app,pos,color):
        self.app = app
        self.color = color
        self.x, self.y = pos
        self.increments = deque([(1,0),(0,1),(-1,0),(0,-1)]) 
        self.increments.rotate(randint(0,3))
    
    def run(self): 
        # Obtenir la valeur actuelle de la cellule 
        value = self.app.grid[self.y][self.x] 
        
        # Modifie la valeur de la cellule ainsi que la couleur
        if value == 0: # White cellule
            self.app.grid[self.y][self.x] = 1
            self.color = pygame.Color('green')
            self.increments.rotate(1)
        elif value == 1: # Green cellule
            self.app.grid[self.y][self.x] = 2
            self.color = pygame.Color('cyan')
            self.increments.rotate(-1)
        elif value == 2: # Cyan cellule
            self.app.grid[self.y][self.x] = 3
            self.color = pygame.Color('purple')
            self.increments.rotate(1)
        
        
        # Dessine la cellule
        SIZE = self.app.CELL_SIZE 
        rect = self.x * SIZE, self.y * SIZE, SIZE - 1, SIZE - 1 
        pygame.draw.rect(self.app.screen, self.color, rect, width=0)

        # Déplacement vers la prochaine cellule
        dx, dy = self.increments[0] 
        self.x = (self.x + dx) % self.app.COLS 
        self.y = (self.y + dy) % self.app.ROWS


class App():
    def __init__(self,WIDTH=1375,HEIGHT=715,CELL_SIZE=6,COLOR=(0,0,0),SPEED=1000):
        pygame.init()
        self.screen = pygame.display.set_mode([WIDTH,HEIGHT])
        self.clock = pygame.time.Clock()
        self.screen.fill(COLOR)
        self.speed = SPEED

        self.CELL_SIZE = CELL_SIZE
        self.ROWS, self.COLS = HEIGHT//CELL_SIZE, WIDTH//CELL_SIZE
        self.grid = [[0 for col in range(self.COLS)] for row in range(self.ROWS)]

        self.ant = Ant(app=self, pos=[self.COLS//2,self.ROWS//2],color=pygame.Color('green')) 

    def run(self):
        while True:
            self.ant.run()

            [exit() for i in pygame.event.get() if i.type == pygame.QUIT]
            pygame.display.flip()
            self.clock.tick(self.speed)

if __name__ == '__main__':
    app = App()
    app.run()