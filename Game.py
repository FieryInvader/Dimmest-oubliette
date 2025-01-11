import pygame
import math
import random
import time

pygame.init()

#button class
class Button(pygame.sprite.Sprite):
    def __init__(self, surface, x, y, image, ability):
        self.x = x
        self.y = y
        self.ability = ability
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.surface = surface
        
        
    def draw(self):
        self.surface.blit(self.image, (self.rect.x, self.rect.y))
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos): #ON HOVER
            if self.ability != "pass":
                icon = pygame.image.load("images/heroes/focused_ability.png")
                display.blit(icon, (self.x-15, self.y-15))
            else:
                icon = pygame.image.load("images/heroes/focused_pass.png")
                display.blit(icon, (self.x-36, self.y-15))
            
    # CHECK PASS ACTION!!!!!!!!!!!!!!!!!!!!!!!

#functions that draw stuff
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
        if ability.Type != 'Pass':
            img = pygame.image.load(f"images/{hero.hero_class}/{ability.name}.png")
            img_list.append(img)
    ability0 = Button(display, 445 + next_icon, 607, img_list[0], ability = hero.abilities[0])
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
    ability4= Button(display, 445 + next_icon, 607, img_list[4], hero.abilities[4])
    ability4.draw()
    next_icon += 62
    img = pygame.image.load("images/heroes/ability_pass.png")
    ability_pass = Button(display, 445 + next_icon, 607, img, hero.abilities[5])
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
    dodge = hero.dodge * 100
    draw_text(f"{dodge}%", font_med, grey, 350, 820)
    draw_text(f"{hero.speed}", font_med, grey, 350, 840)
    
    return [ability0, ability1, ability2, ability3, ability4, ability_pass]

def draw_target(target):
    draw_target_overlay()
    #hero icon
    draw_text(target.name, font, yellow, 320, 620)
    draw_text(target.hero_class, font, grey, 320, 640)
    
    #hero stats 
    draw_text(f"{target.current_hp}/{target.max_hp}", font_small, dark_red, 310, 707)
    draw_text(f"{target.stress}/10", font_small, grey, 310, 730)
    draw_text("DODGE", font_med, grey, 260, 820)
    draw_text("SPD", font_med, grey, 260, 840)
    dodge = target.dodge * 100
    draw_text(f"{dodge}%", font_med, grey, 350, 820)
    draw_text(f"{target.speed}", font_med, grey, 350, 840)

def draw_ability(hero, button):
    #draw selected ability
    icon = pygame.image.load("images/heroes/selected_ability.png") #BLINKER KURWA
    display.blit(icon, (button.x-15, button.y-15))
    abil = pygame.image.load("images/targets/ability_stats.png") 
    display.blit(abil, (445, 710))
    #print ability name and any effects it causes
    name = button.ability.name
    name = name.capitalize()
    name = name.replace("_", " ")
    draw_text(f"{name}", font_med, white, 460, 715)
    if button.ability.Type == "Attack":
        #draw ability stats 
        acc = round(button.ability.accuracy, 2) *100

        crit = round(button.ability.crit, 2) *100
        dmg_low = round(hero.dmg_range[0] * button.ability.dmg_mod * hero.dmg_amp)
        dmg_high = round(hero.dmg_range[-1] * button.ability.dmg_mod * hero.dmg_amp)

        draw_text(f"{acc}%", font_med, grey, 350, 760)
        draw_text(f"{crit}%", font_med, grey, 350, 780)
        draw_text(f"{dmg_low}-{dmg_high}", font_med, grey, 350, 800)
        #draw ability statuses
        if button.ability.status == 'Bleed':
            dot = button.ability.dot
            r = button.ability.rounds
            draw_text(f"Bleed {dot}/{r} rds", font_small, dark_red, 460, 735)
        elif button.ability.status == 'Blight':
            dot = button.ability.dot
            r = button.ability.rounds
            draw_text(f"Blight {dot}/{r} rds", font_small, vomit, 460, 735)
        elif button.ability.status == 'Stun':
            draw_text("Stun", font_small, yellow, 460, 735)
    elif button.ability.Type == "Heal":
        #draw ability stats 
        acc = round(button.ability.accuracy, 2)
        crit = round(button.ability.crit, 2)
        heal = button.ability.heal
        draw_text(f"{acc}", font_med, grey, 350, 760)
        draw_text(f"{crit}", font_med, grey, 350, 780)
        draw_text(f"{heal}", font_med, grey, 350, 800)
        draw_text(f"Heal {button.ability.heal}", font_small, green, 460, 735)
        if button.ability.status == 'Cure':
            draw_text("Remove bleed/blight from target and self", font_small, green, 460, 750)
    elif button.ability.Type == "Stress_heal":
        s = abs(button.ability.stress)
        draw_text(f"Remove {s} Stress", font_small, white, 460, 735)
    elif button.ability.Type == "Buff":
        draw_text(f"+{button.ability.dmg_mod}% DMG", font_small, white, 460, 735)
        draw_text(f"+{button.ability.speed}% SPD", font_small, white, 600, 735)
        draw_text(f"+{button.ability.crit}% CRIT", font_small, white, 460, 750)
    
    

