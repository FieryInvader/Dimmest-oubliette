import pygame


pygame.init()

clock = pygame.time.Clock()
FPS = 60
screen_width = 1700
screen_height = 900

screen = pygame.display
screen.set_caption('Dimmest oubliet')

display = screen.set_mode((screen_width,screen_height))

class Square(pygame.sprite.Sprite):
    def __init__(self, x, y,name):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f"images/{name}.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def update(self):
        if key[pygame.K_d]:
            self.rect.move_ip(1, 0)
        elif key[pygame.K_a]:
            self.rect.move_ip(-1,0)

dismas = Square(400, 600,'dismas')
reynauld = Square(530,590,'reynauld')
paracelcus = Square(230,600,'paracelsus')
junia = Square(100,600,'junia')

bg = pygame.image.load('images/background.jpg')

party = pygame.sprite.Group()
party.add(dismas)
party.add(reynauld)
party.add(paracelcus)
party.add(junia)

run = True
while run:
    
    key = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    display.blit(bg,(50,50))
    party.update()
    party.draw(display)
    pygame.display.update()

pygame.quit()