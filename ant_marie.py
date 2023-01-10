import pygame
from collections import deque
from random import randrange


def clockwise(letter):
    if letter == 'D':
        return(1)
    elif letter == 'G':
        return(-1)
    return(0)

def get_color():
    channel = lambda: randrange(50,220)
    return channel(), channel(), channel()

def attribute_color(pattern):
    colors = []
    for direction in pattern:
        colors.append(get_color())
    return(colors)

class Ant():
    def __init__(self,seq,app,pos):
        self.app = app
        self.pattern = list(seq)
        self.colorList = attribute_color(self.pattern)
        self.color = self.colorList[1]
        self.x, self.y = pos
        self.increments = deque([(1,0),(0,1),(-1,0),(0,-1)])
        self.increments.rotate(1)

    def run(self):
        # Obtenir la valeur actuelle de la cellule
        value = self.app.grid[self.y][self.x]
        # Modifie la valeur de la cellule ainsi que la couleur
        for i in range(len(self.pattern)-1):
            if value == i:
                self.app.grid[self.y][self.x] += 1
                self.color = self.colorList[i+1]
                self.increments.rotate(clockwise(self.pattern[i]))
        if value == len(self.pattern) - 1:
            self.app.grid[self.y][self.x] = 0
            self.color = self.colorList[0]
            self.increments.rotate(clockwise(self.pattern[len(self.pattern)-1]))

        # Dessine la cellule
        SIZE = self.app.CELL_SIZE
        rect = self.x * SIZE, self.y * SIZE, SIZE - 1, SIZE - 1
        pygame.draw.rect(self.app.screen, self.color, rect, width=0)

        # Déplacement vers la prochaine cellule
        dx, dy = self.increments[0]
        self.x = (self.x + dx) % self.app.COLS
        self.y = (self.y + dy) % self.app.ROWS


class App():
    def __init__(self,seq,CELL_SIZE=6,COLOR=(0,0,0),SPEED=100000000):
        pygame.init()
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        WIDTH, HEIGHT = self.screen.get_size()
        self.clock = pygame.time.Clock()
        self.screen.fill(COLOR)
        self.speed = SPEED

        self.CELL_SIZE = CELL_SIZE
        self.ROWS, self.COLS = HEIGHT//CELL_SIZE, WIDTH//CELL_SIZE
        self.grid = [[0 for col in range(self.COLS)] for row in range(self.ROWS)]

        self.ant = Ant(seq, app=self, pos=[self.COLS//2,self.ROWS//2])

    def run(self):
        A = 1
        while A == 1:
            self.ant.run()

            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE :
                    A = 0

            pygame.display.flip()
            self.clock.tick(self.speed)

#if __name__ == '__main__':
    #app = App("DG")
    #app.run()
