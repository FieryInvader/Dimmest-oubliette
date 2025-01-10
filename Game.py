import pygame
import math
import random

pygame.init()

def apply_dmg(target,dmg):
    if target.current_hp - dmg < 0:
        target.current_hp = 0
    else:
        target.current_hp -= dmg
        
def apply_blight(target,damage,rounds):
    target.blight.append((damage,rounds))
    indicator = [0,0]
    for b in target.blight:
        indicator[0] += b[0]
        indicator[1] += b[1]
    return indicator
    
def apply_bleed(target,damage,rounds):
    target.bleed.append((damage,rounds))
    indicator = [0,0]
    for b in target.bleed:
        indicator[0] += b[0]
        indicator[1] += b[1]
    return indicator

#apply_stun(self,target)

#button class
class Button():
    def __init__(self, surface, x, y, image, ability, ability_pass = False):
        self.x = x
        self.y = y
        self.ability = ability
        self.ability_pass = ability_pass
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.surface = surface
        
    def draw(self):
        #draw button
        self.surface.blit(self.image, (self.rect.x, self.rect.y))
        
        action = False
		#get mouse position
        pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
        if self.rect.collidepoint(pos): #ON HOVER
            if self.ability_pass == False:
                icon = pygame.image.load("images/heroes/focused_ability.png")
                display.blit(icon, (self.x-15, self.y-15)) 
            else:
                icon = pygame.image.load("images/heroes/focused_pass.png")
                display.blit(icon, (self.x-36, self.y-15)) 
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: #on click
                action = True
                self.clicked = True

        # if pygame.mouse.get_pressed()[0] == 0:
        #     self.clicked = False

        if self.clicked == True:
            if self.ability_pass == False:
                self.ability.selected()
            else:
                icon = pygame.image.load("images/heroes/selected_pass.png")
                display.blit(icon, (self.x-32, self.y-15)) 

        return action 

#Colours
red = (255,0,0)
dark_red = (168,10,10)
yellow = (233,200,85)
grey = (200,200,200) 
black = (0,0,0)
white = (200,200,200)
dark_grey = (100,100,100)

empty_stress = pygame.image.load("images/heroes/stress_empty.png")
full_stress = pygame.image.load("images/heroes/stress_full.png")

#Classes for our heroes
class Person(pygame.sprite.Sprite):
    def __init__(self, x, y, name, health, critical, dodge, speed, position):
        #visuals
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
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
        self.blight = []
        self.bleed = []
        self.deathblow_res = 0.67

        
    def draw(self,hp, flip = False):
        self.current_hp = hp
        ratio = self.current_hp / self.max_hp
        if flip == True:
            display.blit(pygame.transform.flip(self.image, True, False), self.rect)
            pygame.draw.rect(display, dark_grey, (self.x-40,self.y+150,100,10))
            pygame.draw.rect(display, red, (self.x-40,self.y+150,100*ratio,10))
        else:
            display.blit(self.image, self.rect)
            pygame.draw.rect(display, dark_grey, (self.x-40,self.y+150,100,10))
            pygame.draw.rect(display, red, (self.x-40,self.y+150,100*ratio,10))
            for i in range(11):
                display.blit(empty_stress, (self.x-40+i*9.5,self.y+160))
            for i in range(self.stress):
                display.blit(full_stress, (self.x-40+i*9.5,self.y+160))
            
class ability():
    def __init__(self,name,position,target,dmg,Type,crit,accuracy,status = '', rounds = 0,dot = 0, cure = False):
        self.name = name
        self.position = position
        self.target = target
        self.dmg = dmg
        self.Type = Type
        self.crit = crit
        self.accuracy = accuracy
        self.status = status
        self.rounds = rounds
        self.dot = dot
        self.cure = cure
        
    def selected(self):
        icon = pygame.image.load("images/heroes/selected_ability.png")
        display.blit(icon, (self.x-15, self.y-15)) 
        for t in self.target:
            target_icon = pygame.image.load("images/targets/target_1.png")
            display.blit(target_icon, (900 + 150*t, 450))
        
        
        