#Colours
red = (255,0,0)
dark_red = (168,10,10)
vomit = (130,175,5)
green = (0,255,0)
yellow = (233,200,85)
grey = (200,200,200) 
black = (0,0,0)
white = (200,200,200)
dark_grey = (100,100,100)

empty_stress = pygame.image.load("images/heroes/stress_empty.png")
full_stress = pygame.image.load("images/heroes/stress_full.png")

#Classes for our heroes
class Person(pygame.sprite.Sprite):
    def __init__(self, x, y, name, health, critical, dodge, speed, position, dmg_range):
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
        self.dmg_range = dmg_range
        self.dmg_amp = 1
        self.blight = []
        self.bleed = []
        self.deathblow_res = 0.67
        self.action_token = 0 

        
    def draw(self,hp, flip = False):
        self.current_hp = hp
        ratio = self.current_hp / self.max_hp
        if flip == True:
            display.blit(pygame.transform.flip(self.image, True, False), self.rect)
            pygame.draw.rect(display, dark_grey, (self.x-40,self.y+180,100,10))
            pygame.draw.rect(display, red, (self.x-40,self.y+180,100*ratio,10))
        else:
            display.blit(self.image, self.rect)
            pygame.draw.rect(display, dark_grey, (self.x-40,self.y + 165, 100, 10))
            pygame.draw.rect(display, red, (self.x-40,self.y + 165, 100*ratio, 10))
            for i in range(11):
                display.blit(empty_stress, (self.x-40+i*9.5,self.y+180))
            for i in range(self.stress):
                display.blit(full_stress, (self.x-40+i*9.5,self.y+180))
                
    def roll_dmg(self):
        damage = random.choice(self.dmg_range) * self.dmg_amp
        return damage
    
    def roll_crit(self):
        if random.randint(0,1) < self.crit:
            return True
        else:
            return False

class Highwayman(Person):
    def __init__(self, x, y, name,position):
        #initialize parent class
        self.hero_class = "Highwayman"
        dmg_range = [i for i in range(5,11)]
        super().__init__(x, y, name, 23, 0.05, 0.1, 5, position, dmg_range)
        
        self.abilities = []
        self.wicked_slice = ability('wicked_slice',[0,1,2], [0,1], 'Attack', self.crit + 0.05 ,0.85, dmg_mod = 1.15)
        self.pistol_shot = ability('pistol_shot',[1,2,3], [1,2,3], 'Attack', self.crit + 0.075, 0.85,dmg_mod = 0.9)
        self.grapeshot_blast = ability('grapeshot_blast',[1,2], [(0,1,2)], 'Attack', self.crit - 0.09, 0.75, dmg_mod = 0.5)
        self.open_vein = ability('open_vein',[0,1,2], [0,1],'Attack', self.crit, 0.95, status = 'Bleed', rounds = 2, dot = 3, dmg_mod = 0.85)
        #fix dmg || dmg mod - crit mod - speed mod (numbers)
        self.take_aim = ability('take_aim',[0,1,2,3], [1],'Buff', 0.1,1, speed = 1,dmg_mod = 0.12)#last arguement will add speed to dismas
        self.PASS = ability('pass',[0,1,2,3],[0,1,2,3],'Pass',0,0)
        
        self.abilities.append(self.wicked_slice)
        self.abilities.append(self.pistol_shot)
        self.abilities.append(self.grapeshot_blast)
        self.abilities.append(self.open_vein)
        self.abilities.append(self.take_aim)
        self.abilities.append(self.PASS)
        
