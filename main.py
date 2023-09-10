import pygame
from sys import exit
from random import randint
from random import choice

pygame.init()
screen = pygame.display.set_mode((1500,900))
pygame.display.set_caption("Brawlers")
clock = pygame.time.Clock()

#Classes
class Player:
    def __init__(self, speed, gravity, acceleration, direction, health, specialdamage, specialknockback, physicaldamage, physicalknockback, count,jump):
        self.speed = speed
        self.gravity = gravity
        self.acceleration = acceleration
        self.direction = direction
        self.health = health
        self.specialdamage = specialdamage
        self.specialknockback = specialknockback
        self.physicaldamage = physicaldamage
        self. physicalknockback = physicalknockback
        self.count = count
        self.jump = jump
        self.jumpflag = self.reserve = self.victory = self.physicalflag = False
        self.idle = self.falling = True

class Projectile:
    def __init__(self, speed, shot, direction):
        self.speed = speed
        self.shot = shot
        self.direction = direction

class Healthbar:
    def __init__(self, x, y, w, h, max_hp):
        (self.x, self.y) = (x, y)
        (self.w, self.h) = (w, h)
        self.hp = max_hp
        self.max_hp = max_hp
    def draw(self, surface, color, drawhp):
        self.drawhp = drawhp
        ratio = self.drawhp/self.max_hp
        pygame.draw.rect(surface, (255, 255, 255), (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, color, (self.x, self.y, self.w * ratio, self.h))

#Islands
mainisland_surf = pygame.image.load("Islands/MainIsland.png")
mainisland_surf = pygame.transform.smoothscale(mainisland_surf, (1000, 350))
mainisland_rect = mainisland_surf.get_rect(topleft = (250, 550))

powerisland1_surf = pygame.image.load("Islands/PowerIsland.png").convert_alpha()
powerisland1_surf = pygame.transform.smoothscale(powerisland1_surf, (150, 150))
powerisland1_rect = powerisland1_surf.get_rect(topleft = (100, 200))

powerisland2_surf = pygame.image.load("Islands/PowerIsland.png").convert_alpha()
powerisland2_surf = pygame.transform.smoothscale(powerisland2_surf, (150, 150))
powerisland2_rect = powerisland2_surf.get_rect(topleft = (1250, 200))

#Player 1
player1idle = ["Horse/Horse_Idle1.png", "Horse/Horse_Idle2.png", "Horse/Horse_Idle3.png", "Horse/Horse_Idle4.png"]
player1index = 0
player1_surf = pygame.image.load(player1idle[player1index]).convert_alpha()
player1_surf = pygame.transform.scale(player1_surf, (120, 140))
player1_rect = player1_surf.get_rect(midbottom = (400,100))
player1 = Player(9, 0, 0.001, "R", 70, 5, 15, 3, 15, 0, -20)
player1healthbar = Healthbar(10, 850, 300, 50, player1.health)

#Projectile 1
projectile1_surf = pygame.image.load("Special Attacks/electricball.png").convert_alpha()
projectile1_surf = pygame.transform.scale(projectile1_surf, (60, 60))
projectile1_rect = projectile1_surf.get_rect(topleft = (1100, 1100))
projectile1 = Projectile(10, False, "R")

#Player 2
player2idle = ["Wolf/Wolf_Idle1.png", "Wolf/Wolf_Idle2.png", "Wolf/Wolf_Idle3.png"]
player2index = 0
player2_surf = pygame.image.load(player2idle[player2index]).convert_alpha()
player2_surf = pygame.transform.scale(player2_surf, (110, 155))
player2_rect = player2_surf.get_rect(midbottom = (1100,100))
player2 = Player(7.5, 0, 0.001, "L", 70, 3.5, 40, 3.5, 20, 0, -19.5)
player2healthbar = Healthbar(1190, 850, 300, 50, player2.health)

#Projectile 2
projectile2_surf = pygame.image.load("Special Attacks/fireball_left.png").convert_alpha()
projectile2_surf = pygame.transform.scale(projectile2_surf, (50, 33))
projectile2_rect = projectile2_surf.get_rect(topleft = (1100, 1100))
projectile2 = Projectile(10, False, "L")

#Powerups
powerupone_surf = pygame.image.load("PowerUps/HealthRegenerator.png").convert_alpha()
powerupone_surf = pygame.transform.scale(powerupone_surf, (63, 50))
powerupone_rect = powerupone_surf.get_rect(topleft = (2000, 2000))

poweruptwo_surf = pygame.image.load("PowerUps/HealthRegenerator.png").convert_alpha()
poweruptwo_surf = pygame.transform.scale(poweruptwo_surf, (63, 50))
poweruptwo_rect = poweruptwo_surf.get_rect(topleft = (3000, 2000))

powerups = ["Health", "Speed", "Jump", "Attack", "Knockback"]
powerup = "None"

#Functions:
def player1_jump():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        if player1.jumpflag != True:
            player1.gravity = player1.jump
            player1.jumpflag = True

def player1_movement():
    global player1_surf
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player1_rect.x -= player1.speed
        player1.speed += player1.acceleration
        if player1.direction == "R":
            player1_surf = pygame.transform.flip(player1_surf, True, False)
            player1.direction = "L"
    elif keys[pygame.K_d]:
        player1_rect.x += player1.speed
        player1.speed += player1.acceleration
        if player1.direction == "L":
            player1_surf = pygame.transform.flip(player1_surf, True, False)
            player1.direction = "R"
    else: player1.speed = 9

def player1_gravity():
    player1_rect.y += player1.gravity
    if player1.falling == True: player1.gravity += 0.5
    if player1_rect.y < 500:
        if player1_rect.colliderect(mainisland_rect) == False: player1.falling = True
        else:
            player1.gravity = 0
            player1.jumpflag = False
            player1.falling = False
    if player1_rect.y < 100:
        if player1_rect.colliderect(powerisland2_rect) == False: player1.falling = True
        else:
            player1.gravity = 0
            player1.jumpflag = False
            player1.falling = False
    if player1_rect.y < 100:
        if player1_rect.colliderect(powerisland1_rect) == False: player1.falling = True
        else:
            player1.gravity = 0
            player1.jumpflag = False
            player1.falling = False

def player1_shoot():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_v]:
        if projectile1.shot != True:
            projectile1.shot = True
            projectile1.direction = player1.direction
            (projectile1_rect.x, projectile1_rect.y) = (player1_rect.x + 50, player1_rect.y + 25)
    if projectile1.shot:
        if projectile1.direction == "R": projectile1_rect.x += projectile1.speed
        elif projectile1.direction == "L": projectile1_rect.x -= projectile1.speed

