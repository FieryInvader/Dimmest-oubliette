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


class Person():
    def __init__(self,x, y, name, health, accuracy, critical, damage,
                 dodge, speed):
        #visuals
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f"images/{name}.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        #stats
        self.hp = health
        self.stress = 0
        self.acc = accuracy
        self.crit = critical
        self.dmg = damage
        self.dodge = dodge
        self.speed = speed
        
class Highwayman(Person):
    def __init__(self, x, y, name):
        #initialize parent class
        self.dmg_range = [i for i in range(5,11)]
        super().__init__(x, y, name, 23 , 0.9, 0.05 , self.dmg_range, 0.14, 7)
        
        
        

run = True
while run:
    clock.tick(FPS)
    
    key = pygame.key.get_pressed()
    
    if key[pygame.K_d]:
        scroll -= 3
        
    if key[pygame.K_a]:
        scroll += 2
    
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