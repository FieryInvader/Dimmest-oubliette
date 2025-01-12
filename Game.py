import pygame
import math
import random
import time

pygame.init()

random.seed(time.time())
#button class
class Button():
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
            if self.ability.name != "pass":
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
font_huge = pygame.font.SysFont('Comic sans', 48)
    

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
    draw_text(hero.hero_class.replace("_"," "), font, grey, 320, 640)
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

def draw_target(target, ability, hero):
    #draw overlay
    overlay = pygame.image.load("images/panels/panel_monster.png")
    display.blit(overlay, (800, 568))
    if target in enemy_list:
        indicator = pygame.image.load("images/panels/indicator_valid.png")
        display.blit(indicator, (target.x-50, target.y+175))
        colour = dark_red
        to_hit = (ability.accuracy - target.dodge) * 100
        dmg_low = round(hero.dmg_range[0] * ability.dmg_mod)
        dmg_high = round(hero.dmg_range[-1] * ability.dmg_mod)
        draw_text(f"Hero DMG: {dmg_low}-{dmg_high}", font_small, yellow, 1150, 692)
    else:
        colour = white
        to_hit = ability.accuracy
    #draw name
    draw_text(target.name.capitalize(), font, colour, 850, 612)
    #draw stats
    draw_text(f"HP {target.current_hp}/{target.max_hp}", font, red, 1200, 612)
    
    draw_text(f"Hero to Hit: {to_hit}%", font_small, yellow, 1150, 652)
    crit = round(ability.crit*100,2)
    if crit < 0: 
        crit = 0
    draw_text(f"Hero to Crit: {crit}%", font_small, yellow, 1150, 672)
    #draw stats
    draw_text(f"SPEED: {target.speed}", font_small, grey, 1000, 652)
    dodge = target.dodge * 100
    draw_text(f"DODGE: {dodge}%", font_small, grey, 1000, 672)

#incision does not round critical for some unknown reason

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
        draw_text("100%", font_med, grey, 350, 760)
        draw_text(f"{crit}", font_med, grey, 350, 780)
        draw_text(f"{heal}", font_med, grey, 350, 800)
        draw_text(f"Heal {button.ability.heal}", font_small, green, 460, 735)
        if button.ability.status == 'Cure':
            draw_text("Remove bleed/blight from target and self", font_small, green, 460, 750)
    elif button.ability.Type == "Stress_heal":
        s = abs(button.ability.stress)
        draw_text(f"Remove {s} Stress", font_small, white, 460, 735)
        if button.ability.heal:
            draw_text(f"Heal {button.ability.heal}", font_small, green, 460, 750)
    elif button.ability.Type == "Buff":
        draw_text(f"+{button.ability.dmg_mod}% DMG", font_small, white, 460, 735)
        draw_text(f"+{button.ability.speed}% SPD", font_small, white, 600, 735)
        draw_text(f"+{button.ability.crit}% CRIT", font_small, white, 460, 750)
    
class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, colour,icon = None):
        pygame.sprite.Sprite.__init__(self)
        if not icon:
            self.image = font.render(str(damage), True, colour)
        else:
            self.image = icon
            x += 60
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0
        
    def update(self,animation = False):
		#delete the text after a few seconds
        self.counter += 1
        if self.counter > 100:
            self.kill()
        # if not animation:
        #     for i in range(0,tiles):
        #         display.blit(bg, (i * bg.get_width() + scroll,0))
        #     for enemy in enemy_list:
        #         enemy.draw(enemy.current_hp,flip=True)
        #     for member in party:
        #         member.draw(member.current_hp)



class hit_or_miss(pygame.sprite.Sprite): # i guess they never miss, huh?
    def __init__(self, x, hit):
        pygame.sprite.Sprite.__init__(self)
        if hit:
            colour = yellow
            text = "HIT"
        else:
            colour = grey
            text = "MISS"
        self.image = font.render(text, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, 200)
        self.counter = 0
              
    def update(self,animation = False):
		#delete the text after a few seconds
        self.counter += 1

        if self.counter > 100:
            self.kill()
        # if not animation:
        #     for i in range(0,tiles):
        #         display.blit(bg, (i * bg.get_width() + scroll,0))
        #     for enemy in enemy_list:
        #         enemy.draw(enemy.current_hp,flip=True)
        #     for member in party:
        #         member.draw(member.current_hp)

                

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
sky_blue = (180,180,255)

empty_stress = pygame.image.load("images/heroes/stress_empty.png")
full_stress = pygame.image.load("images/heroes/stress_full.png")