class Crusader(Person):
    def __init__(self, x, y, name, position):
        self.hero_class = "Crusader"
        #initialize parent class
        dmg_range = [i for i in range(6,13)]
        super().__init__(x, y, name, 33, 0.03, 0.05, 1, position, dmg_range)
        
        self.abilities = []
        self.smite = ability('smite', [0,1], [0,1],'Attack', self.crit, 0.85)
        self.zealous_accusation = ability('zealous_accusation', [0,1], [(0,1)], 'Attack', self.crit - 0.04, 0.85,dmg_mod = 0.5)
        self.stunning_blow = ability('stunning_blow', [0,1], [0,1], 'Attack', self.crit, 0.9,dmg_mod = 0.5)
        #fix dmg
        self.inspiring_cry = ability('inspiring_cry', [0,1,2,3], [0,1,2,3],'Stress_heal', self.crit, 1,heal = 1,stress = -2)
        #fix dmg
        self.battle_heal = ability('battle_heal', [0,1,2,3], [0,1,2,3],'Heal', self.crit, 1, heal = 4)
        self.PASS = ability('pass',[0,1,2,3],[0,1,2,3],'Pass',0,0)
      
        self.abilities.append(self.smite)
        self.abilities.append(self.zealous_accusation)
        self.abilities.append(self.stunning_blow)
        self.abilities.append(self.inspiring_cry)
        self.abilities.append(self.battle_heal)
        self.abilities.append(self.PASS)
        
class Plague_Doctor(Person):
    def __init__(self, x, y, name, position):
        self.hero_class = "Plague_Doctor"
        #initialize parent class
        dmg_range = [i for i in range(4,8)]
        super().__init__(x, y, name, 22, 0.02, 0.01, 7, position, dmg_range)
        
        self.abilities = []
        self.noxious_blast = ability("noxious_blast" ,[1,2,3], [0,1],'Attack', self.crit, 0.95,dmg_mod = 0.2, status = 'Blight', rounds = 3, dot= 5)
        self.plague_grenade = ability("plague_grenade", [1,2,3], [(2,3)],'Attack', self.crit, 0.95,dmg_mod = 0.1,status = 'Blight', rounds = 3, dot= 4)
        self.blinding_gas = ability("blinding_gas", [2,3], [(2,3)],'Attack',0,0.95, dmg_mod = 0,status = 'Stun')   
        #fix dmg
        self.battlefield_medicine = ability("battlefield_medicine", [2,3], [0,1,2,3],'Heal', self.crit, 1, status = 'Cure', heal = 1)
        self.incision = ability('incision', [0,1,2], [0,1],'Attack', self.crit + 0.05, 0.85, status = 'Bleed', rounds = 3, dot = 2)
        self.PASS = ability('pass',[0,1,2,3],[0,1,2,3],'Pass',0,0)
             
        self.abilities.append(self.noxious_blast)
        self.abilities.append(self.plague_grenade)
        self.abilities.append(self.blinding_gas)
        self.abilities.append(self.battlefield_medicine)
        self.abilities.append(self.incision)
        self.abilities.append(self.PASS)
        
class Vestal(Person):
    def __init__(self, x, y, name, position):
        self.hero_class = "Vestal"
        #initialize parent class
        dmg_range = [i for i in range(4,9)]
        super().__init__(x, y, name, 24, 0.01, 0.01, 4, position, dmg_range)
        
        self.abilities = []
        self.dazzling_light = ability("dazzling_light", [1,2,3], [0,1,2],'Attack', self.crit + 0.05, 0.9,dmg_mod = 0.2, status = 'Stun')
        #fix dmg
        self.divine_grace = ability("divine_grace", [2,3], [0,1,2,3],'Heal', self.crit, 1,heal = 4)
        #fix dmg
        self.divine_comfort = ability("divine_comfort", [2,3], [(0,1,2,3)],'Heal', self.crit, 1,heal = 1)
        self.judgement = ability("judgement", [0,1,2,3], [(2,3)],'Attack', self.crit + 0.05, 0.85, dmg_mod = 0.5)
        self.illumination = ability('illumination', [0,1,2,3], [0,1,2,3],'Attack', self.crit, 0.9)
        self.PASS = ability('pass',[0,1,2,3],[0,1,2,3],'Pass',0,0)
        
        self.abilities.append(self.dazzling_light)
        self.abilities.append(self.divine_grace)
        self.abilities.append(self.divine_comfort)
        self.abilities.append(self.judgement)
        self.abilities.append(self.illumination)
        self.abilities.append(self.PASS)
        
