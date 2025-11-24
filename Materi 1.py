import pygame
from sys import exit
import os

# =====================
# GAME VARIABLES
# =====================
TILE_SIZE = 32
GAME_WIDTH = 936
GAME_HEIGHT = 624

PLAYER_X = GAME_WIDTH / 2
PLAYER_Y = GAME_HEIGHT / 2
PLAYER_WIDTH = 32
PLAYER_HEIGHT = 42.6

PLAYER_SHOOT_WIDTH = 52
PLAYER_JUMP_SHOOT_WIDTH = 58
GRAVITY = 0.5
PLAYER_VELOCITY_X = 5
PLAYER_VELOCITY_Y = -12

PLAYER_BULLET_WIDTH = 16
PLAYER_BULLET_HEIGHT = 12
PLAYER_BULLET_VELOCITY_X = 8

FLOOR_Y = GAME_HEIGHT * 3 / 4   # posisi lantai (atas tile lantai)

HEALTH_WIDTH = 16
HEALTH_HEIGHT = 4

KUNTILANAK_WIDTH = 55
KUNTILANAK_HEIGHT = 55

# =====================
# IMAGE LOADER
# =====================
def load_image(image_name, scale=None):
    image = pygame.image.load(os.path.join('.', image_name))
    if scale is not None:
        image = pygame.transform.scale(image, scale)
    return image

# =====================
# LOAD IMAGES
# =====================
background_image = load_image('Mountain.png')
player_image_right = load_image('Mario1Right.png', (PLAYER_WIDTH, PLAYER_HEIGHT))
player_image_left = load_image('Mario1Left.png', (PLAYER_WIDTH, PLAYER_HEIGHT))
player_image_jump_right = load_image('MarioJumpRight.png', (PLAYER_WIDTH, PLAYER_HEIGHT))
player_image_jump_left = load_image('MarioJumpLeft.png', (PLAYER_WIDTH, PLAYER_HEIGHT))
player_image_shoot_right = load_image('MarioShootRight.png', (PLAYER_SHOOT_WIDTH, PLAYER_HEIGHT))
player_image_shoot_left = load_image('MarioShootLeft.png', (PLAYER_SHOOT_WIDTH, PLAYER_HEIGHT))
player_image_bullet = load_image('bullet.png', (PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT))
floor_tile_image = load_image('floor.png')
flying_floor_image = load_image('flying_floor.png')
obstacle_tall_image = load_image('obstacle_block.png')
kuntilanak_image = load_image('Kuntilanak.png', (KUNTILANAK_WIDTH, KUNTILANAK_HEIGHT))
health_image = load_image('health.png', (HEALTH_WIDTH, HEALTH_HEIGHT))

# =====================
# PYGAME INIT
# =====================
pygame.init()
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Dana's Game")
pygame.display.set_icon(player_image_right)
clock = pygame.time.Clock()

#Custom event
INVICIBLE_END = pygame.USEREVENT + 0
SHOOTING_END = pygame.USEREVENT + 1

