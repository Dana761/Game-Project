import pygame
from sys import exit
import os
import sys
import random

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".mp3", ".wav", ".ogg"}

def resource_path(relative_path):
    """
    Biar path asset jalan di:
    - Python biasa
    - File hasil PyInstaller (.exe / .app)
    """
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS  # folder temp PyInstaller
    else:
        base_path = os.path.dirname(__file__)  # folder script biasa
    return os.path.join(base_path, relative_path)

def safe_asset_path(filename):
    ext = os.path.splitext(filename)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Blocked unsafe file type: {filename}")

    path = resource_path(os.path.join("assets", filename))

    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing asset: {filename}")

    return path

pygame.mixer.init()

# ==============
# SOUND LOADER
# ==============
def load_sound(name, volume=1.0):
    path = safe_asset_path(name)   
    sound = pygame.mixer.Sound(path)
    sound.set_volume(volume)
    return sound

jump_sound         = load_sound("Jump_sound.MP3",         0.5)
tembak_sarung_sound = load_sound("Tembak_sarung_sound.MP3", 0.2)
enemy_death_sound  = load_sound("enemy_death_sound.MP3", 0.5)
player_hit_sound   = load_sound("hit_sound.MP3",         0.5)
life_energy_sound  = load_sound("life_energy_sound.MP3", 0.5)
bismillah_sound    = load_sound("bismillah.MP3",         0.7)
game_lose_sound    = load_sound("game_lose.MP3",         0.7)
game_win_sound     = load_sound("game_win.MP3",          0.7)

bismillah_duration = bismillah_sound.get_length()

# =====================
# GAME VARIABLES
# =====================
TILE_SIZE = 32
GAME_WIDTH = 960
GAME_HEIGHT = 540

PLAYER_X = GAME_WIDTH / 2
PLAYER_Y = GAME_HEIGHT / 2
PLAYER_WIDTH = 35.4
PLAYER_HEIGHT = 75

GRAVITY = 0.5
PLAYER_VELOCITY_X = 5
PLAYER_VELOCITY_Y = -12

PLAYER_BULLET_WIDTH = 20
PLAYER_BULLET_HEIGHT = 28
PLAYER_BULLET_VELOCITY_X = 8

HEALTH_WIDTH = 16
HEALTH_HEIGHT = 4

KUNTILANAK_WIDTH = 30
KUNTILANAK_HEIGHT = 75
KUNTILANAK_JONGKOK_HEIGHT = 40.72

KUNTILANAK_BULLET_WIDTH = 12
KUNTILANAK_BULLET_HEIGHT = KUNTILANAK_BULLET_WIDTH
KUNTILANAK_BULLET_VELOCITY_X = 2
KUNTILANAK_BULLET_VELOCITY_Y = KUNTILANAK_BULLET_VELOCITY_X

POCONG_WIDTH = 15.95
POCONG_HEIGHT = 75
POCONG_VELOCITY_X = 2
POCONG_VELOCITY_Y = 1

GENDERUWO_WIDTH = 58.82
GENDERUWO_HEIGHT = 100
GENDERUWO_VELOCITY_X = 4
GENDERUWO_VELOCITY_Y = PLAYER_VELOCITY_Y

LIFE_ENERGY_WIDTH = 20
LIFE_ENERGY_HEIGHT = LIFE_ENERGY_WIDTH
BIG_ENERGY_WIDTH = 28
BIG_ENERGY_HEIGHT = BIG_ENERGY_WIDTH
ITEM_VELOCITY_Y = -11

# =====================
# SAFE SPAWN ZONE
# =====================
SAFE_SPAWN_RADIUS_X = TILE_SIZE * 8  # jarak aman kiri-kanan dari posisi awal player

# =====================
# JUMP STATS (OTOMATIS DARI KONSTANTA)
# =====================
vy0 = abs(PLAYER_VELOCITY_Y)   # kecepatan awal loncat (positif)
g = GRAVITY

# total frame di udara (naik + turun)
MAX_JUMP_FRAMES = int(2 * vy0 / g)

# jarak horizontal maksimum (kalau tombol kiri/kanan ditahan)
MAX_JUMP_DISTANCE_X = PLAYER_VELOCITY_X * MAX_JUMP_FRAMES

# jarak aman antar platform (biar nggak pixel perfect)
SAFE_MAX_GAP_X = int(MAX_JUMP_DISTANCE_X * 0.8)   # misal 80% dari maksimum
SAFE_MIN_GAP_X = int(SAFE_MAX_GAP_X * 0.5)        # minimum gap biar nggak nempel

# tinggi loncatan maksimum
MAX_JUMP_HEIGHT = int((vy0 ** 2) / (2 * g))
SAFE_MAX_DELTA_Y = int(MAX_JUMP_HEIGHT * 0.7)     # beda tinggi aman antar platform

# =====================
# IMAGE LOADER
# =====================
def load_image(image_name, scale=None):
    path = resource_path(os.path.join("assets", image_name))
    image = pygame.image.load(path)   # TANPA convert_alpha di sini
    if scale is not None:
        image = pygame.transform.scale(image, scale)
    return image