class Highwayman(Person):
    def __init__(self, x, y, name,position):
        #initialize parent class
        self.hero_class = "Highwayman"
        self.dmg_range = [i for i in range(5,11)]
        super().__init__(x, y, name, 23, 0.05, 0.1, 5,position)
        
        self.abilities = []
        self.wicked_slice = ability('wicked_slice',[0,1,2],[0,1],math.floor(random.choice(self.dmg_range) + self.dmgmod) * 1.15,'Attack',self.crit*1.05,0.85)
        self.pistol_shot = ability('pistol_shot',[0,1,2],[0,1],math.floor(random.choice(self.dmg_range) + self.dmgmod) * 0.85,'Attack',self.crit*1.075,0.85)
        self.grapeshot_blast = ability('grapeshot_blast',[1,2],[(0,1,2)],math.floor(random.choice(self.dmg_range) + self.dmgmod) * 0.5,'Attack',self.crit*0.91,0.75)        
        self.open_vein = ability('open_vein',[0,1,2],[0,1],math.floor(random.choice(self.dmg_range) + self.dmgmod) * 0.85,'Attack',self.crit,0.95,status = 'Bleed',rounds = 2, dot = 3)
        self.take_aim = ability('take_aim',[0,1,2,3],[1],2,'Util',0.1,2)        #last arguement will add speed to dismas
        
        self.abilities.append(self.wicked_slice)
        self.abilities.append(self.pistol_shot)
        self.abilities.append(self.grapeshot_blast)
        self.abilities.append(self.open_vein)
        self.abilities.append(self.take_aim)
        
class Crusader(Person):
    def __init__(self, x, y, name, position):
        self.hero_class = "Crusader"
        #initialize parent class
        self.dmg_range = [i for i in range(6,13)]
        super().__init__(x, y, name, 33, 0.03, 0.05, 1, position)
        
        self.abilities = []
        self.smite = ability('smite',[0,1], [0,1],random.choice(self.dmg_range) + self.dmgmod , 'Attack', self.crit,0.85)
        self.zealous_accusation = ability('zealous_accusation',[0,1],[(0,1)],math.floor((random.choice(self.dmg_range)+self.dmgmod)* 0.6),'Attack',self.crit*0.96,0.85)
        self.stunning_blow = ability('stunning_blow',[0,1],[0,1],math.floor((random.choice(self.dmg_range) + self.dmgmod) * 0.5),'Attack',self.crit,0.9)
        self.inspiring_cry = ability('ispiring_cry',[0,1,2,3],[0,1,2,3],1,'Util',self.crit,1)
        self.battle_heal = ability('battle_heal',[0,1,2,3],[0,1,2,3],random.choice([2,3]),'Util',self.crit,1)
      
        self.abilities.append(self.smite)
        self.abilities.append(self.zealous_accusation)
        self.abilities.append(self.stunning_blow)
        self.abilities.append(self.inspiring_cry)
        self.abilities.append(self.battle_heal)
        