def projectile1_collisions():
    if projectile1_rect.colliderect(player2_rect):
        (projectile1_rect.x, projectile1_rect.y) = (1100, 1100)
        player2.health -= player1.specialdamage
        if projectile1.direction == "R": player2_rect.x += player1.specialknockback
        elif projectile1.direction == "L": player2_rect.x -= player1.specialknockback
        projectile1.shot = False
    elif (projectile1_rect.x > 1500) or (projectile1_rect.x < 0):
        (projectile1_rect.x, projectile1_rect.y) = (1100, 1100)
        projectile1.shot = False

def player1_attack():
    player1.physicalflag = True
    player1.idle = False
    player1.speed = 4.5

def player2_jump():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        if player2.jumpflag != True:
            player2.gravity = player2.jump
            player2.jumpflag = True

def player2_movement():
    global player2_surf
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player2_rect.x -= player1.speed
        player2.speed += player1.acceleration
        if player2.direction == "R":
            player2_surf = pygame.transform.flip(player2_surf, True, False)
            player2.direction = "L"
    elif keys[pygame.K_RIGHT]:
        player2_rect.x += player2.speed
        player2.speed += player2.acceleration
        if player2.direction == "L":
            player2_surf = pygame.transform.flip(player2_surf, True, False)
            player2.direction = "R"
    else: player2.speed = 7.5

