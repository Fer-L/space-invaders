import pygame
import os
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")


#Opponents
SHIP_1 = pygame.image.load(os.path.join("Resources/images", "ship_1.png"))
SHIP_2 = pygame.image.load(os.path.join("Resources/images", "ship_2.png"))
SHIP_3 = pygame.image.load(os.path.join("Resources/images", "ship_3.png"))

# Player ship
SHIP = pygame.image.load(os.path.join("Resources/images", "space-ship.png"))

# Laser do player
LASER = pygame.image.load(os.path.join("Resources/images", "laser.png"))

# Laser do inimigo
LASER_ENEMY = pygame.image.load(os.path.join("Resources/images", "laser_inimigo.png"))

# Background
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("Resources/images", "background-image.png")), (WIDTH, HEIGHT))

class Ship:
    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))

    def get_width(self):
        return self.ship_img.get_width()
    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship):
    def __init__(self, x, y, health = 100):
        super().__init__(x, y, health)
        self.ship_img = SHIP
        self.laser_img = LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

class Enemy(Ship):

    SHIP_MAP = {
        "1" : (SHIP_1),
        "2" : (SHIP_2),
        "3" : (SHIP_3)
    }

    def __init__(self, x, y, types,health = 100):
       super().__init__(x, y, health)
       self.ship_img = self.SHIP_MAP[types]
       self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)

    bullets = []
    enemies = []
    wave_length = 5
    enemy_vel = 1

    player_vel = 2

    player = Player(300, 630)

    clock = pygame.time.Clock()

    def redraw_window():
        WIN.blit(BACKGROUND, (0,0))
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
           enemy.draw(WIN)

        player.draw(WIN)

        pygame.display.update()

    while run:
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["1", "2", "3"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel > 0: # left
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH: # right
            player.x += player_vel

        for enemy in enemies:
            enemy.move(enemy_vel)

        redraw_window()

main()