#Classes for our heroes
class Person():
    def __init__(self, x, y, name, health, critical, dodge, speed, position, 
                 dmg_range, stun_res, blight_res, bleed_res):
        #visuals
        self.x = x
        self.y = y
        self.name = name
        self.position = position
        self.image = pygame.image.load(f"images/heroes/{name}.png")
        self.defend = pygame.image.load(f"images/heroes/{name}_defend.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        #stats
        self.max_hp = health
        self.current_hp = health
        self.stress = 1
        self.crit = critical
        self.dodge = dodge
        self.speed = speed
        self.dmg_range = dmg_range
        self.dmg_amp = 1
        self.stun_res = stun_res
        self.blight_res = blight_res
        self.bleed_res = bleed_res
        self.blight = []
        self.bleed = []
        self.isStunned = False
        self.deathblow_res = 0.67
        self.action_token = 0 
        self.alive = True
        #Enemy variables
        self.action_wait_time = 100
        self.action_cooldown = 0
        
    def draw(self,hp, flip = False, animation = None):
        self.current_hp = hp
        ratio = self.current_hp / self.max_hp
        if flip == True:
            
            if animation == self.defend:
                a = pygame.transform.flip(animation, True, False)
                a = pygame.transform.scale(a, (a.get_width() * 0.5, a.get_height() * 0.5))
                display.blit(a, (self.rect.x,self.rect.y))
            elif animation:
                a = pygame.transform.flip(animation, True, False)
                a = pygame.transform.scale(a, (a.get_width() * 0.5, a.get_height() * 0.5))
                display.blit(a, (600,250))

            else:
                display.blit(pygame.transform.flip(self.image, True, False), self.rect)
            pygame.draw.rect(display, dark_grey, (self.x-40,self.y+180,100,10))
            pygame.draw.rect(display, red, (self.x-40,self.y+180,100*ratio,10))
            if self.blight:
                indicator = [0,0]
                for b in self.blight:
                    indicator[0] += b[0]
                    indicator[1] += b[1]
                text = f"{indicator[0]}/{indicator[1]}"
                blight_icon = pygame.image.load("images/status/blight.png")
                display.blit(blight_icon, (self.rect.center[0],self.rect.center[1] + 150 ))
                draw_text(text, font_small, vomit, self.rect.center[0]+ 30, self.rect.center[1] + 155)
            if self.bleed:
                indicator = [0,0]
                for b in self.bleed:
                    indicator[0] += b[0]
                    indicator[1] += b[1]
                bleed_icon = pygame.image.load("images/status/bleed.png")
                display.blit(bleed_icon, (self.rect.center[0]-50,self.rect.center[1] + 150 ))
                text = f"{indicator[0]}/{indicator[1]}"
                draw_text(text, font_small, dark_red, self.rect.center[0]-20, self.rect.center[1] + 155)
            if self.isStunned:
                if self.action_token < 1:
                    stun_icon = pygame.image.load("images/status/stun.png")
                    display.blit(stun_icon, (self.rect.center[0]-10,self.rect.center[1]-150))    
                else:
                    self.isStunned = False
        else:

            if animation == self.defend:
                a = pygame.transform.scale(animation, (animation.get_width() * 0.5, animation.get_height() * 0.5))
                display.blit(a, (self.rect.x,self.rect.y))
            elif animation:
                a = pygame.transform.scale(animation, (animation.get_width() * 0.5, animation.get_height() * 0.5))
                display.blit(a, (600,250))
            else:
                display.blit(self.image, self.rect)
            pygame.draw.rect(display, dark_grey, (self.rect.center[0]-40,self.rect.center[1] + 165, 100, 10))
            pygame.draw.rect(display, red, (self.rect.center[0]-40,self.rect.center[1] + 165, 100*ratio, 10))
            for i in range(11):
                display.blit(empty_stress, (self.rect.center[0]-40+i*9.5,self.rect.center[1]+180))
            for i in range(self.stress):
                display.blit(full_stress, (self.rect.center[0]-40+i*9.5,self.rect.center[1]+180))
            if self.blight:
                indicator = [0,0]
                for b in self.blight:
                    indicator[0] += b[0]
                    indicator[1] += b[1]
                text = f"{indicator[0]}/{indicator[1]}"
                blight_icon = pygame.image.load("images/status/blight.png")
                display.blit(blight_icon, (self.rect.center[0],self.rect.center[1] + 135 ))
                draw_text(text, font_small, vomit, self.rect.center[0]+ 30, self.rect.center[1] + 140)
            if self.bleed:
                indicator = [0,0]
                for b in self.bleed:
                    indicator[0] += b[0]
                    indicator[1] += b[1]
                bleed_icon = pygame.image.load("images/status/bleed.png")
                display.blit(bleed_icon, (self.rect.center[0]-50,self.rect.center[1] + 135 ))
                text = f"{indicator[0]}/{indicator[1]}"
                draw_text(text, font_small, dark_red, self.rect.center[0]-20, self.rect.center[1] + 140)
            if self.isStunned:
                if self.action_token < 1:
                    stun_icon = pygame.image.load("images/status/stun.png")
                    display.blit(stun_icon, (self.rect.center[0],self.rect.center[1]-150))    
                else:
                    self.isStunned = False
        
        
                
    def roll_dmg(self):
        damage = random.choice(self.dmg_range) * self.dmg_amp
        return damage
    
    def roll_crit(self):
        if random.random() < self.crit:
            return True
        else:
            return False

def roll_to_hit(ability,target):
    roll = random.random()
    if roll < ability.accuracy - target.dodge:
        return True
    else:
        return False

class Highwayman(Person):
    def __init__(self, x, y, name, position):
        #initialize parent class
        self.hero_class = "Highwayman"
        dmg_range = [i for i in range(5,11)]
        super().__init__(x, y, name, 23, 0.05, 0.1, 5, position, dmg_range, 0.3, 0.3, 0.3)
        
        self.abilities = []
        self.wicked_slice = ability('wicked_slice',self,f'images/{self.hero_class}/melee_anim.png',[0,1,2], [0,1], 'Attack', self.crit + 0.05 ,0.85, "wickedslice.wav", dmg_mod = 1.15)
        self.pistol_shot = ability('pistol_shot',self,f'images/{self.hero_class}/pistol_anim.png',[1,2,3], [1,2,3], 'Attack', self.crit + 0.075, 0.85, "pistolshot.wav", dmg_mod = 0.9)
        self.grapeshot_blast = ability('grapeshot_blast',self,f'images/{self.hero_class}/pistol_anim.png',[1,2], [(0,1,2)], 'Attack', self.crit - 0.09, 0.75, "grapeshot.wav", dmg_mod = 0.5)
        self.open_vein = ability('open_vein',self,f'images/{self.hero_class}/melee_anim.png',[0,1,2], [0,1],'Attack', self.crit, 0.95, "openvein.wav", status = 'Bleed', rounds = 2, dot = 3, dmg_mod = 0.85)
        #fix dmg || dmg mod - crit mod - speed mod (numbers)
        self.take_aim = ability('take_aim',self,f'images/{self.hero_class}/take_aim_anim.png',[0,1,2,3], [1],'Buff', 0.1, 1, "takeaim.wav", speed = 1,dmg_mod = 0.12)#last arguement will add speed to dismas
        self.PASS = ability('pass',self,f'images/{self.hero_class}/defend_anim.png',[0,1,2,3],[0,1,2,3],'Pass',0,0, "stress.wav")
        
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
        super().__init__(x, y, name, 33, 0.03, 0.05, 1, position, dmg_range, 0.2, 0.6, 0.2)
        
        self.abilities = []
        self.smite = ability('smite',self,f'images/{self.hero_class}/melee_anim.png', [0,1], [0,1],'Attack', self.crit, 0.85, "smite.wav")
        self.zealous_accusation = ability('zealous_accusation',self,f'images/{self.hero_class}/tileeiedo_anim.png', [0,1], [(0,1)], 'Attack', self.crit - 0.04, 0.85,"zealousacc.wav", dmg_mod = 0.5)
        self.stunning_blow = ability('stunning_blow',self,f'images/{self.hero_class}/stun_anim.png', [0,1], [0,1], 'Attack', self.crit, 0.9, "stunningblow.wav", status = 'Stun',dmg_mod = 0.5)
        #fix dmg
        self.inspiring_cry = ability('inspiring_cry',self,f'images/{self.hero_class}/stress_anim.png', [0,1,2,3], [0,1,2,3],'Stress_heal', self.crit, 1, "inspiringcry.wav", heal = 1,stress = -2)
        #fix dmg
        self.battle_heal = ability('battle_heal',self,f'images/{self.hero_class}/heal_anim.png', [0,1,2,3], [0,1,2,3],'Heal', self.crit, 1, "battleheal.wav", heal = 4)
        self.PASS = ability('pass',self,f'images/{self.hero_class}/defend_anim.png',[0,1,2,3],[0,1,2,3],'Pass',0,0, "stress.wav")
      
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
        super().__init__(x, y, name, 22, 0.02, 0.01, 7, position, dmg_range, 0.3, 0.3, 0.3)
        
        self.abilities = []
        self.noxious_blast = ability("noxious_blast",self,f'images/{self.hero_class}/blast_anim.png' ,[1,2,3], [0,1],'Attack', self.crit, 0.95, "noxiousblast.wav", dmg_mod = 0.2, status = 'Blight', rounds = 3, dot= 5)
        self.plague_grenade = ability("plague_grenade",self,f'images/{self.hero_class}/throw_anim.png', [1,2,3], [(2,3)],'Attack', self.crit, 0.95, "plaguegrenade.wav", dmg_mod = 0.1,status = 'Blight', rounds = 3, dot= 4)
        self.blinding_gas = ability("blinding_gas",self,f'images/{self.hero_class}/throw_anim.png', [2,3], [(2,3)],'Attack',0,0.95, "blindinggas.wav", dmg_mod = 0,status = 'Stun')   
        #fix dmg
        self.battlefield_medicine = ability("battlefield_medicine",self,f'images/{self.hero_class}/heal_anim.png', [2,3], [0,1,2,3],'Heal', self.crit, 1, "battlemed.wav", status = 'Cure', heal = 1)
        self.incision = ability('incision',self,f'images/{self.hero_class}/melee_anim.png', [0,1,2], [0,1],'Attack', self.crit + 0.05, 0.85, "incision.wav", status = 'Bleed', rounds = 3, dot = 2)
        self.PASS = ability('pass',self,f'images/{self.hero_class}/defend_anim.png',[0,1,2,3],[0,1,2,3],'Pass',0,0, "stress.wav")
             
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
        super().__init__(x, y, name, 24, 0.01, 0.01, 4, position, dmg_range, 0.25, 0.3, 0.3)
        
        self.abilities = []
        self.dazzling_light = ability("dazzling_light",self,f'images/{self.hero_class}/stun_anim.png', [1,2,3], [0,1,2],'Attack', self.crit + 0.05, 0.9, "dazzlinglight.wav", dmg_mod = 0.2, status = 'Stun')
        #fix dmg
        self.divine_grace = ability("divine_grace",self,f'images/{self.hero_class}/talktothehand_anim.png', [2,3], [0,1,2,3],'Heal', self.crit, 1, "divinegrace.wav", heal = 6)
        #fix dmg
        self.divine_comfort = ability("divine_comfort",self,f'images/{self.hero_class}/talktothehand_anim.png', [2,3], [(0,1,2,3)],'Heal', self.crit, 1, "divinecomfort.wav", heal = 2)
        self.judgement = ability("judgement",self,f'images/{self.hero_class}/attack_anim.png', [0,1,2,3], [(2,3)],'Attack', self.crit + 0.05, 0.85, "judgement.wav", dmg_mod = 0.5)
        self.illumination = ability('illumination',self,f'images/{self.hero_class}/attack_anim.png', [0,1,2,3], [0,1,2,3],'Attack', self.crit, 0.9, "illumination.wav")
        self.PASS = ability('pass',self,f'images/{self.hero_class}/defend_anim.png',[0,1,2,3],[0,1,2,3],'Pass',0,0, "stress.wav")
        
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
        super().__init__(x, y, name, 30, 0.12, 0.025, 3, position, dmg_range, 0.45, 0.4, 0.4)
        
        self.Slice_and_dice = ability('Slice_and_dice',self,'images/Cutthroat/slice_anim.png', [0,1,2], [(0,1)],'Attack', self.crit, 0.85, "wickedslice.wav", dmg_mod = 1.5,status = 'Bleed', rounds = 3, dot = 1)
        self.Uppercut_Slice = ability('Uppercut_Slice',self,'images/Cutthroat/uppercut_anim.png', [0,1], [0,1],'Attack', self.crit + 0.05, 0.85,"smite.wav",status = 'Bleed', rounds = 3, dot = 3)
        self.Shank = ability('Shank',self,'images/Cutthroat/uppercut_anim.png', [0,1,2], [0,1,2,3],'Attack',self.crit + 0.06, 0.85, "incision.wav", dmg_mod = 2, status = 'Bleed', rounds = 3, dot = 2)
        
        self.abilities =[]
        self.abilities.append(self.Slice_and_dice)
        self.abilities.append(self.Uppercut_Slice)
        self.abilities.append(self.Shank)
        
    def take_action(self):
        self.action_cooldown = 0
        while self.action_cooldown <= self.action_wait_time:
            if self.alive and (self.action_token > 0):
                self.action_cooldown += 1
                if self.action_cooldown == self.action_wait_time:
                    random_action = random.choice(self.abilities)
                    if type(random_action.target[0]) is tuple:
                        for position in random_action.target[0]:
                            for member in party:
                                if member.position == position:
                                    crit = self.roll_crit()
                                    if random_action.Type == 'Stress_damage':
                                        random_action.proc(2,member,crit)
                                    
                                    else:
                                        dmg = self.roll_dmg()
                                        random_action.proc(dmg,member,crit)
                    else:
                        target = random.choice(party)
                        crit = self.roll_crit()
                        if random_action.Type == 'Stress_damage':
                            random_action.proc(2,target,crit)
                        
                        else:
                            dmg = self.roll_dmg()
                            random_action.proc(dmg,target,crit)
        else:
            damage_text_group.update()
            hit_text_group.update()
            damage_text_group.draw(display)
            hit_text_group.draw(display)


class Fusilier(Person):
    def __init__(self, x, y, name,position):
        dmg_range = [i for i in range(2,6)]
        super().__init__(x, y, name, 20, 0.01, 0.075, 6, position, dmg_range, 0.25, 0.2, 0.2)
        self.abilities = []
        self.Blanket = ability('Blanket',self,'images/Fusilier/attack_anim.png', [1,2,3], [(0,1,2,3)],'Attack' ,self.crit + 0.02 ,0.8, "grapeshot.wav")
        self.abilities.append(self.Blanket)
        
    def take_action(self):
        self.action_cooldown = 0
        while self.action_cooldown <= self.action_wait_time:
            if self.alive and (self.action_token > 0):
                self.action_cooldown += 1
                if self.action_cooldown == self.action_wait_time:
                    random_action = random.choice(self.abilities)
                    if type(random_action.target[0]) is tuple:
                        for position in random_action.target[0]:
                            for member in party:
                                if member.position == position:
                                    crit = self.roll_crit()
                                    if random_action.Type == 'Stress_damage':
                                        random_action.proc(2,member,crit)
                                    
                                    else:
                                        dmg = self.roll_dmg()
                                        random_action.proc(dmg,member,crit)
                    else:
                        target = random.choice(party)
                        crit = self.roll_crit()
                        if random_action.Type == 'Stress_damage':
                            random_action.proc(2,target,crit)
                        
                        else:
                            dmg = self.roll_dmg()
                            random_action.proc(dmg,target,crit)
        else:
            damage_text_group.update()
            hit_text_group.update()
            damage_text_group.draw(display)
            hit_text_group.draw(display)

class Witch(Person):
    def __init__(self, x, y, name,position):
        dmg_range = [i for i in range(3,7)]
        super().__init__(x, y, name, 28, 0.02, 0.15, 8, position, dmg_range, 0.25, 0.2, 0.2)
        self.abilities = []
        self.incantation = ability('incantation',self,'images/Witch/attack_anim.png', [0,1,2,3], [0,1,2,3],'Stress_damage' ,self.crit,0.825, "stress.wav")
        self.blast = ability('blast',self,'images/Witch/attack_anim.png', [0,1,2,3], [0,1,2,3],'Attack' ,self.crit + 0.06,0.825, "blast.wav")
        
        self.abilities.append(self.incantation)
        self.abilities.append(self.blast)
        
    def take_action(self):
        self.action_cooldown = 0
        while self.action_cooldown <= self.action_wait_time:
            if self.alive and (self.action_token > 0):
                self.action_cooldown += 1
                if self.action_cooldown == self.action_wait_time:
                    random_action = random.choice(self.abilities)
                    if type(random_action.target[0]) is tuple:
                        for position in random_action.target[0]:
                            for member in party:
                                if member.position == position:
                                    crit = self.roll_crit()
                                    if random_action.Type == 'Stress_damage':
                                        random_action.proc(2,member,crit)
                                    
                                    else:
                                        dmg = self.roll_dmg()
                                        random_action.proc(dmg,member,crit)
                    else:
                        target = random.choice(party)
                        crit = self.roll_crit()
                        if random_action.Type == 'Stress_damage':
                            random_action.proc(2,target,crit)
                        
                        else:
                            dmg = self.roll_dmg()
                            random_action.proc(dmg,target,crit)
        else:
            damage_text_group.update()
            hit_text_group.update()
            damage_text_group.draw(display)
            hit_text_group.draw(display)
            
class Brawler(Person):
    def __init__(self, x, y, name,position):
        dmg_range = [i for i in range(2,5)]
        super().__init__(x, y, name, 50, 0.2, 0.08, 5, position, dmg_range, 0.25, 0.2, 0.2)
        self.abilities = []
        self.rend = ability('rend',self,'images/Brawler/attack_anim.png', [0,1,2,3], [0,1,2,3],'Attack' ,self.crit,0.825, "rend.wav",status = 'Bleed',rounds = 3,dot = 1)
        
        self.abilities.append(self.rend)
        
    def take_action(self):
        self.action_cooldown = 0
        while self.action_cooldown <= self.action_wait_time:
            if self.alive and (self.action_token > 0):
                self.action_cooldown += 1
                if self.action_cooldown == self.action_wait_time:
                    random_action = random.choice(self.abilities)
                    if type(random_action.target[0]) is tuple:
                        for position in random_action.target[0]:
                            for member in party:
                                if member.position == position:
                                    crit = self.roll_crit()
                                    if random_action.Type == 'Stress_damage':
                                        random_action.proc(2,member,crit)
                                    
                                    else:
                                        dmg = self.roll_dmg()
                                        random_action.proc(dmg,member,crit)
                    else:
                        target = random.choice(party)
                        crit = self.roll_crit()
                        if random_action.Type == 'Stress_damage':
                            random_action.proc(2,target,crit)
                        
                        else:
                            dmg = self.roll_dmg()
                            random_action.proc(dmg,target,crit)
        else:
            damage_text_group.update()
            hit_text_group.update()
            damage_text_group.draw(display)
            hit_text_group.draw(display)



class ability():
    def __init__(self, name,hero,anim, position, target,  Type, crit, accuracy, sound,
                 dmg_mod = 1,status = '', rounds = 0, dot = 0, heal = 0, stress = 0,speed = 0):
        self.name = name
        self.hero = hero
        self.heal = heal
        self.position = position
        self.target = target
        self.dmg_mod = dmg_mod #this only modifies damage
        self.Type = Type
        self.crit = crit
        self.accuracy = accuracy
        self.sound = pygame.mixer.Sound(f"sounds/{sound}")
        self.sound_played = 0 
        self.status = status
        self.rounds = rounds
        self.dot = dot
        self.stress = stress
        self.speed = speed
        self.anim = anim
                    
        
    #Function to fire the effect of the ability depending on its Type
    #Using the calculation functions, while checking to apply buffs
    def proc(self, roll_number, target, crit):
        cure = False
        to_hit = random.random()
        dot_stick = random.random()
        anim = pygame.image.load(self.anim)
        if self.sound_played == 0:
            self.sound.play()
            self.sound_played += 1
        #target.draw(target.current_hp)
        if self.Type == 'Attack':
            #if the attack hits
            if to_hit < self.accuracy - target.dodge:
                hit_text = hit_or_miss(target.x, True)
                hit_text_group.add(hit_text)
                #if the attack doesnt crit
                #apply dmg text if crit
                #make dmg a variable and pass it to apply dmg and dmg text
                #do not roll seperately
                dmg = round(roll_number * self.dmg_mod)
                if not crit:
                    apply_dmg(target, dmg)
                    damage_text = DamageText(target.x, target.y-200, dmg,
                                             red)
                    damage_text_group.add(damage_text)
                    if self.status == 'Blight':
                        if dot_stick > target.blight_res:
                            apply_blight(target, self.dot, self.rounds)
                            damage_text = DamageText(target.x, target.y-150, 
                                                     "Blight", vomit)
                            icon = pygame.image.load("images/status/blight.png").convert()
                            icon_txt = DamageText(target.x,target.y-150,'',vomit ,icon)
                            damage_text_group.add(icon_txt)
                            damage_text_group.add(damage_text)
                        else:
                            damage_text = DamageText(target.x, target.y-150, 
                                                     "Resist!", vomit)
                            icon = pygame.image.load("images/status/blight.png").convert()
                            icon_txt = DamageText(target.x,target.y-150,'',vomit,icon)
                            damage_text_group.add(icon_txt)
                            damage_text_group.add(damage_text)
                    elif self.status == 'Bleed':
                        if dot_stick > target.bleed_res:
                            apply_bleed(target, self.dot, self.rounds)
                            damage_text = DamageText(target.x, target.y-150, 
                                                     "Bleed", red)
                            icon = pygame.image.load("images/status/bleed.png").convert()
                            icon_txt = DamageText(target.x,target.y-150,'',red,icon)
                            damage_text_group.add(icon_txt)
                            damage_text_group.add(damage_text)
                        else:
                            damage_text = DamageText(target.x, target.y-150, 
                                                     "Resist!", red)
                            icon = pygame.image.load("images/status/bleed.png").convert()
                            icon_txt = DamageText(target.x,target.y-150,'',red,icon)
                            damage_text_group.add(icon_txt)
                            damage_text_group.add(damage_text)
                    elif self.status == 'Stun':
                        if dot_stick > target.stun_res:
                            apply_stun(target)

                            damage_text = DamageText(target.x, target.y-150, 
                                                     "Stun!", yellow)
                            icon = pygame.image.load("images/status/stun.png")
                            icon_txt = DamageText(target.x, target.y-150,'', yellow,icon = icon)
                            damage_text_group.add(icon_txt)
                            damage_text_group.add(damage_text)
                        else:
                            damage_text = DamageText(target.x, target.y-150, 
                                                     "Stun resisted", yellow)
                            damage_text_group.add(damage_text) 
                else:
                    apply_dmg(target, round(2 * roll_number * self.dmg_mod))
                    damage_text = DamageText(target.x, target.y-200, 
                                             f"{round(2 * roll_number * self.dmg_mod)} CRIT!", red)
                    damage_text_group.add(damage_text)
                    if self.status == 'Blight':
                        apply_blight(target, self.dot, self.rounds+2)
                        damage_text = DamageText(target.x, target.y-150, 
                                                 "Blight", vomit)
                        icon = pygame.image.load("images/status/blight.png").convert()
                        icon_txt = DamageText(target.x,target.y-150,'',vomit,icon)
                        damage_text_group.add(icon_txt)
                        damage_text_group.add(damage_text)
                    elif self.status == 'Bleed':
                        apply_bleed(target, self.dot, self.rounds + 2)
                        damage_text = DamageText(target.x, target.y-150, 
                                                 "Bleed", red)
                        icon = pygame.image.load("images/status/bleed.png").convert()
                        icon_txt = DamageText(target.x,target.y-150,'',red,icon)
                        damage_text_group.add(icon_txt)
                        damage_text_group.add(damage_text)
                    elif self.status == 'Stun':
                        apply_stun(target)
                        damage_text = DamageText(target.x, target.y-200, 
                                                 "Stun", yellow)
                        icon = pygame.image.load("images/status/stun.png")
                        icon_txt = DamageText(target.x, target.y-150,'', yellow,icon = icon)
                        damage_text_group.add(icon_txt)
                        damage_text_group.add(damage_text)

            else:
                hit_text = hit_or_miss(target.x, False)
                hit_text_group.add(hit_text)
        elif self.Type == 'Heal':
            if self.status == 'Cure':
                damage_text = DamageText(target.x, target.y-220, 
                                         'Cured!', white)
                damage_text_group.add(damage_text)
                cure = True
            if not crit:
                apply_heal(target, round(roll_number * self.dmg_mod),cure)
                damage_text = DamageText(target.x, target.y-200, 
                                         str(roll_number), green)
                damage_text_group.add(damage_text)
            else:
                apply_heal(target, round(2 * roll_number * self.dmg_mod),cure)
                damage_text = DamageText(target.x, target.y-200, 
                                         f"{2*roll_number*self.dmg_mod} CRIT!", green)
                damage_text_group.add(damage_text)
        elif self.Type == 'Stress_heal':
            apply_stress(target,roll_number)
            if self.heal != 0:
                apply_heal(target, self.heal ,cure)
                damage_text = DamageText(target.x, target.y-220, 
                                         f"{roll_number} stress", white)
                damage_text_group.add(damage_text)
                damage_text = DamageText(target.x, target.y-200, 
                                         str(self.heal), green)
                damage_text_group.add(damage_text)
            else:
                damage_text = DamageText(target.x, target.y-200, 
                                         f"{roll_number} stress", white)
                damage_text_group.add(damage_text)
        elif self.Type == 'Stress_damage':
            if not crit:
                apply_stress(target,roll_number)
                damage_text = DamageText(target.x, target.y-200, 
                                         f"+{roll_number}Stress", white)
                damage_text_group.add(damage_text)
            else:
                apply_stress(target, roll_number + 1)
                damage_text = DamageText(target.x, target.y-200, 
                                         f"+{roll_number + 1}Stress", white)
                damage_text_group.add(damage_text)
        elif self.Type == 'Buff':
            apply_buff(target,dps_buff = self.dmg_mod,crit_buff = self.crit,speed_buff = self.speed)
            damage_text = DamageText(target.x, target.y-200, 
                                     "Buffed!", sky_blue)
            damage_text_group.add(damage_text)
        if type(self.target[0]) is not tuple:
            x = 100
        else:
            x = round(100/len(self.target[0])*1.5)
        for j in range(x):
            for i in range(0,tiles):
                display.blit(bg, (i * bg.get_width() + scroll,0))
            for enemy in enemy_list:
                if enemy == self.hero:
                    self.hero.draw(self.hero.current_hp,flip = True,animation = anim)
                elif enemy == target:
                    enemy.draw(enemy.current_hp,flip = True,animation = enemy.defend)
                else:
                    enemy.draw(enemy.current_hp,flip=True)
            for member in party:
                if member == self.hero:
                    self.hero.draw(self.hero.current_hp,animation = anim)
                elif member == target:
                    member.draw(member.current_hp,animation = member.defend)
                else:
                    member.draw(member.current_hp)
            damage_text_group.update(animation = True)
            damage_text_group.draw(display)
            hit_text_group.update(animation = True)
            hit_text_group.draw(display)
            pygame.display.update()


#functions to calculate things
def apply_dmg(target,dmg):
    if target.current_hp - dmg < 0:
        target.current_hp = 0
    else:
        target.current_hp -= dmg
    if target in enemy_list:    
        target.draw(target.current_hp,flip = True)
    else:
        target.draw(target.current_hp)
  
        
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
    #if target gets stunned, its harder to get stunnned again this fight
    target.stun_res += 0.5
    target.isStunned = True
    if target.action_token == -1:
        return
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
    target.stress += stress
    if target.stress > 10:
        target.stress = 10
    if target.stress < 0:
        target.stress = 0
        
def apply_buff(target,dps_buff = 0,speed_buff = 0,crit_buff = 0):
    target.dmg_amp += dps_buff
    target.speed += speed_buff
    for ability in target.abilities:
        if ability.Type == 'Attack':
            ability.crit += crit_buff


#ADD DOT ICON HERE
def resolve_dots(target):
    if target.bleed:
        for dot,Round in target.bleed:
            if target.current_hp - dot <= 0 :
                target.current_hp = 0
                target.alive = False
            target.current_hp -= dot
        numbers = [x[0] for x in target.bleed]
        number = sum(numbers)
        damage_text = DamageText(target.x, target.y-240, 
                                 str(number), red)
        icon = pygame.image.load("images/status/tray_bleed.png").convert()
        icon_txt = DamageText(target.x-30,target.y-240,'',red,icon)
        damage_text_group.add(icon_txt)
        damage_text_group.add(damage_text)
        target.bleed[:] = [(x,y-1) for x,y in target.bleed if y-1 > 0]
    if target.blight:
        for dot,Round in target.blight:
            
            if target.current_hp - dot < 0 :
                target.current_hp = 0
                target.alive = False
            target.current_hp -= dot
        numbers = [x[0] for x in target.blight]
        number = sum(numbers)
        damage_text = DamageText(target.x, target.y-240, 
                                 str(number), vomit)
        icon = pygame.image.load("images/status/tray_blight.png").convert()
        icon_txt = DamageText(target.x-30,target.y-240,'',vomit,icon)
        damage_text_group.add(icon_txt)
        damage_text_group.add(damage_text)
        target.blight[:] = [(x,y-1) for x,y in target.blight if y-1 > 0]


#REMINDER TO REVERT BUFFS AFTER ONE FIGHT!!!!!!!!!!
#def revert_buffs(target)

#the main function for the player taking turns
def wait_action(buttons,hero):
    condition = 0 #counter for targets than need to be drawn
    selected_button = None
    action = False
    selected_displayed = False
    targeting_displayed = False
    damage_text_group.update()
    damage_text_group.draw(display)
    hit_text_group.update()
    hit_text_group.draw(display)
    draw_panel()
    draw_hero(hero)
    while not action:
        if not selected_displayed:
            selected = pygame.image.load("images/targets/selected.png")
            display.blit(selected, (473 - 150 * hero.position, 363))
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
                    display.blit(selected, (473 - 150 * hero.position, 363))
                    pygame.display.update()
        if selected_button != None: #if a button was pressed
            selected_button.ability.sound_played=0
            targeting_displayed = False
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
                            #calculate hit
                        for enemy in enemy_list:
                            #if player clicks any enemy that is a valid target
                            if enemy.position in target:
                                if enemy.rect.collidepoint(pos): #ON HOVER
                                    if not targeting_displayed:
                                        draw_target(enemy, selected_button.ability, hero) #oh the misery
                                        targeting_displayed = True
                                    if pygame.mouse.get_pressed()[0] == 1:
                                        action = True #action has been taken
                        if action:
                            for enemy in enemy_list:
                                if enemy.position in target:
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
                                    if not targeting_displayed:
                                        draw_target(enemy, selected_button.ability, hero) #every body wants to be my enemy!
                                        targeting_displayed = True
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
                                display.blit(target_icon, (473 - 150*a, 362))
                                if target_counter < len(target):
                                    plus = pygame.image.load("images/targets/plus_h.png")
                                    display.blit(plus, (460 - 150*a, 508))
                                condition += 1
                            for member in party:
                                #if player clicks any ally that is a valid target
                                if member.position in target:
                                    if member.rect.collidepoint(pos): #ON HOVER
                                        draw_target(member, button.ability, hero)
                                        if pygame.mouse.get_pressed()[0] == 1:
                                            action = True
                        if action:
                            for member in party:
                                #proc the ability on every party in the aoe
                                #because for enemy in enemy_list
                                crit = hero.roll_crit()
                                if selected_button.ability.Type == 'Stress_heal':
                                    selected_button.ability.proc(selected_button.ability.stress,member,crit)
                                elif selected_button.ability.Type == 'Heal':
                                    selected_button.ability.proc(selected_button.ability.heal,member,crit)
                                else:
                                    selected_button.ability.proc(selected_button.ability.dmg_mod,member,crit)
                    else:
                        #if ability is single target
                        target_icon = pygame.image.load("images/targets/target_h_1.png")
                        if condition < len(selected_button.ability.target):
                            display.blit(target_icon, (473 - 150*target, 362))
                            condition += 1
                    for member in party:
                        #check which allies are valid targets
                        #target is now int
                        if member.position == target:
                            #find which ally was targeted
                            if member.rect.collidepoint(pos): #ON HOVER
                                draw_target(member, button.ability, hero)
                                if pygame.mouse.get_pressed()[0] == 1:
                                    #proc the ability on that single ally
                                    crit = hero.roll_crit()
                                    if selected_button.ability.Type == 'Stress_heal':
                                        selected_button.ability.proc(selected_button.ability.stress,member,crit)
                                    elif selected_button.ability.Type == 'Heal':
                                        selected_button.ability.proc(selected_button.ability.heal,member,crit)
                                    else:
                                        selected_button.ability.proc(selected_button.ability.dmg_mod,member,crit)
                                    action = True
                else:
                    action = True
                    apply_stress(hero, 2)
                    pygame.mixer.Sound("sounds/stress.wav").play()
                    #if not attack or util, then ability.Type == Pass
                    
        damage_text_group.update()
        damage_text_group.draw(display)
        hit_text_group.update()
        hit_text_group.draw(display)
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
reynauld = Crusader(550,375,'Reynauld',0)
paracelsus = Plague_Doctor(250,375,'Paracelsus',2)
junia = Vestal(100,375,'Junia',3)

#creating a group of sprites for heroes
party = []
party.append(dismas)
party.append(reynauld)
party.append(paracelsus)
party.append(junia)

   
enemy1 = Cutthroat(900, 375, 'Cutthroat', 0)        
enemy2 = Cutthroat(1050, 375, 'Cutthroat', 1)
enemy3 = Fusilier(1200, 375, 'Fusilier', 2)
enemy4 = Fusilier(1350, 375, 'Fusilier', 3)

enemy5 = Brawler(900, 375, 'Brawler', 0)        
enemy6 = Brawler(1050, 375, 'Brawler', 1)
enemy7 = Witch(1200, 375, 'Witch', 2)
enemy8 = Witch(1350, 375, 'Witch', 3)

enemy_list = []
enemy_list.append(enemy1)
enemy_list.append(enemy2)
enemy_list.append(enemy3)
enemy_list.append(enemy4)

damage_text_group = pygame.sprite.Group()
hit_text_group = pygame.sprite.Group()

COMBAT = pygame.USEREVENT + 1
tile_size = 1000
party_position = 0
map_tiles = [0,1,0,1,0,2]


#main game loop
run = True
game_over = False
fighting = False
condition = lambda x: x.alive == True
tmp = []
wins = 1

#loop music forever (-1)
pygame.mixer.music.load("sounds/music.mp3")
pygame.mixer.music.play(-1)

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
    
    if map_tiles[current_tile] == 2:
        game_over = True
     
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
            member.action_token += 1
            initiative.append((random.choice(range(9)) + member.speed,0,member))
        for enemy in enemy_list:
            enemy.action_token += 1
            initiative.append((random.choice(range(9)) + enemy.speed,1,enemy))
        initiative.sort(key = lambda tup: tup[0], reverse = True)
        for roll, team, person in initiative:
            enemy_list[:] = [x for x in enemy_list if x.alive == True]
            party[:] = [x for x in party if x.alive == True]
            for member in party:
                if member.current_hp <= 0:
                    member.alive = False
            for enemy in enemy_list:
                if enemy.current_hp <= 0:
                    enemy.alive = False
            if not any(enemy_list):
                wins += 1
                fighting = False
                break
            elif not any(party):
                fighting = False
                game_over = True
                break
            #blit background
            for i in range(0,tiles):
                display.blit(bg, (i * bg.get_width() + scroll,0))
            for enemy in enemy_list:
                enemy.draw(enemy.current_hp,flip=True)
            for member in party:
                member.draw(member.current_hp)
            draw_panel()
            damage_text_group.update()
            damage_text_group.draw(display)
            hit_text_group.update()
            hit_text_group.draw(display)
            pygame.display.update()
            resolve_dots(person)
            if team == 0:
                if person.alive:
                    if person.action_token > 0:
                        selected_button = None
                        buttons = draw_hero(person)
                        wait_action(buttons, person)
                        person.action_token -= 1
            else:
                if person.alive:
                    if person.action_token > 0:
                        person.take_action()
                        person.action_token -= 1
                        for abil in person.abilities:
                            abil.sound_played = 0 
    
    if not fighting:
        for member in party:
            member.draw(member.current_hp)

    if wins == 1:
        if not any(enemy_list):
            enemy_list.append(enemy5)
            enemy_list.append(enemy6)
            enemy_list.append(enemy7)
            enemy_list.append(enemy8)

    while game_over:
        if wins == 2:
            end = pygame.image.load("images/game_over/victory.png")
            text = "VICTORIOUS"
            colour = yellow
            x = 600
        else:
            end = pygame.image.load("images/game_over/defeat.png")
            text = "DEFEATED"
            colour = red
            x = 650
            
        display.blit(end, (0,0))
        draw_text(text, font_huge, colour, x, 100)
        pygame.display.update()


    pygame.display.update()

pygame.quit()