def player2_gravity():
    player2_rect.y += player2.gravity
    if player2.falling == True: player2.gravity += 0.5
    if player2_rect.y < 500:
        if player2_rect.colliderect(mainisland_rect) == False: player2.falling = True
        else:
            player2.gravity = 0
            player2.jumpflag = False
            player2.falling = False
    if player2_rect.y < 100:
        if player2_rect.colliderect(powerisland2_rect) == False: player2.falling = True
        else:
            player2.gravity = 0
            player2.jumpflag = False
            player2.falling = False
    if player2_rect.y < 100:
        if player2_rect.colliderect(powerisland1_rect) == False: player2.falling = True
        else:
            player2.gravity = 0
            player2.jumpflag = False
            player2.falling = False

def player2_shoot():
    global projectile2_surf
    keys = pygame.key.get_pressed()
    if keys[pygame.K_l]:
        if projectile2.shot != True:
            projectile2.shot = True
            projectile2.direction = player2.direction
            (projectile2_rect.x, projectile2_rect.y) = (player2_rect.x + 50, player2_rect.y + 50)
    if projectile2.shot:
        if projectile2.direction == "R":
            projectile2_rect.x += projectile2.speed
            projectile2_surf = pygame.image.load("Special Attacks/fireball_right.png").convert_alpha()
            projectile2_surf = pygame.transform.scale(projectile2_surf, (50, 33))
        elif projectile2.direction == "L":
            projectile2_rect.x -= projectile2.speed
            projectile2_surf = pygame.image.load("Special Attacks/fireball_left.png").convert_alpha()
            projectile2_surf = pygame.transform.scale(projectile2_surf, (50, 33))

def projectile2_collisions():
    if projectile2_rect.colliderect(player1_rect):
        (projectile2_rect.x, projectile2_rect.y) = (1100, 1100)
        player1.health -= player2.specialdamage
        if projectile2.direction == "R": player1_rect.x += player2.specialknockback
        elif projectile2.direction == "L": player1_rect.x -= player2.specialknockback
        projectile2.shot = False
    elif (projectile2_rect.x > 1500) or (projectile2_rect.x < 0):
        (projectile2_rect.x, projectile2_rect.y) = (1100, 1100)
        projectile2.shot = False

def player2_attack():
    player2.physicalflag = True
    player2.idle = False
    player2.speed = 3.25

def collisions():
    if player1.physicalflag == True:
        if player1_rect.colliderect(player2_rect):
            player2.health -= player1.physicaldamage
            if player1.direction == "R": player2_rect.x += player1.physicalknockback
            elif player1.direction == "L": player2_rect.x -= player1.physicalknockback
            player1.physicalflag = False
            player1.idle = True
            player1.speed = 9
            player1.count = 0
    if player2.physicalflag == True:
        if player2_rect.colliderect(player1_rect):
            player1.health -= player2.physicaldamage
            if player2.direction == "R": player1_rect.x += player2.physicalknockback
            elif player2.direction == "L": player1_rect.x -= player2.physicalknockback
            player2.physicalflag = False
            player2.idle = True
            player2.speed = 7.5
            player2.count = 0

