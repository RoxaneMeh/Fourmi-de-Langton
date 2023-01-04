import pygame as pg
import re

pg.init()
screen = pg.display.set_mode((640, 480))
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.Font(None, 32)


class InputBox:

    def __init__(self, x, y, w, h, question, exp = "(D|G|A|R){2,}", text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = COLOR_INACTIVE
        self.color_text = "Black"
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color_text)
        self.active = False
        self.ERREUR = False
        self.exp = exp
        self.aff_question = FONT.render(question, True, "Black")
        self.reponse = None

    def handle_event(self, event):

        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if self.ERREUR :
                    self.text = ''
                    self.color_text = "Black"
                    self.ERREUR = False
                if event.key == pg.K_RETURN:
                    if saisie_motif(self.exp,self.text) == False:
                        self.ERREUR = True
                        self.text = "Saisissez une entrée valide"
                        self.color_text = "Red"

                    else:
                        print(self.text)
                        self.reponse = self.text

                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = FONT.render(self.text, True, self.color_text)


    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.aff_question, (self.x, self.y - self.h))
        screen.blit(self.txt_surface, (self.x+5, self.y+5))
        pg.draw.rect(screen, self.color, self.rect, 2)

def saisie_motif(e, chaine):### expression rationnelle, vérifie zone de texte
    p = re.compile(e)
    m = p.match(chaine)
    if m == None:
        return False
    return m.end() == len(chaine)


def QuestionClavier(input_boxes):
    clock = pg.time.Clock()
    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            for box in input_boxes:
                if box.reponse == None :
                    box.handle_event(event)


        for box in input_boxes:
            box.update()


        screen.fill((30, 30, 30))

        for box in input_boxes:
            box.draw(screen)

        pg.display.flip()
        clock.tick(30)