# =====================
# LOAD IMAGES
# =====================
background_image = load_image('Background.png', (GAME_WIDTH, GAME_HEIGHT))
player_image_right = load_image('Ustad_kanan.png', (PLAYER_WIDTH, PLAYER_HEIGHT))
player_image_left = load_image('Ustad_kiri.png', (PLAYER_WIDTH, PLAYER_HEIGHT))
player_image_jump_right = load_image('Ustad_lompat_kanan.png', (51.6, 70))
player_image_jump_left = load_image('Ustad_lompat_kiri.png', (51.6, 70))
player_image_shoot_right = load_image('Ustad_tembak_kanan.png', (50, PLAYER_HEIGHT))
player_image_shoot_left = load_image('Ustad_tembak_kiri.png', (50, PLAYER_HEIGHT))
player_image_bullet = load_image('bullet.png', (PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT))
player_image_walk_right = [load_image(f'Ustad_jalan_kanan{i}.png', (46.39, PLAYER_HEIGHT)) for i in range(2)]
player_image_walk_left = [load_image(f'Ustad_jalan_kiri{i}.png', (46.39, PLAYER_HEIGHT)) for i in range(2)]
player_image_shoot_walk_right = [load_image(f'Ustad_jalan_tembak_kanan{i}.png', (46.39, PLAYER_HEIGHT)) for i in range(2)]
player_image_shoot_walk_left = [load_image(f'Ustad_jalan_tembak_kiri{i}.png', (46.39, PLAYER_HEIGHT)) for i in range(2)]
floor_tile_image = load_image('floor.png', (184.4, 60))
flying_tile_image = load_image('flying_floor.png', (277.5, 30))
kuntilanak_left_image = load_image('KuntilanakKiri.png', (KUNTILANAK_WIDTH, KUNTILANAK_HEIGHT))
kuntilanak_right_image = load_image('KuntilanakKanan.png', (KUNTILANAK_WIDTH, KUNTILANAK_HEIGHT))
kuntilanak_left_jongkok_image = load_image('Kuntil_jongkok_kiri.png', (KUNTILANAK_WIDTH, KUNTILANAK_JONGKOK_HEIGHT))
kuntilanak_right_jongkok_image = load_image('Kuntil_jongkok_kanan.png', (KUNTILANAK_WIDTH, KUNTILANAK_JONGKOK_HEIGHT))
kuntilanak_image_bullet = load_image('enemy_bullet.png', (KUNTILANAK_BULLET_WIDTH, KUNTILANAK_BULLET_HEIGHT))
genderuwo_left_image = load_image('genderuwo_kiri.png', (GENDERUWO_WIDTH, GENDERUWO_HEIGHT))
genderuwo_right_image = load_image('genderuwo_kanan.png', (GENDERUWO_WIDTH, GENDERUWO_HEIGHT))
genderuwo_jump_left_image = load_image('genderuwo_lompat_kiri.png', (GENDERUWO_WIDTH, GENDERUWO_HEIGHT))
genderuwo_jump_right_image = load_image('genderuwo_lompat_kanan.png', (GENDERUWO_WIDTH, GENDERUWO_HEIGHT))
health_image = load_image('health.png', (HEALTH_WIDTH, HEALTH_HEIGHT))
life_energy_image = load_image('LifeEnergy.png', (LIFE_ENERGY_WIDTH, LIFE_ENERGY_HEIGHT))
big_life_energy_image = load_image('BigLifeEnergy.png', (BIG_ENERGY_WIDTH, BIG_ENERGY_HEIGHT))
kuburan_image = load_image('Kuburan.png', (42.2, 25))
pocong_image_right = load_image('Pocong_kanan.png', (POCONG_WIDTH, POCONG_HEIGHT))
pocong_image_left = load_image('Pocong_kiri.png', (POCONG_WIDTH, POCONG_HEIGHT))
masjid_image = load_image('masjid.png', (271, 200))
home_page = load_image('Home.png', (GAME_WIDTH, GAME_HEIGHT))   # front menu
story_page = load_image('Story.png', (GAME_WIDTH, GAME_HEIGHT))
game_guides = [load_image(f'Game_guide{i}.png', (GAME_WIDTH, GAME_HEIGHT)) for i in range(1, 6)]
pause_page = load_image('Game_pause.png', (GAME_WIDTH, GAME_HEIGHT))
game_over_page = load_image('Game_over.png', (GAME_WIDTH, GAME_HEIGHT))
game_win_page = load_image('Game_win.png', (GAME_WIDTH, GAME_HEIGHT))
good_luck_image = load_image('Good_luck.png', (GAME_WIDTH, GAME_HEIGHT))
logo_image = load_image('logo.png', (64, 64))

FLOOR_Y = GAME_HEIGHT - floor_tile_image.get_height()
FLYING_W = flying_tile_image.get_width()

# =====================
# GAME STATE
# =====================
game_state = "home"        # "home", "story", "playing", "good luck", "paused", "guide"
current_guide_index = 0    # index slide guide yang lagi ditampilkan
previous_state = None      # buat tau balik dari guide/story ke mana

FLOOR_Y = GAME_HEIGHT - floor_tile_image.get_height()
FLYING_W = flying_tile_image.get_width()

# =====================
# PYGAME INIT
# =====================
pygame.init()
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Ustad's Adventure")
pygame.display.set_icon(logo_image)
clock = pygame.time.Clock()
pygame.font.init()
game_font = pygame.font.SysFont('Arial', 24)
game_over = False
game_won = False

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
        self.walking = False
        self.current_walk_index = 0
        self.last_update_walk_index = pygame.time.get_ticks()
        self.last_shot_time = 0
        self.shoot_cooldown = 200

    def set_invicible(self, milliseconds=1000):
        self.invicible = True
        pygame.time.set_timer(INVICIBLE_END, milliseconds, 1)

    def update_image(self):
        if self.walking and not self.jumping:
            if self.shooting:
                if self.direction == 'right':
                    self.image = player_image_shoot_walk_right[self.current_walk_index]
                else:
                    self.image = player_image_shoot_walk_left[self.current_walk_index]
            else:
                if self.direction == 'right':
                    self.image = player_image_walk_right[self.current_walk_index]
                else:
                    self.image = player_image_walk_left[self.current_walk_index]
            self.update_walking_animation()
        else:
            self.current_walk_index = 0

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
        
    def update_walking_animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_update_walk_index > 250:
            self.last_update_walk_index = now
            self.current_walk_index = (self.current_walk_index + 1) % len(player_image_walk_right)

    def set_shooting(self):
        now = pygame.time.get_ticks()

        if now - self.last_shot_time < self.shoot_cooldown:
            return  # block spam

        self.last_shot_time = now

        if not self.shooting:
            self.shooting = True
            self.bullets.append(Player.Bullet())
            tembak_sarung_sound.play()
            pygame.time.set_timer(SHOOTING_END, 250, 1)