def powerupspawn():
    global powerupone_surf
    global poweruptwo_surf
    global powerup
    decision = randint(1,1000)
    if decision == 1:
        powerup = powerups[0]
        powerupone_surf = pygame.image.load("PowerUps/HealthRegenerator.png").convert_alpha()
        powerupone_surf = pygame.transform.scale(powerupone_surf, (63, 50))
        poweruptwo_surf = pygame.image.load("PowerUps/HealthRegenerator.png").convert_alpha()
        poweruptwo_surf = pygame.transform.scale(poweruptwo_surf, (63, 50))
        ((powerupone_rect.x, powerupone_rect.y), (poweruptwo_rect.x, poweruptwo_rect.y)) = ((140,140), (1290, 140))
    if decision == 11:
        powerup = powerups[1]
        powerupone_surf = pygame.image.load("PowerUps/SpeedBoost.png").convert_alpha()
        powerupone_surf = pygame.transform.scale(powerupone_surf, (54, 96))
        poweruptwo_surf = pygame.image.load("PowerUps/SpeedBoost.png").convert_alpha()
        poweruptwo_surf = pygame.transform.scale(poweruptwo_surf, (54, 96))
        ((powerupone_rect.x, powerupone_rect.y), (poweruptwo_rect.x, poweruptwo_rect.y)) = ((160,100), (1310, 100))
    if decision == 21:
        powerup = powerups[2]
        powerupone_surf = pygame.image.load("PowerUps/JumpBoost.png").convert_alpha()
        powerupone_surf = pygame.transform.scale(powerupone_surf, (61, 96))
        poweruptwo_surf = pygame.image.load("PowerUps/JumpBoost.png").convert_alpha()
        poweruptwo_surf = pygame.transform.scale(poweruptwo_surf, (61, 96))
        ((powerupone_rect.x, powerupone_rect.y), (poweruptwo_rect.x, poweruptwo_rect.y)) = ((145,100), (1295, 100))
    if decision == 31:
        powerup = powerups[3]
        powerupone_surf = pygame.image.load("PowerUps/AttackBoost.png").convert_alpha()
        powerupone_surf = pygame.transform.scale(powerupone_surf, (91, 96))
        poweruptwo_surf = pygame.image.load("PowerUps/AttackBoost.png").convert_alpha()
        poweruptwo_surf = pygame.transform.scale(poweruptwo_surf, (91, 96))
        ((powerupone_rect.x, powerupone_rect.y), (poweruptwo_rect.x, poweruptwo_rect.y)) = ((130, 100), (1280, 100))
    if decision == 41:
        powerup = powerups[4]
        powerupone_surf = pygame.image.load("PowerUps/KnockbackBoost.png").convert_alpha()
        powerupone_surf = pygame.transform.scale(powerupone_surf, (96, 88))
        poweruptwo_surf = pygame.image.load("PowerUps/KnockbackBoost.png").convert_alpha()
        poweruptwo_surf = pygame.transform.scale(poweruptwo_surf, (96, 88))
        ((powerupone_rect.x, powerupone_rect.y), (poweruptwo_rect.x, poweruptwo_rect.y)) = ((130, 100), (1280, 100))
    if decision == 51:
        powerup = choice(powerups)
        powerupone_surf = pygame.image.load("PowerUps/RandomBoost.png").convert_alpha()
        powerupone_surf = pygame.transform.scale(powerupone_surf, (100, 100))
        poweruptwo_surf = pygame.image.load("PowerUps/RandomBoost.png").convert_alpha()
        poweruptwo_surf = pygame.transform.scale(poweruptwo_surf, (100, 100))
        ((powerupone_rect.x, powerupone_rect.y), (poweruptwo_rect.x, poweruptwo_rect.y)) = ((130, 100), (1280, 100))