class Plague_Doctor(Person):
    def __init__(self, x, y, name, position):
        self.hero_class = "Plague_Doctor"
        #initialize parent class
        self.dmg_range = [i for i in range(4,8)]
        super().__init__(x, y, name, 22, 0.02, 0.01, 7, position)
        
        self.abilities = []
        self.noxious_blast = ability("noxious_blast",[1,2,3],[0,1],math.floor(random.choice(self.dmg_range) + self.dmgmod) * 0.2,'Attack',self.crit,0.95,status = 'Blight',rounds = 3,dot= 5 )
        self.plague_grenade = ability("plague_grenade", [1,2,3],[(2,3)],math.floor(random.choice(self.dmg_range) + self.dmgmod) * 0.1,'Attack',self.crit,0.95,status = 'Blight',rounds = 3,dot= 4 )
        self.blinding_gas = ability("blinding_gas",[2,3],[(2,3)],0,'Attack',0,0.95,status = 'Stun')        
        self.battlefield_medicine = ability("battlefield_medicine",[2,3],[0,1,2,3],1,'Util',self.crit,1)
        self.incision = ability('incision',[0,1,2],[0,1],math.floor(random.choice(self.dmg_range) + self.dmgmod),'Attack',self.crit*1.05,status = 'Bleed', rounds = 3, dot = 2)
             
        self.abilities.append(self.noxious_blast)
        self.abilities.append(self.plague_grenade)
        self.abilities.append(self.blinding_gas)
        self.abilities.append(self.battlefield_medicine)
        self.abilities.append(self.incision)
        
class Vestal(Person):
    def __init__(self, x, y, name, position):
        self.hero_class = "Vestal"
        #initialize parent class
        self.dmg_range = [i for i in range(4,9)]
        super().__init__(x, y, name, 24, 0.01, 0.01, 4,position)
        
        self.abilities = []
        self.dazzling_light = ability("dazzling_light",[1,2,3],[0,1,2],math.floor(random.choice(self.dmg_range) + self.dmgmod) * 0.25,'Attack',self.crit*1.05,0.9,status = 'Stun')
        self.divine_grace = ability("divine_grace",[2,3],[0,1,2,3],random.choice(range(4,6)),'Util',self.crit,1)
        self.divine_comfort = ability("divine_comfort", [2,3],[(0,1,2,3)],random.choice(range(1,4)),'Util',self.crit,1)
        self.judgement = ability("judgement",[0,1,2,3],[(2,3)],math.floor(random.choice(self.dmg_range) + self.dmgmod) * 0.5,'Attack',self.crit*1.05,0.85)
        self.illumination = ability('illumination',[0,1,2,3],[0,1,2,3],math.floor(random.choice(self.dmg_range) + self.dmgmod),'Attack',self.crit,0.9)
        
        self.abilities.append(self.dazzling_light)
        self.abilities.append(self.divine_grace)
        self.abilities.append(self.divine_comfort)
        self.abilities.append(self.judgement)
        self.abilities.append(self.illumination)
        
#Enemy classes
class Cutthroat(Person):
    def __init__(self,x,y,name,position):
        #fixer pls
        super().__init__(x, y, name, 12, 0.12, 0.025, 3, position)
        
        self.Slice_and_dice = ability('Slice_and_dice',[0,1,2],[(0,1)],random.choice(range(3,6)),'Attack',self.crit,0.725)
        self.Uppercut_Slice = ability('Uppercut_Slice',[0,1],[0,1],random.choice(range(2,5)),'Attack',0.05,0.725)
        self.Shank = ability('Shank',[0,1,2],[0,1,2,3],random.choice(range(4,9)),'Attack',0.06,0.725,status = 'Bleed',rounds = 3,dot = 2)
        
        self.abilities =[]
        self.abilities.append(self.Slice_and_dice)
        self.abilities.append(self.Uppercut_Slice)
        self.abilities.append(self.Shank)

class Fusilier(Person):
    def __init__(self, x, y, name,position):
        super().__init__(x,y,name,12,0.01,0.075,6,position)
        self.abilities = []
        self.Blanket = ability('Blanket',[1,2,3],[(0,1,2,3)],random.choice(range(1,6)),'Attack',0.02,0.725)
        self.abilities.append(self.Blanket)

    
#Variables
clock = pygame.time.Clock()
FPS = 60
screen_width = 1600
screen_height = 900
bottom_panel = 150
screen = pygame.display
screen.set_caption('Dimmest oubliette')
display = screen.set_mode((screen_width,screen_height))


font = pygame.font.SysFont('Comic sans', 20) 
font_small = pygame.font.SysFont('Comic sans', 16)    
font_med = pygame.font.SysFont('Comic sans', 18)
 