#Enemy classes
class Cutthroat(Person):
    def __init__(self,x,y,name,position):
        #fixer pls
        dmg_range = [i for i in range(2,5)]
        super().__init__(x, y, name, 30, 0.12, 0.025, 3, position, dmg_range)
        
        self.Slice_and_dice = ability('Slice_and_dice', [0,1,2], [(0,1)],'Attack', self.crit, 0.725,dmg_mod = 1.5)
        self.Uppercut_Slice = ability('Uppercut_Slice', [0,1], [0,1],'Attack', self.crit + 0.05, 0.725)
        self.Shank = ability('Shank', [0,1,2], [0,1,2,3],'Attack',self.crit + 0.06, 0.725,dmg_mod = 2, status = 'Bleed', rounds = 3, dot = 2)
        
        self.abilities =[]
        self.abilities.append(self.Slice_and_dice)
        self.abilities.append(self.Uppercut_Slice)
        self.abilities.append(self.Shank)

    def take_action(self):
        pass

class Fusilier(Person):
    def __init__(self, x, y, name,position):
        dmg_range = [i for i in range(1,6)]
        super().__init__(x, y, name, 20, 0.01, 0.075, 6, position, dmg_range)
        self.abilities = []
        self.Blanket = ability('Blanket', [1,2,3], [(0,1,2,3)],'Attack' ,self.crit + 0.02 ,0.725)
        self.abilities.append(self.Blanket)
        
    def take_action(self):
        pass


#CHANGE ABILITIES TO FIT NEW CONSTRUCTOR STANDARDS


class ability():
    def __init__(self, name, position, target,  Type, crit, accuracy,
                 dmg_mod = 1,status = '', rounds = 0, dot = 0, heal = 0, stress = 0,speed = 0):
        self.name = name
        self.heal = heal
        self.position = position
        self.target = target
        self.dmg_mod = dmg_mod #this only modifies damage
        self.Type = Type
        self.crit = crit
        self.accuracy = accuracy
        self.status = status
        self.rounds = rounds
        self.dot = dot
        self.stress = stress
        self.speed = speed
                    
        
    #Function to fire the effect of the ability depending on its Type
    #Using the calculation functions, while checking to apply buffs
    def proc(self, roll_number, target, crit):
        cure = False
        if self.Type == 'Attack':
            if not crit:
                apply_dmg(target, round(roll_number * self.dmg_mod))
                if self.status == 'Blight':
                    apply_blight(target, self.dot, self.rounds)
                elif self.status == 'Bleed':
                    apply_bleed(target, self.dot, self.rounds)
                elif self.status == 'Stun':
                    apply_stun(target)
            else:
                apply_dmg(target, round(2 * roll_number * self.dmg_mod))
                if self.status == 'Blight':
                    apply_blight(target, self.dot, self.rounds+2)
                elif self.status == 'Bleed':
                    apply_bleed(target, self.dot, self.rounds+2)
                elif self.status == 'Stun':
                    apply_stun(target)
        elif self.Type == 'Heal':
            if self.status == 'Cure':
                cure = True
            if not crit:
                apply_heal(target, round(roll_number * self.dmg_mod),cure)
            else:
                apply_heal(target, round(2 * roll_number * self.dmg_mod),cure)
        elif self.Type == 'Stress_heal':
                apply_stress(target, round(roll_number * self.dmg_mod))
        elif self.Type == 'Buff':
            apply_buff(target,dps_buff = self.dmg_mod,crit_buff = self.crit,speed_buff = self.speed)


#functions to calculate things
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

def apply_stun(target):
    target.action_token -= 1
    
def apply_heal(target,heal,cure = False):
    if target.current_hp + heal > target.max_hp:
        target.current_hp = target.max_hp
    else:
        target.current_hp += heal
    if cure:
        target.blight = []
        target.bleed = []

def apply_stress(target,stress):
    if target.stress == 10:
        pass #meltdown
    elif target.stress + stress < 0:
        pass
    else:
        target.stress += stress
        
def apply_buff(target,dps_buff = 0,speed_buff = 0,crit_buff = 0):
    target.dmg_amp += dps_buff
    target.speed += speed_buff
    for ability in target.abilities:
        if ability.Type == 'Attack':
            ability.crit += crit_buff