class Kuntilanak(pygame.Rect):
    class Bullet(pygame.Rect):
        def __init__(self, kuntilanak, velocity_y):
            if kuntilanak.direction == 'left':
                pygame.Rect.__init__(self, kuntilanak.x, kuntilanak.y + TILE_SIZE/2, KUNTILANAK_BULLET_WIDTH, KUNTILANAK_BULLET_HEIGHT)
                self.velocity_x = - KUNTILANAK_BULLET_VELOCITY_X
            elif kuntilanak.direction == 'right':
                pygame.Rect.__init__(self, kuntilanak.x + kuntilanak.width, kuntilanak.y + TILE_SIZE/2, KUNTILANAK_BULLET_WIDTH, KUNTILANAK_BULLET_HEIGHT)
                self.velocity_x = KUNTILANAK_BULLET_VELOCITY_X
            self.velocity_y = velocity_y
            self.image = kuntilanak_image_bullet
            self.used = False

    def __init__(self, x, y):
        pygame.Rect.__init__(self, x, y, KUNTILANAK_WIDTH, KUNTILANAK_HEIGHT)
        self.image = kuntilanak_left_image
        self.velocity_y = 0
        self.direction = 'left'
        self.jumping = False
        self.health = 2
        self.bullets = []
        self.last_fired = pygame.time.get_ticks()
        self.guarding = False
    
    def update_image(self):
        # simpan dulu posisi kaki
        old_bottom = self.bottom

        if self.direction == 'right':
            if self.guarding:
                self.image = kuntilanak_right_jongkok_image
            else:
                self.image = kuntilanak_right_image
        elif self.direction == 'left':
            if self.guarding:
                self.image = kuntilanak_left_jongkok_image
            else:
                self.image = kuntilanak_left_image

        # SAMAKAN ukuran rect dengan ukuran gambar,
        # tapi kaki tetap di posisi lama
        self.width  = self.image.get_width()
        self.height = self.image.get_height()
        self.bottom = old_bottom
    
    def set_shooting(self):
        # Hanya nembak kalau:
        # 1) player cukup dekat (jarak X <= 4 tile)
        # 2) player lagi di LANTAI (bukan flying floor)
        if abs(self.x - player.x) <= TILE_SIZE * 10 and is_player_on_floor():
            self.guarding = False
            now = pygame.time.get_ticks()
            if now - self.last_fired > 1000:  # delay 1 detik antar tembakan
                self.last_fired = now
                # CUMA SATU PELURU, LURUS (velocity_y = 0)
                self.bullets.append(Kuntilanak.Bullet(self, 0))
        else:
            # kalau player jauh / di udara / di flying floor → guard/jongkok
            self.guarding = True

class Pocong(pygame.Rect):
    def __init__(self, x, y):
        pygame.Rect.__init__(self, x, y, POCONG_WIDTH, POCONG_HEIGHT)
        self.image = pocong_image_right
        self.direction = 'right'
        self.health = 3 
        self.velocity_x = POCONG_VELOCITY_X
        self.velocity_y = POCONG_VELOCITY_Y
        self.start_x = x
        self.start_y = y
        self.max_range_x = TILE_SIZE * 4
        self.max_range_y = TILE_SIZE
        self.jumping = False

    def update_image(self):
        if self.direction == 'right':
            self.image = pocong_image_right
        elif self.direction == 'left':
            self.image = pocong_image_left

class Genderuwo(pygame.Rect):
    def __init__(self, x, y):
        pygame.Rect.__init__(self, x, y, GENDERUWO_WIDTH, GENDERUWO_HEIGHT)
        self.image = genderuwo_right_image
        self.direction = 'right'
        self.velocity_x = 0
        self.velocity_y = 0
        self.jumping = False  
        # ===== AI LONCAT YANG LEBIH PINTER =====
        self.last_jump_time = 0          # kapan terakhir lompat
        self.jump_cooldown = 700         # cooldown lompat (ms), 0.7 detik  

    def update_image(self):
        if self.direction == 'right':
            # kalau mau beda sprite waktu lompat
            self.image = genderuwo_jump_right_image if self.jumping else genderuwo_right_image
        else:
            self.image = genderuwo_jump_left_image if self.jumping else genderuwo_left_image

class Tile(pygame.Rect):
    def __init__(self, x, y, image):
        self.image = image
        rect = self.image.get_rect(topleft=(x, y))
        pygame.Rect.__init__(self, rect)

class Item(pygame.Rect):
    def __init__(self, x, y, image):
        pygame.Rect.__init__(self, x, y, image.get_width(), image.get_height())
        self.image = image
        self.jumping = False
        self.velocity_y = ITEM_VELOCITY_Y
        self.used = False

# =====================
# GLOBAL LISTS
# =====================
player = None
kuntilanaks = []
kuntilanak_bullets = []
tiles = []
flying_tiles = []
items = []
kuburans = []
pocongs = []
genderuwos = []

def is_player_on_floor():
    """True kalau player lagi berdiri di lantai (tiles), bukan di flying floor."""
    if player is None:
        return False

    for tile in tiles:  # cuma cek lantai, flying_tiles nggak dicek
        if (
            player.bottom == tile.top and      # kaki nempel di atas tile
            player.right > tile.left and      # overlap di sumbu X
            player.left < tile.right
        ):
            return True
    return False

def is_on_tile(entity, tile_list):
    """True kalau entity lagi berdiri di atas salah satu tile di tile_list."""
    for tile in tile_list:
        if (
            entity.bottom == tile.top and  # kaki nempel di atas tile
            entity.right > tile.left and
            entity.left < tile.right
        ):
            return True
    return False

def get_masjid_rect():
    """Balik Rect posisi masjid di koordinat dunia sekarang."""
    if not tiles:
        return None
    last_tile = tiles[-1]
    masjid_x = last_tile.right - masjid_image.get_width()
    masjid_y = last_tile.top - masjid_image.get_height()
    return pygame.Rect(masjid_x, masjid_y, masjid_image.get_width(), masjid_image.get_height())

def is_in_masjid_zone(rect, buffer=150):
    """
    True kalau rect ini terlalu dekat area masjid.
    buffer = jarak aman di depan masjid (sebelum masjid).
    """
    masjid_rect = get_masjid_rect()
    if not masjid_rect:
        return False

    zone_left = masjid_rect.left - buffer  # mulai zona “bersih”
    zone_right = masjid_rect.right         # sampai ujung masjid

    # kalau center X sudah masuk zona ini → anggap kena
    return rect.centerx >= zone_left

# =====================
# MAP SETUP
# =====================
def get_masjid_range():
    """Balikin (left, right) area masjid di sumbu X."""
    if not tiles:
        return None, None
    last_tile = tiles[-1]
    masjid_x = last_tile.right - masjid_image.get_width()
    masjid_right = masjid_x + masjid_image.get_width()
    return masjid_x, masjid_right

