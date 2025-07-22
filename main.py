import pygame
import random
import math
import time
from pygame import mixer
from pygame.locals import *

pygame.init()
pygame.mixer.init()

# Creating window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Fortnite")
icon = pygame.image.load('assets/spaceship_32.png')
pygame.display.set_icon(icon)

# Loading background image
bgImg = pygame.image.load('assets/background.jpg')

# All levels music
easy_mode_music = 'assets/bg_music_easy.wav'
med_mode_music = 'assets/bg_music_med.wav'
diff_mode_music = 'assets/bg_music_hard.wav'

# Loading bullet music
bulletSound = mixer.Sound('assets/laser.wav')

# Rendering fonts
font = pygame.font.Font('freesansbold.ttf', 24)
fontButton = pygame.font.SysFont('Arial Black', 16)

# Loading images
bulletImg = pygame.image.load('assets/bullet.png')
playerImg = pygame.image.load('assets/spaceship_64.png')

# Global variables
isBulletFired = False
enemySpeed = 0.1
enemyWave = 0
howManyEnemyPerWave = 0

def player(x, y):
    screen.blit(playerImg, (x, y))

class Enemy:
    def __init__(self, xAxis, yAxis):
        self.xAxis = xAxis
        self.yAxis = yAxis
        self.image = pygame.image.load('assets/enemy.png')
        self.yChange = enemySpeed

    def move(self):
        self.yAxis += self.yChange

    def makeEnemy(self):
        screen.blit(self.image, (self.xAxis, self.yAxis))

def bullet(x, y):
    global isBulletFired
    isBulletFired = True
    bulletSound.play()
    screen.blit(bulletImg, (x + 16, y))  # Centered on spaceship

def distanceBw(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2) < 27

def showScore(score):
    scoreFont = font.render("Score: " + str(score), True, (235, 225, 215))
    screen.blit(scoreFont, (10, 20))

class Button:
    button_col = (30, 26, 53)
    hover_col = (120, 0, 120)
    click_col = (130, 10, 135)
    text_col = (210, 210, 210)
    width = 150
    height = 50

    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text
        self.isButtonClicked = False

    def drawButton(self):
        action = False
        pos = pygame.mouse.get_pos()
        button_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                self.isButtonClicked = True
                pygame.draw.rect(screen, self.click_col, button_rect, border_radius=15)
            elif pygame.mouse.get_pressed()[0] == 0 and self.isButtonClicked:
                self.isButtonClicked = False
                action = True
            else:
                pygame.draw.rect(screen, self.hover_col, button_rect, border_radius=15)
        else:
            pygame.draw.rect(screen, self.button_col, button_rect, border_radius=15)

        text_img = fontButton.render(self.text, True, self.text_col)
        text_rect = text_img.get_rect(center=button_rect.center)
        screen.blit(text_img, text_rect)

        return action

# Center buttons horizontally
center_x = (800 - Button.width) // 2
easy = Button(center_x, 180, 'Easy Mode')
medium = Button(center_x, 250, 'Medium Mode')
hard = Button(center_x, 320, 'Hard Mode')
quitGame = Button(center_x, 390, 'Quit Game')

def start():
    global isBulletFired, enemyWave, howManyEnemyPerWave

    playerxAxis = 370
    playeryAxis = 480
    playerXchange = 0
    playerYchange = 0

    bulletxAxis = 0
    bulletyAxis = playeryAxis
    bulletYchange = 2.5

    score = 0
    enemies = []
    run = True

    while run:
        screen.blit(bgImg, (0, 0))
        showScore(score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            playerXchange = -1.25
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            playerXchange = 1.25
        elif keys[pygame.K_w] or keys[pygame.K_UP]:
            playerYchange = -0.5
            bulletyAxis = playeryAxis
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            playerYchange = 0.5
            bulletyAxis = playeryAxis
        else:
            playerXchange = 0
            playerYchange = 0

        if keys[pygame.K_SPACE] or keys[pygame.K_LCTRL]:
            if not isBulletFired:
                bulletxAxis = playerxAxis
                bullet(bulletxAxis, bulletyAxis)

        playerxAxis += playerXchange
        playeryAxis += playerYchange

        playerxAxis = max(0, min(playerxAxis, 736))
        playeryAxis = max(0, min(playeryAxis, 536))

        if bulletyAxis <= 0:
            isBulletFired = False
            bulletyAxis = 480

        if len(enemies) == 0:
            enemyWave += howManyEnemyPerWave
            for _ in range(enemyWave):
                enemies.append(Enemy(random.randint(0, 736), random.randint(-250, 0)))

        for enemy in enemies[:]:
            if enemy.yAxis >= 600 or distanceBw(playerxAxis, playeryAxis, enemy.xAxis, enemy.yAxis):
                run = False

            enemy.makeEnemy()
            enemy.move()

            if distanceBw(enemy.xAxis, enemy.yAxis, bulletxAxis, bulletyAxis):
                enemies.remove(enemy)
                isBulletFired = False
                bulletyAxis = 480
                score += 1

        if isBulletFired:
            bulletyAxis -= bulletYchange
            bullet(bulletxAxis, bulletyAxis)

        player(playerxAxis, playeryAxis)
        pygame.display.update()

    mixer.music.load('assets/sad_sound.wav')
    mixer.music.play()
    youLoseFont = font.render("You Lose", True, (235, 225, 215))
    scoreFont = font.render("Score: " + str(score), True, (235, 225, 215))
    screen.blit(youLoseFont, (345, 260))
    screen.blit(scoreFont, (345, 285))
    pygame.display.update()
    time.sleep(3)

def play():
    mixer.music.load(easy_mode_music)
    mixer.music.play(-1)

    run = True
    while run:
        screen.blit(bgImg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        global enemySpeed, enemyWave, howManyEnemyPerWave
        enemyWave = 0

        if easy.drawButton():
            mixer.music.load(easy_mode_music)
            mixer.music.play(-1)
            howManyEnemyPerWave = 2
            enemySpeed = 0.1
            start()

        elif medium.drawButton():
            mixer.music.load(med_mode_music)
            mixer.music.play(-1)
            howManyEnemyPerWave = 3
            enemySpeed = 0.2
            start()

        elif hard.drawButton():
            mixer.music.load(diff_mode_music)
            mixer.music.play(-1)
            howManyEnemyPerWave = 5
            enemySpeed = 0.25
            start()

        elif quitGame.drawButton():
            run = False

        pygame.display.update()

play()
pygame.quit()
