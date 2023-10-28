import pygame, random




image_rock = pygame.image.load('moon/stone.png')
sizes = [[64, 64], [96, 96], [128, 128], [160, 160], [198, 198]]
rocks = []
image_laser = pygame.image.load('moon/laser.png')
image_exp = (pygame.image.load('moon/Explosion/regularExplosion00.png'),
              pygame.image.load('moon/Explosion/regularExplosion01.png'),
              pygame.image.load('moon/Explosion/regularExplosion02.png'),
              pygame.image.load('moon/Explosion/regularExplosion03.png'),
              pygame.image.load('moon/Explosion/regularExplosion04.png'),
              pygame.image.load('moon/Explosion/regularExplosion05.png'),
              pygame.image.load('moon/Explosion/regularExplosion06.png'),
              pygame.image.load('moon/Explosion/regularExplosion07.png'),
              pygame.image.load('moon/Explosion/regularExplosion08.png'))
image_star = pygame.image.load('moon/star.png')

for size in sizes:
    rocks.append(pygame.transform.scale(image_rock, size))
RES = (1280, 720)

ekran = pygame.display.set_mode(RES)
clock = pygame.time.Clock()
FPS = 60



running = True
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
RECORD = 0
class Player(pygame.sprite.Sprite,):
    def __init__(self, pose):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('moon/spaceship.png')
        self.rect = self.image.get_rect()
        self.speed = 15
        self.shoot_delay = 100
        self.last_shoot = pygame.time.get_ticks()
        self.rect.center = pose
    
    

    def update(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
           
        elif keys[pygame.K_s]:
            self.rect.y += self.speed
          
        elif keys[pygame.K_a]:
            self.rect.x -= self.speed
          
        elif keys[pygame.K_d]:
            self.rect.x += self.speed

        self.shoot()

    def shoot(self):
        now = pygame.time.get_ticks()
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_SPACE]:
            if now - self.last_shoot - self.shoot_delay > 0:
                coords = self.rect.center
                ans = [(coords[0] + 17, coords[1] - 25), (coords[0] - 17, coords[1] - 25), (coords[0] + 27, coords[1] - 5), (coords[0] - 27, coords[1] -5)]
                bullet = Bullet((random.choice(ans)))
                all_sprites.add(bullet)
                bullets.add(bullet)
                self.last_shoot = now



class Bullet(pygame.sprite.Sprite):
    def __init__(self, coords):
        super().__init__()
        self.image = image_laser
        self.rect = self.image.get_rect()
        self.rect.center = coords
        self.dx = 0
        self.dy = -15


    def update(self):
        coords = self.rect.center
        if(coords[1] + self.dy < 50):
            self.kill()
        elif(coords[1] + self.dy > 1230):
            self.kill()
        else:
            coords = coords[0], coords[1] + self.dy
        self.rect.center = coords

class power_up(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_star
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(50, 1230), random.randint(50, 50))
        self.speed = 10

    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 720:
            self.kill()
        if pygame.sprite.spritecollide(p, Power_up, True,):
            self.kill()

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.index = random.randint(0, 4)
        self.image = rocks[self.index]
        self.radius = sizes[self.index][0] // 2
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(1280 - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.rot_speed = random.randrange(-4, 4)
        self.rot_angle = 0
        self.dx = random.uniform(-7, 7)
        self.dy = random.uniform(1, 7)
        self.last_update = pygame.time.get_ticks()


    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            new_image = pygame.transform.rotate(rocks[self.index], self.rot_angle)
            self.rot_angle = (self.rot_angle + self.rot_speed) % 360
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        coords = self.rect.center
        #enemy bounces off the borders
        if(coords[0] + self.dx <- 128):
            self.kill()
        elif(coords[0] + self.dx > 1408):
            self.kill()
        else:
            coords = coords[0] + self.dx, coords[1]
        if(coords[1] + self.dy <- 128):
            self.kill()
        elif(coords[1] + self.dy > 848):
            self.kill()
        else:
            coords = coords[0], coords[1] + self.dy
        self.rect.center = coords
        self.rotate()
        

class Explosion(pygame.sprite.Sprite):
    def __init__(self, coords):
        super().__init__()
        self.stage = 0 
        self.image = image_exp[self.stage]
        self.rect = self.image.get_rect()
        self.rect.center = coords
        self.delay = 75 
        self.last_stage = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_stage >= self.delay:
            if self.stage == 8:
                self.kill()
            else:
                self.stage += 1
                self.last_stage = now
                self.image = image_exp[self.stage]
        

p = Player((640, 600))
player = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(p)
player.add(p)
bullets = pygame.sprite.Group()
shootables = pygame.sprite.Group()
Power_up = pygame.sprite.Group()


def spawn():
    for i in range(10 - len(shootables)):
        t = Rock()
        all_sprites.add(t)
        shootables.add(t)
spawn()

def spawn_up():
    for i in range(1 - len(Power_up)):
        w = power_up()
        Power_up.add(w)
        all_sprites.add(w)
        if pygame.sprite.groupcollide(player, Power_up, True, True):
            break


pygame.init()
font = pygame.font.SysFont('ARIAL', 25)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    spawn_up()
    spawn()
    ekran.fill(BLACK)
    all_sprites.draw(ekran)
    all_sprites.update()
    player_hit = pygame.sprite.spritecollide(p, shootables, False, pygame.sprite.collide_circle)
    if player_hit:
        running = False


    hit = pygame.sprite.groupcollide(shootables, bullets, True, True)
    for i in hit:
        t = Explosion(i.rect.center)
        all_sprites.add(w)
        RECORD += 10

    caption = font.render(str(RECORD),True, 'WHITE')

    all_sprites.draw(ekran)
    ekran.blit(caption, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)
    pygame.display.update()
    pygame.display.flip()




pygame.quit()