# =====================
# CLASSES
# =====================
class Player(pygame.Rect):
    class Bullet(pygame.Rect):
        def __init__(self):
            if player.direction == 'left':
                pygame.Rect.__init__(self, player.x, player.y + TILE_SIZE/2, PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT)
                self.velocity_x = - PLAYER_BULLET_VELOCITY_X
            elif player.direction == 'right':
                pygame.Rect.__init__(self, player.x + player.width, player.y + TILE_SIZE/2, PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT)
                self.velocity_x = PLAYER_BULLET_VELOCITY_X
            self.image = player_image_bullet
            self.used = False
            
    def __init__(self):
        pygame.Rect.__init__(self, PLAYER_X, PLAYER_Y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.image = player_image_right
        self.velocity_x = 0
        self.velocity_y = 0
        self.direction = 'right'
        self.jumping = False
        self.invicible = False
        self.max_health = 28
        self.health = self.max_health
        self.shooting = False
        self.bullets = []


    def set_invicible(self, milliseconds=1000):
        self.invicible = True
        pygame.time.set_timer(INVICIBLE_END, milliseconds, 1)

    def update_image(self):
        if self.shooting and self.jumping:
            if self.direction == 'right':
                self.image = player_image_shoot_right
            else:
                self.image = player_image_shoot_left
        elif self.shooting:
            if self.direction == 'right':
                self.image = player_image_shoot_right
            else:
                self.image = player_image_shoot_left
        elif self.jumping:
            if self.direction == 'right':
                self.image = player_image_jump_right
            else:
                self.image = player_image_jump_left
        else:
            if self.direction == 'right':
                self.image = player_image_right
            else:
                self.image = player_image_left
    
    def set_shooting(self):
        if not self.shooting:
            self.shooting = True
            self.bullets.append(Player.Bullet())
            pygame.time.set_timer(SHOOTING_END, 250, 1)

class KUNTILANAK(pygame.Rect):
    def __init__(self, x, y):
        pygame.Rect.__init__(self, x, y, KUNTILANAK_WIDTH, KUNTILANAK_HEIGHT)
        self.image = kuntilanak_image
        self.velocity_y = 0
        self.direction = 'left'
        self.jumping = False
        self.health = 1

class Tile(pygame.Rect):
    def __init__(self, x, y, image):
        self.image = image
        rect = self.image.get_rect(topleft=(x, y))
        pygame.Rect.__init__(self, rect)

# =====================
# MAP SETUP
# =====================
def create_map():
    # lantai utama (floor.png harus panjang 936px)
    tiles.append(Tile(0, FLOOR_Y, floor_tile_image))

    for i in range(3):
        kuntilanak = KUNTILANAK(player.x + TILE_SIZE*(3+i*1.5), TILE_SIZE * 6)
        kuntilanaks.append(kuntilanak)

# =====================
# MOVEMENT & COLLISION
# =====================
def apply_gravity_and_collision(entity, tiles, gravity=0.5, max_fall_speed=15):
    # GRAVITY
    entity.velocity_y += gravity
    entity.velocity_y = min(entity.velocity_y, max_fall_speed)
    entity.y += entity.velocity_y

    entity.jumping = True  # default: di udara

    # COLLISION
    for tile in tiles:
        if entity.colliderect(tile):
            if entity.velocity_y > 0:  # jatuh mengenai lantai
                entity.bottom = tile.top
                entity.velocity_y = 0
                entity.jumping = False
            elif entity.velocity_y < 0:  # kejedot dari bawah
                entity.top = tile.bottom
                entity.velocity_y = 0

def move_player(player, tiles):
    global kuntilanaks
    # ------- HORIZONTAL -------
    player.x += player.velocity_x

    # Batas layar
    if player.left < 0: player.left = 0
    if player.right > GAME_WIDTH: player.right = GAME_WIDTH

    # Collision horizontal
    for tile in tiles:
        if player.colliderect(tile):
            if player.velocity_x > 0:
                player.right = tile.left
            elif player.velocity_x < 0:
                player.left = tile.right
    #bullets
    for bullet in player.bullets:
        bullet.x += bullet.velocity_x
        for kuntilanak in kuntilanaks:
            if kuntilanak.health > 0 and not bullet.used and bullet.colliderect(kuntilanak):
                kuntilanak.health -= 1
                bullet.used = True
    
    player.bullets = [bullet for bullet in player.bullets if not bullet.used 
                      and bullet.x + bullet.width > 0 and bullet.x < GAME_WIDTH]
    kuntilanaks = [kuntilanak for kuntilanak in kuntilanaks if kuntilanak.health > 0]

    # ------- VERTICAL -------
    apply_gravity_and_collision(player, tiles)

def move_kuntilanak(kuntilanak, tiles):
    apply_gravity_and_collision(kuntilanak, tiles)

# =====================
# DRAW
# =====================
def draw():

    window.fill((10, 61, 171))
    window.blit(background_image, (0, 0))

    for tile in tiles:
        window.blit(tile.image, tile)

    player.update_image()
    window.blit(player.image, player)
    for kuntilanak in kuntilanaks:
        window.blit(kuntilanak.image, kuntilanak)

    for bullet in player.bullets:
        window.blit(bullet.image, bullet)
        
    # pygame.draw.rect(window, 'red', (TILE_SIZE, TILE_SIZE, 10 * player.max_health, 10))
    # pygame.draw.rect(window, 'green', (TILE_SIZE, TILE_SIZE, 10 * player.health, 10))
    pygame.draw.rect(window, 'black', (TILE_SIZE, TILE_SIZE, HEALTH_WIDTH, HEALTH_HEIGHT * player.max_health))
    for i in range(player.max_health - player.health, player.max_health):
        window.blit(health_image, (TILE_SIZE, TILE_SIZE + i * HEALTH_HEIGHT, HEALTH_WIDTH, HEALTH_HEIGHT))
# =====================
# GAME START
# =====================
player = Player()
# kuntilanak = KUNTILANAK(player.x + TILE_SIZE*3, TILE_SIZE*6)
kuntilanaks = []
tiles = []
create_map()

# platform terbang & obstacle
tiles.append(Tile(500, 390, flying_floor_image))
tiles.append(Tile(100, FLOOR_Y - 96, obstacle_tall_image))  # tinggi 96, nempel lantai

# =====================
# GAME LOOP
# =====================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == INVICIBLE_END:
            player.invicible = False
        elif event.type == SHOOTING_END:
            player.shooting = False
    keys = pygame.key.get_pressed()

    # lompat
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and not player.jumping:
        player.velocity_y = PLAYER_VELOCITY_Y
        player.jumping = True

    # gerak kiri/kanan
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.velocity_x = -PLAYER_VELOCITY_X
        player.direction = 'left'
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.velocity_x = PLAYER_VELOCITY_X
        player.direction = 'right'
    else:
        player.velocity_x = 0  # lepas tombol → berhenti
    
    if keys[pygame.K_SPACE] or keys[pygame.K_x]:
        player.set_shooting()
        # print(len(player.bullets))
    move_player(player, tiles) 
    for k in kuntilanaks:         
        move_kuntilanak(k, tiles)

    for k in kuntilanaks:
        if not player.invicible and player.colliderect(k):
            print("Nabrak Kuntilanak!")
            player.health -=1
            player.set_invicible()
    draw()
    pygame.display.update()
    clock.tick(60)
