import pygame 
from collections import deque 
from random import randrange, choice

# Important dans ce programme: bien définir l'hexagone à construire, doit être cohérent avec directions 
directions = {'N': (0, 1), 'NE': (1, 0), 'SE': (1, -1), 'S': (0, -1), 'SW': (-1, 0), 'NW': (-1, 1)}

sequence = "L2NNL1L2L1"
pattern = []
i = 0
while i < len(sequence):
    if sequence[i] in ('R','L'):
        pattern.append(sequence[i] + sequence[i+1]) 
        i += 2
    else:
        pattern.append(sequence[i])
        i += 1
for l in pattern:
    if l not in ('N','U','R1','R2','L1','L2'):
        raise ValueError("Invalid argument")

def clockwise(letter):
    if letter == 'R1':
        return(1)
    elif letter[0] == 'R2':
        return(2)
    elif letter == 'U':
        return(3)
    elif letter == 'L1':
        return(-1)
    elif letter == 'L2':
        return(-2)
    return(0)

def get_color():
    channel = lambda: randrange(50,255)
    return channel(), channel(), channel() 

def attribute_color(pattern):
    colors = []
    for direction in pattern:
        colors.append(get_color())
    return(colors)
color = attribute_color(pattern)

class Ant():
    def __init__(self,app,pos,color):
        self.app = app
        self.color = color
        self.x, self.y = pos
        self.increments = deque(list(directions.values())) 
        
    def run(self): 
        # Obtenir la valeur actuelle de la cellule 
        value = self.app.grid[self.y][self.x]
        # Modifie la valeur de la cellule ainsi que la couleur
        for i in range(len(pattern)-1):
            if value == i:
                self.app.grid[self.y][self.x] += 1
                self.color = color[i+1]
                self.increments.rotate(clockwise(pattern[i]))
        if value == len(pattern) - 1:
            self.app.grid[self.y][self.x] = 0
            self.color = color[0]
            self.increments.rotate(clockwise(pattern[len(pattern)-1]))
        
        # Dessine la cellule
        SIZE = self.app.CELL_SIZE

        if self.x % 2 == 0:
            x, y = self.x * SIZE + SIZE // 3, (self.y + 1/2) * SIZE + SIZE // 3
        else:
            x, y = self.x * SIZE + SIZE // 3, self.y * SIZE + SIZE // 3
        vertices = [(x, y),(x + SIZE // 3, y), (x + SIZE * 2//3, y + SIZE // 3), (x + SIZE // 3, y + SIZE*2//3), (x, y + SIZE*2//3), (x - SIZE // 3, y + SIZE // 3)]
        pygame.draw.polygon(self.app.screen, self.color, vertices)

        dx, dy = self.increments[0]
        self.x = (self.x + dx) % self.app.COLS 
        self.y = (self.y + dy) % self.app.ROWS

class App():
    def __init__(self,WIDTH=1375,HEIGHT=715,CELL_SIZE=3,COLOR=(0,0,0),SPEED=1000):
        pygame.init()
        self.screen = pygame.display.set_mode([WIDTH,HEIGHT])
        self.clock = pygame.time.Clock()
        self.screen.fill(COLOR)
        self.speed = SPEED

        self.CELL_SIZE = CELL_SIZE
        self.ROWS, self.COLS = HEIGHT//CELL_SIZE, WIDTH//CELL_SIZE
        self.grid = [[0 for col in range(self.COLS)] for row in range(self.ROWS)]

        self.ant = Ant(app=self, pos=[self.COLS//3,self.ROWS//2 + self.ROWS//6],color=color[1]) 

    def run(self):
        while True:
            self.ant.run()

            [exit() for i in pygame.event.get() if i.type == pygame.QUIT]
            pygame.display.flip()
            self.clock.tick(self.speed)

if __name__ == '__main__':
    app = App()
    app.run()