#REMINDER TO REVERT BUFFS AFTER ONE FIGHT!!!!!!!!!!
#def revert_buffs(target)

#the main function for the player taking turns
def wait_action(buttons,hero):
    condition = 0 #counter for targets than need to be drawn
    selected_button = None
    action = False
    selected_displayed = False
    while not action:
        if not selected_displayed:
            selected = pygame.image.load("images/targets/selected.png")
            display.blit(selected, (470 - 150 * hero.position, 390))
            selected_displayed = True
        pos = pygame.mouse.get_pos()
        #Wait for player to click an ability
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            for button in buttons:
                #player clicks ability
                if event.type == pygame.MOUSEBUTTONDOWN and button.rect.collidepoint(pos):
                    condition = 0
                    selected_button = button #the ability that was pressed
                    #blit background
                    for i in range(0,tiles):
                        display.blit(bg, (i * bg.get_width() + scroll,0))
                    for enemy in enemy_list:
                        enemy.draw(enemy.current_hp,flip=True)
                    for member in party:
                        member.draw(member.current_hp)
                    draw_panel()
                    draw_hero(hero)
                    selected = pygame.image.load("images/targets/selected.png")
                    display.blit(selected, (470 - 150 * hero.position, 390))
                    pygame.display.update()
        if selected_button != None: #if a button was pressed
            for target in selected_button.ability.target: #valid targets
                if selected_button.ability.Type == 'Attack':
                    #if ability is aoe
                    if type(target)==tuple:
                        target_counter = 0 
                        #target is tuple, so we iterate
                        for a in target:
                            target_counter += 1
                            #draw targets
                            #this checks that all targets are drawn
                            #when they are, stop drawing them
                            if condition < len(target): 
                                target_icon = pygame.image.load("images/targets/target_1.png")
                                display.blit(target_icon, (823 + 150*a, 380))
                                if target_counter < len(target): 
                                    #draw plus signs
                                    #we need targets-1 plus signs
                                    plus = pygame.image.load("images/targets/plus.png")
                                    display.blit(plus, (960 + 150*a, 525))
                                condition += 1
                            for enemy in enemy_list:
                                #if player clicks any enemy that is a valid target
                                if enemy.position in target:
                                    if enemy.rect.collidepoint(pos): #ON HOVER
                                        draw_enemy(enemy) #oh the misery
                                        if pygame.mouse.get_pressed()[0] == 1:
                                            action = True #action has been taken
                                    if action:
                                        #proc the ability on every enemy in the aoe
                                        #because for enemy in enemy_list
                                        #we roll dmg here so its different every time
                                        damage = hero.roll_dmg()
                                        crit = hero.roll_crit()
                                        selected_button.ability.proc(damage, enemy, crit)
                                        #if we roll dmg when we initialize ability,
                                        #it will deal the same dmg every time
                    else:
                        #if ability is single target
                        target_icon = pygame.image.load("images/targets/target_1.png")
                        if condition < len(selected_button.ability.target):
                            display.blit(target_icon, (823 + 150*target, 380))
                            condition += 1
                        for enemy in enemy_list:
                            #check which enemies are valid targets
                            #target is now int
                            if enemy.position == target:
                                #find which enemy was targeted
                                if enemy.rect.collidepoint(pos):
                                    draw_enemy(enemy) #every body wants to be my enemy!
                                    if pygame.mouse.get_pressed()[0] == 1:
                                        #proc the ability on that single enemy
                                        #we roll dmg here so its different every time
                                        damage = hero.roll_dmg()
                                        crit = hero.roll_crit()
                                        selected_button.ability.proc(damage, enemy, crit)
                                        #if we roll dmg when we initialize ability,
                                        #it will deal the same dmg every time
                                        action = True
                elif selected_button.ability.Type in ['Heal','Buff','Stress_heal']:
                    #if ability is aoe
                    if type(target)==tuple:
                        target_counter = 0 
                        #target is tuple, so we iterate
                        for a in target: 
                            target_counter += 1
                            #draw targets
                            #this checks that all targets are drawn
                            #when they are, stop drawing them
                            if condition < len(target):
                                target_icon = pygame.image.load("images/targets/target_h_1.png")
                                display.blit(target_icon, (475 - 150*a, 360))
                                if target_counter < len(target):
                                    plus = pygame.image.load("images/targets/plus_h.png")
                                    display.blit(plus, (462 - 150*a, 505))
                                condition += 1
                            for member in party:
                                #if player clicks any ally that is a valid target
                                if member.position in target:
                                    if member.rect.collidepoint(pos): #ON HOVER
                                        if pygame.mouse.get_pressed()[0] == 1:
                                            action = True
                                    if action:
                                        #proc the ability on every party in the aoe
                                        #because for enemy in enemy_list
                                        crit = hero.roll_crit()
                                        if selected_button.ability.Type == 'Stress':
                                            selected_button.ability.proc(selected_button.ability.stress,member,crit)
                                        elif selected_button.ability.Type == 'Heal':
                                            selected_button.ability.proc(selected_button.ability.heal,member,crit)
                                        else:
                                            selected_button.ability.proc(selected_button.ability.dmg_mod,member,crit)
                    else:
                        #if ability is single target
                        target_icon = pygame.image.load("images/targets/target_h_1.png")
                        if condition < len(selected_button.ability.target):
                            display.blit(target_icon, (475 - 150*target, 360))
                            condition += 1
                    for member in party:
                        #check which allies are valid targets
                        #target is now int
                        if member.position == target:
                            #find which ally was targeted
                            if member.rect.collidepoint(pos): #ON HOVER
                                if pygame.mouse.get_pressed()[0] == 1:
                                    #proc the ability on that single ally
                                    crit = hero.roll_crit()
                                    selected_button.ability.proc(selected_button.ability.heal,member,crit)
                                    action = True
                else:
                    print('PASSING')
                    action = True
                    apply_stress(hero, 2)
                    break
                    #if not attack or util, then ability.Type == Pass
                    
                    
        draw_panel()
        draw_hero(hero)
        if selected_button:
            draw_ability(hero, selected_button)
        pygame.display.update()
    return selected_button