def spawn_kuntilanaks(count=3):
    """Spawn kuntilanak di atas tile lantai (bukan flying floor), random di mana saja."""
    if not tiles:
        return

    masjid_left, masjid_right = get_masjid_range()

    attempts = 0
    max_attempts = count * 20

    while len(kuntilanaks) < count and attempts < max_attempts:
        attempts += 1
        tile = random.choice(tiles)  # hanya ground tiles

        max_x_start = tile.width - KUNTILANAK_WIDTH
        if max_x_start < 0:
            continue

        x = tile.x + random.randint(0, max_x_start)

        k = Kuntilanak(x, 0)
        k.bottom = tile.top

        if is_in_masjid_zone(k):
            continue

        # JANGAN spawn di belakang / terlalu dekat depan player
        if k.centerx <= PLAYER_X + SAFE_SPAWN_RADIUS_X:
            continue

        # ❌ JANGAN spawn di area masjid / setelah masjid
        if masjid_left is not None and k.centerx >= masjid_left:
            continue

        # hindari overlap dengan kuntilanak lain
        if any(k.colliderect(other) for other in kuntilanaks):
            continue

        kuntilanaks.append(k)

def spawn_genderuwo():
    """Spawn genderuwo DI LANTAI, JELAS KELIHATAN DI KIRI PLAYER."""
    if not tiles:
        return

    # ambil tile paling kiri (lantai pertama)
    tile = tiles[0]

    # taruh genderuwo di atas lantai, agak ke tengah tile
    x = tile.centerx - GENDERUWO_WIDTH // 2
    y = tile.top - GENDERUWO_HEIGHT

    g = Genderuwo(x, y - 5)   # sedikit di atas, biar langsung ke-snap ke lantai
    apply_gravity_and_collision(g, tiles)  # langsung tempelin ke lantai

    g.direction = 'right'  # langsung ngadep ke ustad
    genderuwos.append(g)

def create_map():
    # lantai panjang
    for i in range(103):
        tile = Tile(i * floor_tile_image.get_width(), FLOOR_Y, floor_tile_image)
        tiles.append(tile)

    spawn_kuntilanaks(60)

def reset_game():
    global player, kuntilanaks, kuntilanak_bullets, tiles, flying_tiles, items, kuburans, pocongs, game_over, game_won, genderuwos
    player = Player()
    kuntilanaks = []
    kuntilanak_bullets = []
    tiles = []
    flying_tiles = []
    items = []
    kuburans = []
    pocongs = []
    genderuwos = []

    create_map()
    create_flying_tiles()
    spawn_random_kuburan(250)
    adjust_flying_tiles_height()              # atur tinggi dulu
    adjust_flying_floor_gap_for_edge_kuburan()# atur jarak kalau ujungnya ada kuburan
    spawn_pocongs_on_flying_tiles()           # baru spawn pocong di posisi final
    spawn_genderuwo()

    game_over = False
    game_won = False

# platform terbang & obstacle
def create_flying_tiles():
    flying_h = flying_tile_image.get_height()

    min_y = GAME_HEIGHT // 4
    CLEARANCE = 10
    max_y = int(FLOOR_Y - KUNTILANAK_HEIGHT - CLEARANCE - flying_h)

    if max_y < min_y:
        max_y = min_y

    x = int(PLAYER_X + SAFE_SPAWN_RADIUS_X)
    y = max_y   # di bawah

    EDGE_MIN_GAP = SAFE_MIN_GAP_X
    EDGE_MAX_GAP = SAFE_MAX_GAP_X

    prev_right = x + FLYING_W
    flying_tiles.append(Tile(x, y, flying_tile_image))

    for _ in range(41):
        edge_gap = random.randint(EDGE_MIN_GAP, EDGE_MAX_GAP)
        x = prev_right + edge_gap

        delta_y = random.randint(-SAFE_MAX_DELTA_Y, SAFE_MAX_DELTA_Y)
        y += delta_y

        if y < min_y:
            y = min_y
        if y > max_y:
            y = max_y

        tile = Tile(x, y, flying_tile_image)
        flying_tiles.append(tile)
        prev_right = tile.right

