import pygame
import math
import random

pygame.init()

#apply_blight(self,target,damage,rounds)
#apply_bleed(self,target,damage,rounds)
#apply_stun(self,target)


#Classes for our heroes
class Person(pygame.sprite.Sprite):
    def __init__(self,x, y, name, health, critical, dodge, speed, position):
        #visuals
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image = pygame.image.load(f"images/heroes/{name}.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.position = position
        #stats
        self.max_hp = health
        self.current_hp = health
        self.stress = 0
        self.crit = critical
        self.dodge = dodge
        self.speed = speed
        self.dmgmod = 0
        self.deathblow_res = 0.67

        
    def draw(self):
        display.blit(self.image, self.rect)

class Highwayman(Person):
    def __init__(self, x, y, name,position):
        #initialize parent class
        self.hero_class = "Highwayman"
        self.dmg_range = [i for i in range(5,11)]
        self.abilities=["wicked_slice", "pistol_shot", 
                        "grapeshot_blast", "open_vein"]
        super().__init__(x, y, name, 23, 0.05, 0.1, 5,position)
        
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
        
class Crusader(Person):
    def __init__(self, x, y, name, position):
        self.hero_class = "Crusader"
        #initialize parent class
        self.dmg_range = [i for i in range(6,13)]
        self.abilities=["smite", "zealous_accusation", 
                        "stunning_blow", "inspiring_cry"]
        super().__init__(x, y, name, 33, 0.03, 0.05, 1, position)
        
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
        
    def inspiring_cry(self):
        ability_type = 'Util'
        position = [0,1,2,3]
        target = [0,1,2,3]
        #stressheal(target,1)
        
class Plague_Doctor(Person):
    def __init__(self, x, y, name, position):
        self.hero_class = "Plague_Doctor"
        #initialize parent class
        self.dmg_range = [i for i in range(4,8)]
        self.abilities=["noxious_blast", "plague_grenade", 
                        "blinding_gas", "battlefield_medicine"]
        super().__init__(x, y, name, 22, 0.02, 0.01, 7, position)
        
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
        
    def blinding_gas(self):
        ability_type = 'Attack'
        position = [2,3]
        target = (2,3)
        dmg = 0
        crit = 0
        acc = 0.95
        #apply_stun(target)
        
    def battlefield_medicine(self):
        ability_type = 'Util'
        position = [2,3]
        target = [0,1,2,3]
        #heal(target,1)
        #cure(target)
        
class Vestal(Person):
    def __init__(self, x, y, name, position):
        self.hero_class = "Vestal"
        #initialize parent class
        self.dmg_range = [i for i in range(4,9)]
        self.abilities=["dazzling_light", "divine_grace", 
                        "divine_comfort", "judgement"]
        super().__init__(x, y, name, 24, 0.01, 0.01, 4,position)
        
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
        position = [0,1,2,3]
        target = [0,1,2,3]
        dmg = (random.choice(self.dmg_range) + self.dmgmod) * 2
        crit = self.crit * 1.05
        acc = 0.90

#Enemy classes
class Cutthroat(Person):
    def __init__(self,x,y,name,position):
        #fixer pls
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
        
 
    
#Variables
clock = pygame.time.Clock()
FPS = 60
screen_width = 1600
screen_height = 900
bottom_panel = 150
screen = pygame.display
screen.set_caption('Dimmest oubliette')
display = screen.set_mode((screen_width,screen_height))

#Colours
red = (255,0,0)
dark_red = (168,10,10)
yellow = (233,200,85)
grey = (80,80,80) 
black = (0,0,0)
white = (200,200,200)

font = pygame.font.SysFont('Times New Roman', 20)      
 
#Text creation
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    display.blit(img, (x, y))
    
def draw_panel():
    #panels
    left_panel = pygame.image.load("images/panels/left_decor.png")
    right_panel = pygame.image.load("images/panels/right_decor.png")
    panel_hero = pygame.image.load("images/panels/panel_hero.png")
    panel_banner = pygame.image.load("images/panels/panel_banner.png")
    display.blit(left_panel, (0, 575))
    display.blit(right_panel, (1380, 575))
    display.blit(panel_hero, (220, 700))
    display.blit(panel_banner, (194, 580))
    

def draw_hero(hero):
    icon = pygame.image.load(f"images/heroes/{hero.name}_icon.png")
    display.blit(icon, (245, 605))
    draw_text(hero.name, font, yellow, 320, 620)
    draw_text(hero.hero_class, font, grey, 320, 640)
    next_icon = 0 
    for ability in hero.abilities:
        icon = pygame.image.load(f"images/{hero.hero_class}/{ability}.png")
        display.blit(icon, (445 + next_icon, 607))
        next_icon += 62
    icon = pygame.image.load("images/heroes/ability_move.png")
    display.blit(icon, (445 + next_icon, 607))
    next_icon += 62
    icon = pygame.image.load("images/heroes/ability_pass.png")
    display.blit(icon, (445 + next_icon, 607))       
    

class Bandit(Person):
    def __init__(self,x,y,name):
        pass

def draw_text(text, text_col, x, y):
    img = pygame.font.SysFont('Times New Roman', 26).render(text, True, text_col)
    screen.blit(img, x, y)
    
clock = pygame.time.Clock()
FPS = 60
screen_width = 1800
screen_height = 1000
screen = pygame.display
screen.set_caption('Dimmest oubliette')
display = screen.set_mode((screen_width,screen_height))


#load background
bg = pygame.image.load('images/dungeon/hallway2.png')

#Calculate tiles that need to fit in screen + 1 for buffer
tiles = math.ceil(screen_width / bg.get_width()) + 1

#scroll variable for the background scroll
scroll = 0

#hero init (well theyre not bloody villains)
dismas = Highwayman(400, 560,'Dismas',1)
reynauld = Crusader(530,555,'Reynauld',0)
paracelcus = Plague_Doctor(230,560,'Paracelsus',2)
junia = Vestal(100,560,'Junia',3)

#creating a group of sprites for heroes
party = pygame.sprite.Group()
party.add(dismas)
party.add(reynauld)
party.add(paracelcus)
party.add(junia)


        
   
enemy1 = Cutthroat(800, 560, 'cutthroat', 0)        
enemy2 = Cutthroat(900, 560, 'cutthroat', 1)
enemy3 = Fusilier(1000, 560, 'fusilier', 2)
enemy4 = Fusilier(1100, 560, 'fusilier', 3)

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
        
    draw_panel()
    draw_hero(dismas)
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

    enemy1.draw()
    party.draw(display)
    pygame.display.update()

pygame.quit()