#Variables
clock = pygame.time.Clock()
FPS = 144
screen_width = 1600
screen_height = 900
bottom_panel = 150
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
dismas = Highwayman(400, 375,'Dismas',1)
reynauld = Crusader(530,375,'Reynauld',0)
paracelsus = Plague_Doctor(230,375,'Paracelsus',2)
junia = Vestal(100,375,'Junia',3)

#creating a group of sprites for heroes
party = []
party.append(dismas)
party.append(reynauld)
party.append(paracelsus)
party.append(junia)

   
enemy1 = Cutthroat(900, 375, 'cutthroat', 0)        
enemy2 = Cutthroat(1050, 375, 'cutthroat', 1)
enemy3 = Fusilier(1200, 375, 'fusilier', 2)
enemy4 = Fusilier(1350, 375, 'fusilier', 3)

enemy_list = []
enemy_list.append(enemy1)
enemy_list.append(enemy2)
enemy_list.append(enemy3)
enemy_list.append(enemy4)


COMBAT = pygame.USEREVENT + 1
tile_size = 1000
party_position = 0
map_tiles = [0,1,0,2,0,1]


#main game loop
run = True
fighting = False
while run:
    clock.tick(FPS)
    
    key = pygame.key.get_pressed()
    #update scroll only when d is pressed
    if fighting == False:
        if key[pygame.K_d]:
            scroll -= 3
            party_position += 10
            
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
    
    #When we have scrolled past the screen reset the queue
    if abs(scroll) > bg.get_width():
        scroll = 0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == COMBAT:
            fighting = True
            initiative = []
        if fighting:
            loc = (i-1 * bg.get_width()) + scroll
            for member in party:
                initiative.append((random.choice(range(9)) + member.speed,0,member))
            for enemy in enemy_list:
                initiative.append((random.choice(range(9)) + enemy.speed,1,enemy))
            initiative.sort(key = lambda tup: tup[1])
            for roll, team, person in initiative:
                #blit background
                for i in range(0,tiles):
                    display.blit(bg, (i * bg.get_width() + scroll,0))
                for enemy in enemy_list:
                    enemy.draw(enemy.current_hp,flip=True)
                for member in party:
                    member.draw(member.current_hp)
                draw_panel()
                pygame.display.update()
                if team == 0:
                    selected_button = None
                    buttons = draw_hero(person)
                    wait_action(buttons, person)
                else:
                    pass

                
    if not fighting:
        for member in party:
            member.draw(member.current_hp)
    pygame.display.update()

pygame.quit()