#Text creation
def draw_text(text, font, colour, x, y):
    img = font.render(text, True, colour)
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
    #hero icon
    icon = pygame.image.load(f"images/heroes/{hero.name}_icon.png")
    display.blit(icon, (245, 605))
    draw_text(hero.name, font, yellow, 320, 620)
    draw_text(hero.hero_class, font, grey, 320, 640)
    next_icon = 0 # pixels to space out buttons
    img_list = []
    #make ability buttons
    for ability in hero.abilities:
        img = pygame.image.load(f"images/{hero.hero_class}/{ability.name}.png")
        img_list.append(img)
    ability0 = Button(display, 445 + next_icon, 607, img_list[0], hero.abilities[0])
    ability0.draw()
    next_icon += 62
    ability1 = Button(display, 445 + next_icon, 607, img_list[1], hero.abilities[1])
    ability1.draw()
    next_icon += 62
    ability2 = Button(display, 445 + next_icon, 607, img_list[2], hero.abilities[2])
    ability2.draw()
    next_icon += 62
    ability3 = Button(display, 445 + next_icon, 607, img_list[3], hero.abilities[3])
    ability3.draw()
    next_icon += 62
    img = pygame.image.load("images/heroes/ability_move.png")
    move = Button(display, 445 + next_icon, 607, img)
    move.draw()
    next_icon += 62
    img = pygame.image.load("images/heroes/ability_pass.png")
    ability_pass = Button(display, 445 + next_icon, 607, img, True)
    ability_pass.draw()
    next_icon += 62  
    
    #hero stats 
    draw_text(f"{hero.current_hp}/{hero.max_hp}", font_small, dark_red, 310, 707)
    draw_text(f"{hero.stress}/10", font_small, grey, 310, 730)
    draw_text("ACC", font_med, grey, 260, 760)
    draw_text("CRIT", font_med, grey, 260, 780)
    draw_text("DMG", font_med, grey, 260, 800)
    draw_text("DODGE", font_med, grey, 260, 820)
    draw_text("SPD", font_med, grey, 260, 840)
    
    

#load background
bg = pygame.image.load('images/dungeon/hallway2.png')

#Calculate tiles that need to fit in screen + 1 for buffer
tiles = math.ceil(screen_width / bg.get_width()) + 1

#scroll variable for the background scroll
scroll = 0

#hero init (well theyre not bloody villains)
dismas = Highwayman(400, 400,'Dismas',1)
reynauld = Crusader(530,400,'Reynauld',0)
paracelcus = Plague_Doctor(230,400,'Paracelsus',2)
junia = Vestal(100,400,'Junia',3)

#creating a group of sprites for heroes
party = []
party.append(dismas)
party.append(reynauld)
party.append(paracelcus)
party.append(junia)

   
enemy1 = Cutthroat(900, 410, 'cutthroat', 0)        
enemy2 = Cutthroat(1050, 410, 'cutthroat', 1)
enemy3 = Fusilier(1200, 410, 'fusilier', 2)
enemy4 = Fusilier(1350, 410, 'fusilier', 3)

enemy_list = []
enemy_list.append(enemy1)
enemy_list.append(enemy2)
enemy_list.append(enemy3)
enemy_list.append(enemy4)


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
            initiative = []
            while fighting:
                for member in party:
                    initiative.append((random.choice(range(9)) + member.speed,0,member.position))
                for enemy in enemy_list:
                    initiative.append((random.choice(range(9)) + enemy.speed,1,enemy.position))
                initiative.sort(key = lambda tup: tup[1])
                print(initiative)
                fighting = False
            
            
#Testing, move this code inside the combat
    for enemy in enemy_list:
        enemy.draw(enemy.current_hp,flip=True)
    
    for member in party:
        member.draw(member.current_hp)
    pygame.display.update()

pygame.quit()