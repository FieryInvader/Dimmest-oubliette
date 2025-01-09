import pygame
import math

pygame.init()

class Square(pygame.sprite.Sprite):     #Note: create specific hero classes for abilities and stuff
    def __init__(self, x, y,name):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f"images/{name}.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    # def update(self):
    #     if key[pygame.K_d]:
    #         self.rect.move_ip(1, 0)
    #     elif key[pygame.K_a]:
    #         self.rect.move_ip(-1,0)

clock = pygame.time.Clock()
FPS = 60
screen_width = 1500
screen_height = 900
screen = pygame.display
screen.set_caption('Dimmest oubliet')
display = screen.set_mode((screen_width,screen_height))



bg = pygame.image.load('images/hallway2.png')

tiles = math.ceil(screen_width / bg.get_width()) + 1

scroll = 0

dismas = Square(400, 560,'dismas')
reynauld = Square(530,555,'reynauld')
paracelcus = Square(230,560,'paracelsus')
junia = Square(100,560,'junia')


party = pygame.sprite.Group()
party.add(dismas)
party.add(reynauld)
party.add(paracelcus)
party.add(junia)

run = True
while run:
    clock.tick(FPS)
    
    key = pygame.key.get_pressed()
    
    if key[pygame.K_d]:
        scroll -= 0.8
    
    for i in range(0,tiles):
        display.blit(bg, (i * bg.get_width() + scroll,0))
        
    
    if abs(scroll) > bg.get_width():
        scroll = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False




    party.draw(display)
    pygame.display.update()

pygame.quit()