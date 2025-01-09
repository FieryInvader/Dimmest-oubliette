import pygame
import math
import random

pygame.init()

#Colours
red = (255,0,0)
dark_red = (168,10,10)
shit_yellow = (205,150,0)
grey = (80,80,80) 
black = (0,0,0)
white = (200,200,200)

#apply_blight(self,target,damage,rounds)
#apply_bleed(self,target,damage,rounds)
#apply_stun(self,target)

class Person(pygame.sprite.Sprite):
    def __init__(self,x, y, name, health, critical, dodge, speed):
        #visuals
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f"images/heroes/{name}.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        #stats
        self.hp = health
        self.stress = 0
        self.crit = critical
        self.dodge = dodge
        self.speed = speed
        self.dmgmod = 0
        self.deathblow_res = 0.67
        
        
class Highwayman(Person):
    def __init__(self, x, y, name):
        #initialize parent class
        self.dmg_range = [i for i in range(5,11)]
        super().__init__(x, y, name, 23, 0.05, 0.1, 5)
        
    def wicked_slice(self):
        ability_type = 'Attack'
        position = [0,1,2]
        target = [0,1]
        dmg = (random.choice(self.dmg_range) + self.dmgmod) * 1.15
        crit = self.crit * 1.05
        acc = 0.85
        
    def pistol_shot(self):
        ability_type = 'Attack'
        position = [1,2,3]
        target = [1,2,3]
        dmg = (random.choice(self.dmg_range) + self.dmgmod) * 0.85
        crit = self.crit * 1.075
        acc = 0.85
        
    def grapeshot_blast(self):
        ability_type = 'Attack'
        position = [1,2]
        target = (0,1,2)
        dmg = (random.choice(self.dmg_range) + self.dmgmod) * 0.5
        crit = self.crit * 0.91
        acc = 0.75
        
    def open_vein(self):
        ability_type = 'Attack'
        position = [0,1,2]
        target = [0,1]
        dmg = (random.choice(self.dmg_range) + self.dmgmod) * 0.85
        crit = self.crit * 1
        acc = 0.95
        #apply_bleed(target,dmg,rounds)
        
    def take_aim(self):
        ability_type = 'Util'
        position = [0,1,2,3]
        self.acc += 0.15
        self.dmgmod = 2
        self.crit = self.crit + 0.2
        self.speed += 2
        
class Crusader(Person):
    def __init__(self, x, y, name):
        #initialize parent class
        self.dmg_range = [i for i in range(6,13)]
        super().__init__(x, y, name, 33, 0.03, 0.05, 1)
        
    def smite(self):
        ability_type = 'Attack'
        position = [0,1]
        target = [0,1]
        dmg = (random.choice(self.dmg_range) + self.dmgmod) * 1
        crit = self.crit
        acc = 0.85
        
    def zealous_accusation(self):
        ability_type = 'Attack'
        position = [0,1]
        target = (0,1)
        dmg = (random.choice(self.dmg_range) + self.dmgmod) * 0.5
        crit = self.crit - 0.04
        acc = 0.85
        
    def stunning_blow(self):
        ability_type = 'Attack'
        position = [0,1]
        target = [0,1]
        dmg = (random.choice(self.dmg_range) + self.dmgmod) * -0.5
        crit = self.crit 
        acc = 0.9
        
    def battle_heal(self):
        ability_type = 'Util'
        position = [0,1,2,3]
        target = [0,1,2,3]
        #heal(target,3)
        
    def inspiring_cry(self):
        ability_type = 'Util'
        position = [0,1,2,3]
        target = [0,1,2,3]
        #stressheal(target,1)
        
class Plague_Doctor(Person):
    def __init__(self, x, y, name):
        #initialize parent class
        self.dmg_range = [i for i in range(4,8)]
        super().__init__(x, y, name, 22, 0.02, 0.01, 7)
        
    def noxious_blast(self):
        ability_type = 'Attack'
        position = [1,2,3]
        target = [0,1]
        dmg = (random.choice(self.dmg_range) + self.dmgmod) * 0.2
        crit = self.crit * 1.05
        acc = 0.95
        #apply_blight(target,5,3)
        
    def plague_grenade(self):
        ability_type = 'Attack'
        position = [2,3]
        target = (2,3)
        dmg = (random.choice(self.dmg_range) + self.dmgmod) * 0.1
        crit = self.crit * 1
        acc = 0.95
        #apply_blight(target,4,3)
        
    def plague_grenade(self):
        ability_type = 'Attack'
        position = [2,3]
        target = (2,3)
        dmg = 0
        crit = 0
        acc = 0.95
        #apply_stun(target)
        
    def incision(self):
        ability_type = 'Attack'
        position = [0,1,2]
        target = [0,1]
        dmg = (random.choice(self.dmg_range) + self.dmgmod) * 1
        crit = self.crit * 1.05
        acc = 0.85
        #apply_bleed(target,2,3)
        
    def battlefield_medicine(self):
        ability_type = 'Util'
        position = [2,3]
        target = [0,1,2,3]
        #heal(target,1)
        #cure(target)
        
class Vestal(Person):
    def __init__(self, x, y, name):
        #initialize parent class
        self.dmg_range = [i for i in range(4,9)]
        super().__init__(x, y, name, 24, 0.01, 0.01, 4)
        
    def dazzling_light(self):
        ability_type = 'Attack'
        position = [1,2,3]
        target = [0,1,2]
        dmg = (random.choice(self.dmg_range) + self.dmgmod) * 0.25
        crit = self.crit * 1.05
        acc = 0.90
        #apply_stun(target)
        
    def divine_grace(self):
        ability_type = 'Util'
        position = [2,3]
        target = [0,1,2,3]
        #heal(target,5)
        
    def divine_comfort(self):
        ability_type = 'Util'
        position = [2,3]
        target = (0,1,2,3)
        #heal(target,5)
        
    def judgement(self):
        ability_type = 'Attack'
        position = [2,3]
        target = (0,1,2,3)
        dmg = (random.choice(self.dmg_range) + self.dmgmod) * 0.5
        crit = self.crit * 1.05
        acc = 0.85
        
    def illumination(self):
        ability_type = 'Attack'
        position = [0,1,2,3]
        target = [0,1,2,3]
        dmg = (random.choice(self.dmg_range) + self.dmgmod) * 2
        crit = self.crit * 1.05
        acc = 0.90

class Bandit(Person):
    def __init__(self,x,y,name):
        pass

def draw_text(text, text_col, x, y):
    img = pygame.font.SysFont('Times New Roman', 26).render(text, True, text_col)
    screen.blit(img, x, y)
    
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
dismas = Highwayman(400, 560,'dismas')
reynauld = Crusader(530,555,'reynauld')
paracelcus = Plague_Doctor(230,560,'paracelsus')
junia = Vestal(100,560,'junia')

#creating a group of sprites for heroes
party = pygame.sprite.Group()
party.add(dismas)
party.add(reynauld)
party.add(paracelcus)
party.add(junia)



=======
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

>>>>>>> 28cd73204d5f87db91fff00af67fd9b2d740640d
        
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