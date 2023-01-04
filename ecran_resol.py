import pygame as pg
import re

pg.init()
screen = pg.display.set_mode((640, 480))
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.Font(None, 32)


class InputBox:

    def __init__(self, x, y, w, h, exp = "(D|G|A|R){2,}", text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = COLOR_INACTIVE
        self.color_text = "White"
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color_text)
        self.active = False
        self.ERREUR = False
        self.exp = exp

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
                    self.color_text = "White"
                    self.ERREUR = False
                if event.key == pg.K_RETURN:
                    if saisie_motif(self.exp,self.text) == False:
                        self.ERREUR = True
                        self.text = "Saisissez une entrée valide"
                        self.color_text = "Red"

                    else:
                        print(self.text)
                        self.ERREUR = False
                        self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = FONT.render(self.text, True, self.color_text)
        

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)

def saisie_motif(e, chaine):### expression rationnelle, vérifie zone de texte
    p = re.compile(e)
    m = p.match(chaine)
    if m == None:
        return False
    return m.end() == len(chaine)
    
        

def main():
    clock = pg.time.Clock()
    input_box1 = InputBox(100, 100, 140, 32)
    input_box2 = InputBox(100, 150, 140, 32)
    input_box3 = InputBox(100, 200, 140, 32, exp = "[0-9]+")
    input_boxes = [input_box1, input_box2, input_box3]
    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            for box in input_boxes:
                box.handle_event(event)
                

        for box in input_boxes:
            box.update()
            

        screen.fill((30, 30, 30))
        
        for box in input_boxes:
            box.draw(screen)

        pg.display.flip()
        clock.tick(30)

if __name__ == '__main__':
    main()
    pg.quit()


#https://coderslegacy.com/python/text-input-box-in-pygame/