def player1powerup():
    if player1_rect.colliderect(powerupone_rect) or player1_rect.colliderect(poweruptwo_rect):
        if powerup == "Health":
            player1.health += 15
            ((powerupone_rect.x, powerupone_rect.y), (poweruptwo_rect.x, poweruptwo_rect.y)) = ((2000, 2000), (3000, 3000))
        elif powerup == "Speed":
            player1.speed += 2
            ((powerupone_rect.x, powerupone_rect.y), (poweruptwo_rect.x, poweruptwo_rect.y)) = ((2000, 2000), (3000, 3000))
        elif powerup == "Jump":
            player1.jump -= 0.5
            ((powerupone_rect.x, powerupone_rect.y), (poweruptwo_rect.x, poweruptwo_rect.y)) = ((2000, 2000), (3000, 3000))
        elif powerup == "Attack":
            player1.physicaldamage += 1
            player1.specialdamage += 1
            ((powerupone_rect.x, powerupone_rect.y), (poweruptwo_rect.x, poweruptwo_rect.y)) = ((2000, 2000), (3000, 3000))
        elif powerup == "Knockback":
            player1.physicalknockback += 10
            player1.specialknockback += 10
            ((powerupone_rect.x, powerupone_rect.y), (poweruptwo_rect.x, poweruptwo_rect.y)) = ((2000, 2000), (3000, 3000))

def player2powerup():
    if player2_rect.colliderect(powerupone_rect) or player2_rect.colliderect(poweruptwo_rect):
        if powerup == "Health":
            player2.health += 15
            ((powerupone_rect.x, powerupone_rect.y), (poweruptwo_rect.x, poweruptwo_rect.y)) = ((2000, 2000), (3000, 3000))
        elif powerup == "Speed":
            player2.speed += 2
            ((powerupone_rect.x, powerupone_rect.y), (poweruptwo_rect.x, poweruptwo_rect.y)) = ((2000, 2000), (3000, 3000))
        elif powerup == "Jump":
            player2.jump -= 0.5
            ((powerupone_rect.x, powerupone_rect.y), (poweruptwo_rect.x, poweruptwo_rect.y)) = ((2000, 2000), (3000, 3000))
        elif powerup == "Attack":
            player2.physicaldamage += 1
            player2.specialdamage += 1
            ((powerupone_rect.x, powerupone_rect.y), (poweruptwo_rect.x, poweruptwo_rect.y)) = ((2000, 2000), (3000, 3000))
        elif powerup == "Knockback":
            player2.physicalknockback += 10
            player2.specialknockback += 10
            ((powerupone_rect.x, powerupone_rect.y), (poweruptwo_rect.x, poweruptwo_rect.y)) = ((2000, 2000), (3000, 3000))

def victorycheck():
    if player1.health <= 0 or player1_rect.y >= 900:
        player2.victory = True

    elif player2.health <= 0 or player2_rect.y >= 900:
        player1.victory = True

#Music
pygame.mixer.music.load("Battle Music.mp3")
pygame.mixer.music.play(0)

