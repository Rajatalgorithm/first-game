import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))
bg_img = pygame.image.load("universe.jpg")
bg_img = pygame.transform.scale(bg_img, (800, 600))

pygame.display.set_caption("SPACE INVASION")
logo = pygame.image.load("jo.jpg")
pygame.display.set_icon(logo)

mixer.music.load("background music.mp3")
mixer.music.play(-1)

playerImg = pygame.image.load("ufo.png")
P1 = 370
P2 = 480
P1_change = 0

enemyImg = []
e1 = []
e2 = []
e1_change = []
e2_change = []
num_of_enemies = 10

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("alien.png"))
    e1.append(random.randint(0, 736))
    e2.append(random.randint(50, 150))
    e1_change.append(0.3)
    e2_change.append(40)

bulletImg = pygame.image.load("bullets.png")
B1 = 0
B2 = 480
B1_change = 0
B2_change = 40
bullet_state = "ready"

score_value = 0
font = pygame.font.Font("freesansbold.ttf", 18)

textX = 10
textY = 10

over_font = pygame.font.Font("freesansbold.ttf", 62)


def show_score(x, y):
    score = font.render("SCORE:" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    B2_change = 0
    B1_change = 0
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(e1, e2, B1, B2):
    distance = math.sqrt((math.pow(e1 - B1, 2)) + (math.pow(e2 - B2, 2)))
    if distance < 27:
        return True
    else:
        return False


running = True
while running:

    screen.blit(bg_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                P1_change = -0.3
            if event.key == pygame.K_RIGHT:
                P1_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_music = mixer.Sound("bullet sound.mp3")
                    bullet_music.play()
                    B2_change = 0.3
                    B1 = P1
                    fire_bullet(B1, B2)
                if bullet_state == "ready":
                    B1_change = 0.3
                    B2 = P2

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                P1_change = 0

    P1 += P1_change

    if P1 <= 0:
        P1 = 1
    elif P1 >= 736:
        P1 = 736

    for i in range(num_of_enemies):

        if e2[i] > 400:
            for j in range(num_of_enemies):
                e2[j] = 2000
            game_over_text()
            break

        e1[i] += e1_change[i]
        if e1[i] <= 0:
            e1_change[i] = 0.3
            e2[i] += e2_change[i]
        elif e1[i] >= 736:
            e1_change[i] = -0.3
            e2[i] += e2_change[i]

        collision = isCollision(e1[i], e2[i], B1, B2)
        if collision:
            B2 = 480
            bullet_state = "ready"
            score_value += 1
            e1[i] = random.randint(0, 735)
            e2[i] = random.randint(50, 150)

        enemy(e1[i], e2[i], i)

    if B2 <= 0:
        B2 = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(B1, B2)
        B2 -= B2_change

    player(P1, P2)
    show_score(textX, textY)
    pygame.display.update()