def spawn_pocongs_on_flying_tiles():
    """Spawn 1 pocong di SETIAP flying floor (kecuali yang deket masjid)."""
    if not flying_tiles:
        return

    masjid_left, masjid_right = get_masjid_range()

    for tile in flying_tiles:
        # posisi awal pocong: berdiri pas di atas tile, di tengah
        x = tile.centerx - POCONG_WIDTH // 2
        y = tile.top - POCONG_HEIGHT

        p = Pocong(x, y)
        p.bottom = tile.top
        p.start_x = p.x
        p.start_y = p.y

        # JANGAN spawn di zona masjid
        if is_in_masjid_zone(p):
            continue

        # JANGAN spawn di area masjid / setelah masjid
        if masjid_left is not None and p.centerx >= masjid_left:
            continue

        # atur range patroli pocong supaya nggak keluar dari tile
        max_range = min(TILE_SIZE * 4, (tile.width - POCONG_WIDTH) // 2)
        if max_range <= 0:
            continue

        p.max_range_x = max_range
        p.velocity_y = 0
        p.max_range_y = 0  # nggak usah lompat vertikal jauh

        # hindari overlap dengan pocong lain (kalau kepasang 2 tile nempel)
        if any(p.colliderect(other) for other in pocongs):
            continue

        pocongs.append(p)

def is_under_flying_tile(fly_tile, rect):
    """Cek apakah rect (kuburan) berada di bawah sebuah flying tile."""
    return (
        rect.centerx > fly_tile.left and
        rect.centerx < fly_tile.right and
        rect.top >= fly_tile.bottom
    )

def spawn_random_kuburan(total=5):
    """Sebar kuburan random, tidak saling tumpang tindih.
       - Kalau di flying floor: posisinya tengah atau ujung kanan, dan
         tiap flying floor maksimal cuma boleh 1 kuburan di atasnya.
       - Di bawah tiap flying floor maksimal cuma boleh 1 kuburan,
         dan hanya kalau jarak vertikalnya cukup tinggi (clearance).
    """
    all_floors = tiles + flying_tiles   # gabungkan semua platform
    if not all_floors:
        return

    kub_w = kuburan_image.get_width()
    kub_h = kuburan_image.get_height()

    attempts = 0
    max_attempts = total * 30

    MIN_GAP_UNDER_FLY = 60  # jarak aman minimal antara kuburan dan bawah flying tile

    while len(kuburans) < total and attempts < max_attempts:
        attempts += 1
        tile = random.choice(all_floors)

        # posisi X khusus kalau tile adalah flying floor
        if tile in flying_tiles:
            # tengah atau ujung kanan (bukan ujung kiri)
            if random.random() < 0.5:
                # tengah
                x = tile.centerx - kub_w // 2
            else:
                # ujung kanan
                x = tile.right - kub_w

            # ===== (1) BATAS: TIAP FLYING TILE MAKSIMAL 1 KUBURAN DI ATASNYA =====
            already_on_this_flying = False
            for existing in kuburans:
                # existing.bottom == tile.top → kuburan ada di atas tile
                # dan overlap di sumbu X
                if (
                    existing.bottom == tile.top and
                    existing.right > tile.left and
                    existing.left < tile.right
                ):
                    already_on_this_flying = True
                    break

            if already_on_this_flying:
                # sudah ada kuburan di flying floor ini → skip
                continue

        else:
            # lantai biasa: random di lebar tile
            max_x_start = tile.width - kub_w
            if max_x_start < 0:
                continue
            x = tile.x + random.randint(0, max_x_start)

        y = tile.top - kub_h
        new_rect = pygame.Rect(x, y, kub_w, kub_h)

        # >>> JANGAN TARUH KUBURAN DI BELAKANG / TERLALU DEKAT DEPAN PLAYER <<<
        if new_rect.centerx <= PLAYER_X + SAFE_SPAWN_RADIUS_X:
            continue

        # >>> JANGAN TARUH KUBURAN DI ZONA MASJID <<<
        if is_in_masjid_zone(new_rect):
            continue

        # >>> JANGAN TARUH KUBURAN DI AREA MASJID / SETELAH MASJID <<<
        masjid_left, masjid_right = get_masjid_range()
        if masjid_left is not None and new_rect.centerx >= masjid_left:
            continue

        # >>> JANGAN NUBRUK KUBURAN LAIN <<<
        if any(new_rect.colliderect(k) for k in kuburans):
            continue

        # >>> JAGA JARAK MINIMAL ANTAR KUBURAN <<<
        MIN_KUBURAN_DISTANCE = 200
        too_close = False
        for k in kuburans:
            dx = abs(new_rect.centerx - k.centerx)
            dy = abs(new_rect.centery - k.centery)
            if dx < MIN_KUBURAN_DISTANCE and dy < MIN_KUBURAN_DISTANCE:
                too_close = True
                break

        if too_close:
            continue

        # >>> JANGAN NUBRUK KUNTILANAK JUGA <<<
        if any(new_rect.colliderect(k) for k in kuntilanaks):
            continue

        # >>> ATUR KUBURAN DI BAWAH FLYING TILE <<<
        too_many_under_flying = False
        bad_gap_under_flying = False

        for fly in flying_tiles:
            if is_under_flying_tile(fly, new_rect):
                # hitung kuburan yang sudah ada di bawah flying tile ini
                count_under = 0
                for existing in kuburans:
                    if is_under_flying_tile(fly, existing):
                        count_under += 1
                if count_under >= 1:
                    # udah ada kuburan di bawah flying tile ini → tolak posisi ini
                    too_many_under_flying = True

                # cek jarak vertikal antara bawah flying tile dan atas kuburan baru
                vertical_gap = new_rect.top - fly.bottom
                if vertical_gap < MIN_GAP_UNDER_FLY:
                    # jarak terlalu sempit, player susah lompat → tolak
                    bad_gap_under_flying = True

                # cukup cek 1 flying tile yang kena
                break

        if too_many_under_flying or bad_gap_under_flying:
            continue

        # kalau semua cek lolos, baru tambahin ke list
        kub = Tile(x, y, kuburan_image)
        kub.parent_tile = tile     
        kuburans.append(kub)

def has_edge_kubur_on_flying(tile, edge_margin=10):
    """True kalau di ujung kanan flying floor ini ada kuburan yang nempel di atasnya."""
    for kubur in kuburans:
        # kita pakai parent_tile biar pasti kuburan ini milik tile ini
        if getattr(kubur, "parent_tile", None) is tile:
            # cek apakah kuburan ini nempel di ujung kanan tile
            if kubur.right >= tile.right - edge_margin:
                return True
    return False

def adjust_flying_floor_gap_for_edge_kuburan(max_edge_gap=None):
    """
    Kalau ada flying floor yang di ujung kanannya ada kuburan,
    jarak ke flying floor berikutnya dipendekin supaya lebih gampang dilompat.
    """
    if max_edge_gap is None:
        max_edge_gap = SAFE_MIN_GAP_X   # atau int(SAFE_MIN_GAP_X * 0.7)

    # asumsi: flying_tiles urut dari kiri ke kanan (sesuai create_flying_tiles)
    for i, tile in enumerate(flying_tiles[:-1]):  # sampai tile ke-2 terakhir
        if not has_edge_kubur_on_flying(tile):
            continue

        next_tile = flying_tiles[i + 1]
        gap = next_tile.left - tile.right

        # kalau gap sudah kecil, biarin aja
        if gap <= max_edge_gap:
            continue

        # hitung seberapa banyak harus digeser ke kiri
        shift = gap - max_edge_gap

        # geser flying floor berikutnya ke kiri
        next_tile.x -= shift

        # kuburan yang nempel di flying floor itu ikut geser
        for kubur in kuburans:
            if getattr(kubur, "parent_tile", None) is next_tile:
                kubur.x -= shift

def adjust_flying_tiles_height(clearance=160):
    """
    Naikkan flying floor kalau ada kuburan terlalu dekat di bawahnya.
    clearance = jarak aman vertikal antara bawah flying tile dan atas kuburan.
    """
    flying_h = flying_tile_image.get_height()

    # batas aman supaya platform nggak naik terlalu tinggi / terlalu rendah
    min_y = GAME_HEIGHT // 6
    max_y = int(FLOOR_Y - KUNTILANAK_HEIGHT - 10 - flying_h)

    for idx, tile in enumerate(flying_tiles):
        # flying floor pertama (index 0) jangan diutak-atik tingginya
        if idx == 0:
            continue

        # cari kuburan yang paling dekat di bawah tile ini
        closest_kubur_top = None
        for kubur in kuburans:
            overlap_x = (kubur.right > tile.left and
                         kubur.left < tile.right)
            if not overlap_x:
                continue

            if kubur.top < tile.bottom:
                continue

            if closest_kubur_top is None or kubur.top < closest_kubur_top:
                closest_kubur_top = kubur.top

        if closest_kubur_top is None:
            continue

        vertical_gap = closest_kubur_top - tile.bottom

        if vertical_gap < clearance:
            desired_bottom = closest_kubur_top - clearance
            new_y = desired_bottom - tile.height

            if new_y < min_y:
                new_y = min_y
            if new_y > max_y:
                new_y = max_y

            tile.y = new_y

            for kubur in kuburans:
                if getattr(kubur, "parent_tile", None) is tile:
                    kubur.bottom = tile.top


        # kalau nggak ada kuburan di bawah tile ini → skip
        if closest_kubur_top is None:
            continue

        vertical_gap = closest_kubur_top - tile.bottom

        # kalau jarak terlalu mepet → naikin tile
        if vertical_gap < clearance:
            desired_bottom = closest_kubur_top - clearance
            new_y = desired_bottom - tile.height

            # clamp ke batas atas/bawah yang aman
            if new_y < min_y:
                new_y = min_y
            if new_y > max_y:
                new_y = max_y

            # naikkan flying tile
            tile.y = new_y

            # >>> KUBURAN YANG NEMPEL DI ATAS TILE INI IKUT NAIK <<<
            for kubur in kuburans:
                if getattr(kubur, "parent_tile", None) is tile:
                    kubur.bottom = tile.top

# =====================
# MOVEMENT & COLLISION
# =====================
def apply_gravity_and_collision(entity, tiles, gravity=0.5, max_fall_speed=15):
    # tambahin gravitasi
    entity.velocity_y += gravity
    if entity.velocity_y > max_fall_speed:
        entity.velocity_y = max_fall_speed

    # simpan posisi sebelum gerak (buat cek datangnya dari atas / bawah / samping)
    old_rect = entity.copy()

    # gerak vertikal
    entity.y += entity.velocity_y
    entity.jumping = True  # default: dianggap di udara

    for tile in tiles:
        if entity.colliderect(tile):
            # JATUH DARI ATAS (old bottom masih di atas tile)
            if entity.velocity_y > 0 and old_rect.bottom <= tile.top:
                entity.bottom = tile.top
                entity.velocity_y = 0
                entity.jumping = False

            # KEJEDOT DARI BAWAH (old top masih di bawah tile)
            elif entity.velocity_y < 0 and old_rect.top >= tile.bottom:
                entity.top = tile.bottom
                entity.velocity_y = 0
            # kalau datangnya dari samping → DIEMIN (nggak dipaksa naik/turun)

def get_safe_item_position(base_x, base_y, image):
    """Cari posisi item yang nggak nabrak kuburan.
       Kalau posisi awal nabrak kuburan, geser ke samping kuburan.
    """
    w = image.get_width()
    h = image.get_height()
    rect = pygame.Rect(base_x, base_y, w, h)

    # Cek dulu: nabrak kuburan yang mana?
    colliding_kubur = None
    for k in kuburans:
        if rect.colliderect(k):
            colliding_kubur = k
            break

    # Kalau nggak nabrak kuburan apa pun → pakai posisi awal
    if colliding_kubur is None:
        return base_x, base_y

    candidates = []

    # Coba taruh di KANAN kuburan
    x_right = colliding_kubur.right + 5
    candidates.append(pygame.Rect(x_right, base_y, w, h))

    # Coba taruh di KIRI kuburan
    x_left = colliding_kubur.left - w - 5
    candidates.append(pygame.Rect(x_left, base_y, w, h))

    # Pilih kandidat yang nggak nabrak kuburan lain
    for r in candidates:
        if not any(r.colliderect(k) for k in kuburans):
            return r.x, r.y

    # Fallback terakhir: geser jauh kiri/kanan sampai nemu yang aman
    SHIFT = kuburan_image.get_width() + w + 10
    for dx in (-SHIFT, SHIFT, -2 * SHIFT, 2 * SHIFT):
        test_rect = rect.copy()
        test_rect.x += dx
        if not any(test_rect.colliderect(k) for k in kuburans):
            return test_rect.x, test_rect.y

    # Kalau bener-bener nggak nemu, ya udah balikin posisi awal
    return base_x, base_y

def drop_item(character):
    random_number = random.randint(1, 100)

    if 0 < random_number <= 20:
        img = big_life_energy_image
    elif 20 < random_number <= 50:
        img = life_energy_image
    else:
        return  # nggak drop apa-apa

    # Drop di atas kepala musuh, agak di tengah badan
    base_x = character.centerx - img.get_width() // 2
    base_y = character.top - img.get_height()

    # Cari posisi yang nggak nabrak kuburan (otomatis geser ke samping kalau perlu)
    safe_x, safe_y = get_safe_item_position(base_x, base_y, img)

    items.append(Item(safe_x, safe_y, img))

def move_player_x(velocity_x):
    # 1. Geser dulu seluruh map
    move_map_x(velocity_x)

    # 2. Cek apakah setelah digeser, player jadi nabrak SAMPING tile/flying floor
    illegal = False
    for tile in tiles + flying_tiles:
        if player.colliderect(tile):

            # Kalau posisi player PERSIS di atas tile (landing),
            # jangan dianggap tabrakan samping
            if player.bottom <= tile.top:
                continue

            # Kalau player di bawah tile (misal di bawah flying floor),
            # juga bukan tabrakan samping
            if player.top >= tile.bottom:
                continue

            # Sampai sini berarti badan player "nempel" DI SAMPING tile
            illegal = True
            break

    # 3. Kalau gerakan ilegal (nabrak samping), balikin posisi map
    if illegal:
        move_map_x(-velocity_x)

def move_map_x(velocity_x):
    for tile in tiles:
        tile.x += velocity_x

    for tile in flying_tiles:          
        tile.x += velocity_x

    for kuntilanak in kuntilanaks:
        kuntilanak.x += velocity_x
        for bullet in kuntilanak.bullets:
            bullet.x += velocity_x

    for bullet in kuntilanak_bullets:
        bullet.x += velocity_x

    for item in items:
        item.x += velocity_x

    for kuburan in kuburans:
        kuburan.x += velocity_x
    
    for pocong in pocongs:
        pocong.start_x += velocity_x
        pocong.x += velocity_x 

    for genderuwo in genderuwos:
        genderuwo.x += velocity_x


def move_player(player, tiles):
    global game_over
    # ------- HORIZONTAL -------
    # Batas layar
    if player.left < 0:
        player.left = 0
    if player.right > GAME_WIDTH:
        player.right = GAME_WIDTH

    # bullets
    for bullet in player.bullets:
        bullet.x += bullet.velocity_x
        for kuntilanak in kuntilanaks:
            if kuntilanak.health > 0 and not bullet.used and bullet.colliderect(kuntilanak):
                bullet.used = True
                kuntilanak.health -= 1
                if kuntilanak.health <= 0:
                    enemy_death_sound.play() 
                    drop_item(kuntilanak)
                    kuntilanak_bullets.extend(kuntilanak.bullets)
        
        for pocong in pocongs:
            if pocong.health > 0 and not bullet.used and bullet.colliderect(pocong):
                bullet.used = True
                pocong.health -= 1
                if pocong.health <= 0:
                    enemy_death_sound.play() 
                    drop_item(pocong)
    
    player.bullets = [
        bullet for bullet in player.bullets
        if (not bullet.used) and (bullet.x + bullet.width > 0) and (bullet.x < GAME_WIDTH)
    ]

    # ------- VERTICAL -------
    apply_gravity_and_collision(player, tiles + flying_tiles)

    if player.health <= 0 or player.y > GAME_HEIGHT:
        game_over = True

def move_kuntilanak(kuntilanak, tiles):
    global kuntilanaks, kuntilanak_bullets
    if kuntilanak.centerx < player.centerx:
        kuntilanak.direction = 'right'  
    else:
        kuntilanak.direction = 'left'
    
    kuntilanak.set_shooting()
    for bullet in kuntilanak.bullets:
        bullet.x += bullet.velocity_x
        bullet.y += bullet.velocity_y
        if not player.invicible and player.colliderect(bullet):
            player.health -= 2
            bullet.used = True
            player_hit_sound.play()  
            player.set_invicible()

    # Bersihkan peluru di luar layar / sudah dipake
    kuntilanak.bullets = [
        bullet for bullet in kuntilanak.bullets
        if (not bullet.used) and (bullet.x + bullet.width > 0) and (bullet.x < GAME_WIDTH)
    ]
    
    kuntilanaks = [kuntilanak for kuntilanak in kuntilanaks if kuntilanak.health > 0]

    apply_gravity_and_collision(kuntilanak, tiles)

def move_kuntilanak_bullets():
    global kuntilanak_bullets

    for bullet in kuntilanak_bullets:
        bullet.x += bullet.velocity_x
        bullet.y += bullet.velocity_y

        # tabrak player?
        if not player.invicible and player.colliderect(bullet):
            player.health -= 3
            bullet.used = True
            player_hit_sound.play()  
            player.set_invicible()

    # bersihin peluru yang udah kepake / keluar layar
    kuntilanak_bullets = [
        bullet for bullet in kuntilanak_bullets
        if (not bullet.used) and (bullet.x + bullet.width > 0) and (bullet.x < GAME_WIDTH)
    ]

def move_pocong(pocong):
    # ====== GERAK HORIZONTAL (patroli) ======
    if abs(pocong.x + pocong.velocity_x - pocong.start_x) >= pocong.max_range_x:
        pocong.velocity_x *= -1
        if pocong.velocity_x < 0:
            pocong.direction = 'left'
        elif pocong.velocity_x > 0:
            pocong.direction = 'right'
    else:
        pocong.x += pocong.velocity_x

    # ====== CEK LAGI DI ATAS FLYING TILE ATAU BUKAN ======
    on_flying = False
    for tile in flying_tiles:
        # kaki pocong pas di atas tile, dan X-nya overlap sama tile
        if (
            pocong.bottom == tile.top and
            pocong.right > tile.left and
            pocong.left < tile.right
        ):
            on_flying = True
            break

    # ====== RANDOM LOMPAT KALAU LAGI DI FLYING FLOOR ======
    if on_flying and not pocong.jumping:
        if random.random() < 0.1:   # 10% per frame
            pocong.velocity_y = -10
            pocong.jumping = True

    # ====== GRAVITY + COLLISION DENGAN LANTAI & FLYING FLOOR ======
    apply_gravity_and_collision(pocong, tiles + flying_tiles, GRAVITY)

    # ====== TABRAK PLAYER? ======
    if not player.invicible and player.colliderect(pocong):
        player.health -= 5
        player_hit_sound.play()  
        player.set_invicible()

def move_genderuwo(genderuwo):
    speed = abs(GENDERUWO_VELOCITY_X)

    # ===== 1. KEJAR PLAYER DI X =====
    if genderuwo.centerx < player.centerx:
        genderuwo.x += speed
        genderuwo.direction = 'right'
    elif genderuwo.centerx > player.centerx:
        genderuwo.x -= speed
        genderuwo.direction = 'left'

    # ===== 2. LOMPAT TERUS SETIAP KALI NYENTUH TILE =====
    on_any_tile = is_on_tile(genderuwo, tiles + flying_tiles)

    if on_any_tile and not genderuwo.jumping:
        genderuwo.velocity_y = PLAYER_VELOCITY_Y   # sama kaya ustad
        genderuwo.jumping = True

    # ===== 3. GRAVITY + COLLISION =====
    apply_gravity_and_collision(genderuwo, tiles + flying_tiles, GRAVITY)

    # ===== 4. TABRAK PLAYER? =====
    if player.colliderect(genderuwo):
        player.health = 0
        player_hit_sound.play()  

def get_tile_under(entity, tile_list):
    """Balikin tile tempat entity lagi berdiri (kalau ada)."""
    for tile in tile_list:
        if (
            entity.bottom == tile.top and
            entity.right > tile.left and
            entity.left < tile.right
        ):
            return tile
    return None

# =====================
# DRAW
# =====================
def draw():
    window.fill((0, 0, 0))

    # ===== MENU / STORY / GUIDE / PAUSE =====
    if game_state == "home":
        window.blit(home_page, (0, 0))
        return

    if game_state == "story":
        window.blit(story_page, (0, 0))
        return

    if game_state == "guide":
        window.blit(game_guides[current_guide_index], (0, 0))
        return

    if game_state == "paused":
        window.blit(pause_page, (0, 0))
        return

    if game_state == "goodluck":
        window.blit(good_luck_image, (0, 0))
        return

    # ===== GAMEPLAY / GAME OVER / WIN =====
    window.fill((84, 198, 255))
    window.blit(background_image, (0, 0))

    for tile in tiles:
        window.blit(tile.image, tile)
    
    for tile in flying_tiles:
        window.blit(tile.image, tile)

    # masjid
    masjid_rect = get_masjid_rect()
    if masjid_rect:
        window.blit(masjid_image, masjid_rect)

    for kuburan in kuburans:
        window.blit(kuburan.image, kuburan)

    player.update_image()
    window.blit(player.image, player)

    for kuntilanak in kuntilanaks:
        kuntilanak.update_image()
        window.blit(kuntilanak.image, kuntilanak)
        for bullet in kuntilanak.bullets:
            window.blit(bullet.image, bullet)

    for bullet in player.bullets:
        window.blit(bullet.image, bullet)
    
    for bullet in kuntilanak_bullets:
        window.blit(bullet.image, bullet)

    for pocong in pocongs:
        pocong.update_image()
        window.blit(pocong.image, pocong)
    
    for genderuwo in genderuwos:
        genderuwo.update_image()
        window.blit(genderuwo.image, genderuwo)

    for item in items:
        window.blit(item.image, item) 
        
    # health bar
    pygame.draw.rect(window, 'black', (TILE_SIZE, TILE_SIZE, HEALTH_WIDTH, HEALTH_HEIGHT * player.max_health))
    for i in range(player.max_health - player.health, player.max_health):
        window.blit(health_image, (TILE_SIZE, TILE_SIZE + i * HEALTH_HEIGHT, HEALTH_WIDTH, HEALTH_HEIGHT))

    # game over / win pakai gambar
    if game_over:
        window.blit(game_over_page, (0, 0))
        if not hasattr(player, "played_lose_sound"):
            game_lose_sound.play()
            player.played_lose_sound = True

    elif game_won:
        window.blit(game_win_page, (0, 0))
        if not hasattr(player, "played_win_sound"):
            game_win_sound.play()
            player.played_win_sound = True

# =====================
# GAME START
# =====================
player = Player()

create_map()
create_flying_tiles()
spawn_random_kuburan(250)
adjust_flying_tiles_height()
adjust_flying_floor_gap_for_edge_kuburan()
spawn_pocongs_on_flying_tiles()
spawn_genderuwo()

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

        # ====== KEYDOWN: LOGIKA MENU / STATE ======
        if event.type == pygame.KEYDOWN:
            # ---------- HOME ----------
            if game_state == "home":
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    game_state = "story"

            # ---------- STORY ----------
            elif game_state == "story":
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    game_state = "guide"
                    current_guide_index = 0
                    previous_state = "story"
                elif event.key == pygame.K_ESCAPE:
                    game_state = "home"

            # ---------- GUIDE ----------
            elif game_state == "guide":
                if event.key == pygame.K_ESCAPE:
                    # balik ke halaman sebelumnya (story / paused / home)
                    if previous_state == "story":
                        game_state = "story"
                    elif previous_state == "paused":
                        game_state = "paused"
                    elif previous_state == "home":
                        game_state = "home"
                    else:
                        game_state = "playing"
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    # next slide atau selesai
                    if current_guide_index < len(game_guides) - 1:
                        current_guide_index += 1
                    else:
                        # kalau guide datang dari story -> mulai main
                        if previous_state == "story":
                            game_state = "goodluck"
                            bismillah_sound.play()

                            goodluck_start = pygame.time.get_ticks()
                            goodluck_duration = bismillah_sound.get_length() * 1000  # convert ke ms

                        # kalau guide datang dari pause -> balik pause
                        elif previous_state == "paused":
                            game_state = "paused"
                        else:
                            game_state = "playing"

            # ---------- PAUSED ----------
            elif game_state == "paused":
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    # continue game
                    game_state = "playing"
                elif event.key == pygame.K_g:
                    # buka guide dari pause
                    game_state = "guide"
                    current_guide_index = 0
                    previous_state = "paused"
                elif event.key == pygame.K_h or event.key == pygame.K_ESCAPE:
                    # kembali ke home + reset game
                    game_state = "home"
                    reset_game()

            # ---------- PLAYING ----------
            elif game_state == "playing":
                # P untuk pause
                if event.key == pygame.K_p and not game_over and not game_won:
                    game_state = "paused"

                # GAME OVER / WIN controls
                if (game_over or game_won):
                    # ENTER = restart level (mulai ulang)
                    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        pygame.mixer.stop()      # 🔥 STOP semua suara langsung
                        reset_game()
                        game_state = "playing"

                    # ESC = kembali ke home
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.stop()      # 🔥 STOP semua suara langsung
                        reset_game()
                        game_state = "home"

    # ====== KEY PRESSED: LOGIKA MAIN GAME ======
    keys = pygame.key.get_pressed()

    # ==========================
    # UPDATE DUNIA HANYA KALAU SEDANG MAIN
    # ==========================
    if game_state == "playing" and not game_over and not game_won:
        # lompat
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and not player.jumping:
            player.velocity_y = PLAYER_VELOCITY_Y
            player.jumping = True
            jump_sound.play()

        # jalan?
        if keys[pygame.K_LEFT] or keys[pygame.K_a] or keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.walking = True
        else:
            player.walking = False

        # gerak kiri/kanan (scroll map)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_player_x(PLAYER_VELOCITY_X)
            player.direction = 'left'
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_player_x(-PLAYER_VELOCITY_X)
            player.direction = 'right'
        else:
            player.velocity_x = 0

        # nembak
        if keys[pygame.K_SPACE] or keys[pygame.K_x]:
            player.set_shooting()

        # gerak pocong
        for pocong in pocongs:
            move_pocong(pocong)
        pocongs = [p for p in pocongs if p.health > 0]

        # gerak kuntilanak
        for kuntilanak in kuntilanaks:
            move_kuntilanak(kuntilanak, tiles)

        # gerak genderuwo
        for genderuwo in genderuwos:
            move_genderuwo(genderuwo)

        # peluru kuntilanak warisan
        move_kuntilanak_bullets()

        # item jatuh + diambil
        for item in items:
            apply_gravity_and_collision(item, tiles + flying_tiles, GRAVITY)

            if player.colliderect(item):
                item.used = True
                life_energy_sound.play()
                if item.image == life_energy_image:
                    player.health = min(player.health + 2, player.max_health)
                elif item.image == big_life_energy_image:
                    player.health = min(player.health + 8, player.max_health)

        items = [item for item in items if not item.used]

        # kuburan = instakill
        for kuburan in kuburans:
            if player.colliderect(kuburan):
                player.health = 0
                player_hit_sound.play()

        # CEK ZONE MENANG (USTAD SAMPAI MASJID)
        masjid_rect = get_masjid_rect()
        if masjid_rect and player.colliderect(masjid_rect):
            game_won = True

        # gerak player (gravity, peluru, hp <= 0 → game_over)
        move_player(player, tiles)

    # ==========================
    # DRAW SELALU
    # ==========================
    if game_state == "goodluck":
        elapsed = pygame.time.get_ticks() - goodluck_start

        # tunggu sampai audio bismillah selesai
        if elapsed > goodluck_duration:
            game_state = "playing"

        draw()
        pygame.display.update()
        clock.tick(60)
        continue


    draw()
    pygame.display.update()
    clock.tick(60)