while True:
    screen.fill((135, 206, 235))

    #Islands
    screen.blit(mainisland_surf, mainisland_rect)
    screen.blit(powerisland1_surf, powerisland1_rect)
    screen.blit(powerisland2_surf, powerisland2_rect)

    # Player 2 Idle Animation
    if player2.idle == True:
        if player2index <= 2:
            player2_surf = pygame.image.load(player2idle[int(player2index)]).convert_alpha()
            player2_surf = pygame.transform.scale(player2_surf, (110, 150))
            if player2.direction == "R": player2_surf = pygame.transform.flip(player2_surf, True, False)
            player2index += 0.25
        else:
            player2index = 0
    else:
        if player2.count < 5:
            player2.count += 1
            if player2.direction == "R":
                player2_surf = pygame.image.load("Wolf\Wolf_Physical_Right.png").convert_alpha()
                player2_surf = pygame.transform.scale(player2_surf, (170, 170))
            elif player2.direction == "L":
                player2_surf = pygame.image.load("Wolf\Wolf_Physical_Left.png").convert_alpha()
                player2_surf = pygame.transform.scale(player2_surf, (170, 170))
        else:
            player2.count = 0
            player2.idle = True
            player2.physicalflag = False
            player2.speed = 7.5

    #Player 1 Idle Animation
    if player1.idle:
        if player1index <= 3:
            player1_surf = pygame.image.load(player1idle[int(player1index)]).convert_alpha()
            player1_surf = pygame.transform.scale(player1_surf, (120, 130))
            if player1.direction == "L": player1_surf = pygame.transform.flip(player1_surf, True, False)
            player1index += 0.25
        else: player1index = 0
    else:
        if player1.count < 1:
            player1.count += 0.5
            if player1.direction == "R":
                player1_surf = pygame.image.load("Horse\Horse_Physical_Right.png").convert_alpha()
                player1_surf = pygame.transform.scale(player1_surf, (120, 130))
            elif player1.direction == "L":
                player1_surf = pygame.image.load("Horse\Horse_Physical_Left.png").convert_alpha()
                player1_surf = pygame.transform.scale(player1_surf, (120, 130))
        else:
            player1.count = 0
            player1.idle = True
            player1.physicalflag = False
            player1.speed = 9

    #Player 1 Main Island Collision
    if player1_rect.y > 500:
        if player1_rect.colliderect(mainisland_rect): player1.speed = 0
    if player1_rect.y > 100:
        if player1_rect.colliderect(powerisland1_rect): player1.speed = 0
        if player1_rect.colliderect(powerisland2_rect): player1.speed = 0

    # Player 2 Main Island Collision
    if player2_rect.y > 500:
        if player2_rect.colliderect(mainisland_rect): player2.speed = 0
    if player2_rect.y > 100:
        if player2_rect.colliderect(powerisland1_rect): player2.speed = 0
        if player2_rect.colliderect(powerisland2_rect): player2.speed = 0

    #PLayer 1 Basics
    screen.blit(player1_surf, player1_rect)
    player1_movement()
    player1_jump()
    player1_gravity()
    player1_shoot()
    player1powerup()
    projectile1_collisions()

    #PLayer 2 Basics
    screen.blit(player2_surf, player2_rect)
    player2_movement()
    player2_jump()
    player2_gravity()
    player2_shoot()
    player2powerup()
    projectile2_collisions()

    #Attack and Health
    collisions()
    victorycheck()

    if player1.health > 70: player1healthbar.draw(screen, (0, 0, 255), 70)
    else: player1healthbar.draw(screen, (0,0,255), player1.health)

    if player2.health > 70: player2healthbar.draw(screen, (255, 0, 0), 70)
    else: player2healthbar.draw(screen, (255, 0, 0), player2.health)

    screen.blit(projectile1_surf, projectile1_rect)
    screen.blit(projectile2_surf, projectile2_rect)

    #PowerUps
    screen.blit(powerupone_surf, powerupone_rect)
    screen.blit(poweruptwo_surf, poweruptwo_rect)
    powerupspawn()

    #Victory
    if player1.victory:
        screen.fill((2, 2, 23, 255))
        winscreen1_surf = pygame.image.load("Win Screens\Magic_Win_Screen.png").convert_alpha()
        winscreen1_surf = pygame.transform.smoothscale(winscreen1_surf, (900, 900))
        winscreen1_rect = winscreen1_surf.get_rect(topleft=(300, 0))
        screen.blit(winscreen1_surf, winscreen1_rect)


    if player2.victory:
        screen.fill((38, 12, 2, 255))
        winscreen2_surf = pygame.image.load("Win Screens\Melee_Win_Screen.png").convert_alpha()
        winscreen2_surf = pygame.transform.smoothscale(winscreen2_surf, (900, 900))
        winscreen2_rect = winscreen2_surf.get_rect(topleft=(300, 0))
        screen.blit(winscreen2_surf, winscreen2_rect)

    pygame.display.update()
    clock.tick(240)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            #Physical Attacks
            if event.key == pygame.K_k: player2_attack()
            elif event.key == pygame.K_b: player1_attack()
            #Reserve Usage
            if event.key == pygame.K_s:
                if player1.reserve == False:
                    player1.reserve = True
                    player1.health += 20
            elif event.key == pygame.K_DOWN:
                if player2.reserve == False:
                    player2.reserve = True
                    player2.health += 30
        # Closing Screen
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()