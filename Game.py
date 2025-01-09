import pygame
import math
import random

pygame.init()

class Square(pygame.sprite.Sprite):     #Note: create specific hero classes for abilities and stuff
    def __init__(self, x, y,name):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f"images/heroes/{name}.png")
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


#load background
bg = pygame.image.load('images/dungeon/hallway2.png')

#Calculate tiles that need to fit in screen + 1 for buffer
tiles = math.ceil(screen_width / bg.get_width()) + 1

#scroll variable for the background scroll
scroll = 0

#hero init
dismas = Square(400, 560,'dismas')
reynauld = Square(530,555,'reynauld')
paracelcus = Square(230,560,'paracelsus')
junia = Square(100,560,'junia')

#creating a group of sprites for heroes
party = pygame.sprite.Group()
party.add(dismas)
party.add(reynauld)
party.add(paracelcus)
party.add(junia)


class Person():
    def __init__(self,x, y, name, health, critical,
                 dodge, speed,position):
        #visuals
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f"images/{name}.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.position = position
        #stats
        self.hp = health
        self.stress = 0
        self.crit = critical
        self.dodge = dodge
        self.speed = speed
        self.dmgmod = 0
        
class Highwayman(Person):
    def __init__(self, x, y, name, position):
        #initialize parent class
        self.dmg_range = [i for i in range(5,11)]
        super().__init__(x, y, name, 23 , 0.9, 0.05 , 0.14, 7,position)
        
    def wicked_slice(self):
        position = [0,1]
        target = [0,1]
        dmg = (random.choice(self.dmg_range) + self.dmgmod) * 1.15
        crit = self.crit + 0.05
        acc = self.acc  - 0.1
        
    def pistol_shot(self):
        position = [1,2,3]
        target = [1,2,3]
        dmg = (random.choice(self.dmg_range) + self.dmgmod) * 0.95
        crit = self.crit + 0.075
        acc = self.acc - 0.05
        
    def grapeshot_blast(self):
        position = [1,2]
        target = (0,1,2)
        dmg = (random.choice(self.dmg_range) + self.dmgmod) * -0.4
        crit = self.crit - 0.09
        acc = self.acc - 0.2
        
    def open_vein(self):
        position = [0,1,2]
        target = [0,1]
        dmg = (random.choice(self.dmg_range) + self.dmgmod) * -0.15
        crit = 0
        acc = self.acc
        #apply_bleed(target)
        
    def take_aim(self):
        position = [0,1,2,3]
        self.acc += 0.15
        self.dmgmod = 2
        self.crit = self.crit + 0.2
        self.speed += 2

class Cutthroat(Person):
    def __init__(self,x,y,name,position):
        super().__init__(x, y, name, 12, 0.725, 0.12,0.025, 3, position)

        
    def Slice_and_dice(self):
        self_tile = [0,1,2]
        target = (0,1)
        dmg = random.choice(range(3,6))
        crit = 0.12
        
    def Uppercut_Slice(self):
        self_tile = [0,1]
        target = [0,1]
        dmg = random.choice(range(2,5))
        crit = 0.06

    def Shank(self):
        self_tile = [0,1,2]
        target = [0,1,2,3]
        dmg = random.choice(range(4,9))
        crit = 0.06
        #apply_bleed(target,ammount,duration)

class Fusilier(Person):
    def __init__(self, x, y, name,position):
        super().__init__(x,y,name,12,0.725,0.01,0.075,6)
        
    def Blanket(self):
        self_tile = [1,2,3]
        target = (0,1,2,3)
        dmg = random.choice(range(1,5))
        crit = 0.02
        
COMBAT = pygame.USEREVENT + 1
tile_size = 1000
party_position = 0
map_tiles = [0,0,1,0,2,1]
#main game loop
run = True
while run:
    clock.tick(FPS)
    
    key = pygame.key.get_pressed()
    #update scroll only when d is pressed
    if key[pygame.K_d]:
        scroll -= 3
        party_position += 3
        
    if key[pygame.K_a]:
        scroll += 2
        party_position -= 2

    
    #insert the background image into the screen queue while scrolling
    for i in range(0,tiles):
        display.blit(bg, (i * bg.get_width() + scroll,0))
        
    # Check for battle triggers
    current_tile = party_position // tile_size  # Calculate which tile the player is on (round down)
    if map_tiles[current_tile] == 1:
        pygame.event.post(pygame.event.Event(COMBAT))
        
    
    #When we have scrolled past the screen reset the queue
    if abs(scroll) > bg.get_width():
        scroll = 0
    for event in pygame.event.get():
        fighting = False
        if event.type == pygame.QUIT:
            run = False
        if event.type == COMBAT:
            fighting = True
            while fighting:
                pass




    party.draw(display)
    pygame.display.update()

pygame.quit()