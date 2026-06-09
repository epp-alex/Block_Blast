import pygame
import random
import sys
import os
import json
import traceback

# --- KONFIGURATION & PFADE ---
LOGFILE = "crash_log.txt"
HIGHSCORE_FILE = os.path.join(os.path.expanduser("~"), ".block_blast_highscore")

# --- SPRACHPAKETE ---
# "flag" ist eine Liste von (farbe, rect_anteil) Streifen/Bereichen
# Format: Liste von (RGB, (x%, y%, w%, h%)) – relativ zur Button-Größe
LANG = {
    "Deutsch": {
        "flag_stripes": [          # Schwarz-Rot-Gold, horizontal
            ((20,  20,  20),  (0, 0,     1.0, 0.333)),
            ((220, 30,  30),  (0, 0.333, 1.0, 0.333)),
            ((220, 180, 0),   (0, 0.667, 1.0, 0.333)),
        ],
        "level_up":     "LEVEL UP!",
        "game_over":    "GAME OVER",
        "restart_quit": "R = Neustart   Q = Beenden",
        "pause":        "PAUSE (P)",
        "best":         "BEST",
        "bomb":         "BOMBE",
        "hint":         "Rechtsklick oder R = Drehen",
    },
    "English": {
        "flag_stripes": [          # Union Jack vereinfacht
            ((0,   36, 125),  (0, 0,     1.0, 1.0)),   # Blauer Hintergrund
            ((255, 255, 255), (0, 0.33,  1.0, 0.34)),  # Weißes Kreuz horizontal
            ((255, 255, 255), (0.38, 0,  0.24, 1.0)),  # Weißes Kreuz vertikal
            ((200, 16,  46),  (0, 0.40,  1.0, 0.20)),  # Rotes Kreuz horizontal
            ((200, 16,  46),  (0.43, 0,  0.14, 1.0)),  # Rotes Kreuz vertikal
        ],
        "level_up":     "LEVEL UP!",
        "game_over":    "GAME OVER",
        "restart_quit": "R = Restart   Q = Quit",
        "pause":        "PAUSE (P)",
        "best":         "BEST",
        "bomb":         "BOMB",
        "hint":         "Right-click or R = Rotate",
    },
    "Français": {
        "flag_stripes": [          # Blau-Weiß-Rot, vertikal
            ((0,  35,  149),  (0,     0, 0.333, 1.0)),
            ((255, 255, 255), (0.333, 0, 0.334, 1.0)),
            ((223, 11,  42),  (0.667, 0, 0.333, 1.0)),
        ],
        "level_up":     "LEVEL UP!",
        "game_over":    "FIN DE PARTIE",
        "restart_quit": "R = Recommencer   Q = Quitter",
        "pause":        "PAUSE (P)",
        "best":         "SCORE MAX",
        "bomb":         "BOMBE",
        "hint":         "Clic droit ou R = Pivoter",
    },
    "Español": {
        "flag_stripes": [          # Rot-Gelb-Rot, horizontal (Spanien)
            ((218, 11,  26),  (0, 0,    1.0, 0.25)),
            ((222, 171, 0),   (0, 0.25, 1.0, 0.50)),
            ((218, 11,  26),  (0, 0.75, 1.0, 0.25)),
        ],
        "level_up":     "¡NIVEL UP!",
        "game_over":    "FIN DEL JUEGO",
        "restart_quit": "R = Reiniciar   Q = Salir",
        "pause":        "PAUSA (P)",
        "best":         "RÉCORD",
        "bomb":         "BOMBA",
        "hint":         "Clic derecho o R = Rotar",
    },
    "Italiano": {
        "flag_stripes": [          # Grün-Weiß-Rot, vertikal
            ((0,  146, 70),   (0,     0, 0.333, 1.0)),
            ((255, 255, 255), (0.333, 0, 0.334, 1.0)),
            ((206, 43,  55),  (0.667, 0, 0.333, 1.0)),
        ],
        "level_up":     "LIVELLO UP!",
        "game_over":    "GAME OVER",
        "restart_quit": "R = Riavvia   Q = Esci",
        "pause":        "PAUSA (P)",
        "best":         "MIGLIORE",
        "bomb":         "BOMBA",
        "hint":         "Tasto destro o R = Ruota",
    },
    "Nederlands": {
        "flag_stripes": [          # Rot-Weiß-Blau, horizontal
            ((174, 28,  40),  (0, 0,     1.0, 0.333)),
            ((255, 255, 255), (0, 0.333, 1.0, 0.333)),
            ((33,  70,  139), (0, 0.667, 1.0, 0.333)),
        ],
        "level_up":     "LEVEL UP!",
        "game_over":    "GAME OVER",
        "restart_quit": "R = Herstart   Q = Stoppen",
        "pause":        "PAUZE (P)",
        "best":         "BESTE",
        "bomb":         "BOMM",
        "hint":         "Rechtsklik of R = Draaien",
    },
    "Polski": {
        "flag_stripes": [          # Weiß-Rot, horizontal
            ((255, 255, 255), (0, 0,   1.0, 0.5)),
            ((220, 20,  60),  (0, 0.5, 1.0, 0.5)),
        ],
        "level_up":     "NOWY POZIOM!",
        "game_over":    "KONIEC GRY",
        "restart_quit": "R = Restart   Q = Wyjdź",
        "pause":        "PAUZA (P)",
        "best":         "REKORD",
        "bomb":         "BOMBA",
        "hint":         "Prawy przycisk lub R = Obróć",
    },
    "Русский": {
        "flag_stripes": [          # Weiß-Blau-Rot, horizontal
            ((255, 255, 255), (0, 0,     1.0, 0.333)),
            ((0,   57,  166), (0, 0.333, 1.0, 0.333)),
            ((213, 43,  30),  (0, 0.667, 1.0, 0.333)),
        ],
        "level_up":     "НОВЫЙ УРОВЕНЬ!",
        "game_over":    "ИГРА ОКОНЧЕНА",
        "restart_quit": "R = Сброс   Q = Выход",
        "pause":        "ПАУЗА (P)",
        "best":         "РЕКОРД",
        "bomb":         "БОМБА",
        "hint":         "Пкм или R = Повернуть",
    },
    "Українська": {
        "flag_stripes": [          # Blau-Gelb, horizontal
            ((0,  91,  187), (0, 0,   1.0, 0.5)),
            ((255, 213, 0),  (0, 0.5, 1.0, 0.5)),
        ],
        "level_up":     "НОВИЙ РІВЕНЬ!",
        "game_over":    "ГРА ЗАКІНЧЕНА",
        "restart_quit": "R = Перезапуск   Q = Вихід",
        "pause":        "ПАУЗА (P)",
        "best":         "РЕКОРД",
        "bomb":         "БОМБА",
        "hint":         "ПКМ або R = Повернути",
    },
    "Magyar": {
        "flag_stripes": [          # Rot-Weiß-Grün, horizontal
            ((206, 41,  57),  (0, 0,     1.0, 0.333)),
            ((255, 255, 255), (0, 0.333, 1.0, 0.333)),
            ((71,  112, 80),  (0, 0.667, 1.0, 0.333)),
        ],
        "level_up":     "SZINTLÉPÉS!",
        "game_over":    "JÁTÉK VÉGE",
        "restart_quit": "R = Újraindítás   Q = Kilépés",
        "pause":        "SZÜNET (P)",
        "best":         "REKORD",
        "bomb":         "BOMBA",
        "hint":         "Jobb klikk vagy R = Forgatás",
    },
        "Türkçe": {
        "flag_stripes": [          # Rot mit weißem Balken links (Annäherung für Pygame)
            ((227, 10,  23),  (0, 0,    1.0, 1.0)),   # Roter Grund
            ((255, 255, 255), (0.15, 0.2, 0.15, 0.6)), # Weißer Akzent links
        ],
        "level_up":     "YENİ SEVİYE!",
        "game_over":    "OYUN BİTTİ",
        "restart_quit": "R = Yeniden Başlat   Q = Çıkış",
        "pause":        "PAUSE (P)",
        "best":         "EN YÜKSEK",
        "bomb":         "BOMBA",
        "hint":         "Sağ tık veya R = Döndür",
    },
    "Ελληνικά": {
        "flag_stripes": [          # Griechische Flagge: 9 Streifen + Kreuz oben links
            ((0,   91,  174), (0, 0,     1.0, 1.0)),   # Blauer Grundmantel
            ((255, 255, 255), (0, 0.111, 1.0, 0.111)), # Streifen 2
            ((255, 255, 255), (0, 0.333, 1.0, 0.111)), # Streifen 4
            ((255, 255, 255), (0, 0.555, 1.0, 0.111)), # Streifen 6
            ((255, 255, 255), (0, 0.777, 1.0, 0.111)), # Streifen 8
            # Das Kreuz-Quadrat oben links:
            ((0,   91,  174), (0,    0, 0.45, 0.555)), # Blaues Eckquadrat
            ((255, 255, 255), (0,    0.222, 0.45, 0.111)), # Weißer Balken horizontal
            ((255, 255, 255), (0.18, 0,     0.09, 0.555)), # Weißer Balken vertikal
        ],
        "level_up":     "ΝΕΟ ΕΠΙΠΕΔΟ!",
        "game_over":    "ΤΕΛΟΣ ΠΑΙΧΝΙΔΙΟΥ",
        "restart_quit": "R = Επανεκκίνηση   Q = Έξοδος",
        "pause":        "ΠΑΥΣΗ (P)",
        "best":         "ΡΕΚΟΡ",
        "bomb":         "ΒΟΜΒΑ",
        "hint":         "Δεξί κλικ ή R = Περιστροφή",
    },

}

def draw_flag(surf, lang_key, x, y, w, h):
    """Zeichnet eine vereinfachte Flagge als pygame-Rechtecke."""
    stripes = LANG[lang_key].get("flag_stripes", [])
    # Hintergrund
    clip = pygame.Rect(x, y, w, h)
    for color, (rx, ry, rw, rh) in stripes:
        r = pygame.Rect(
            x + int(rx * w),
            y + int(ry * h),
            max(1, int(rw * w)),
            max(1, int(rh * h)),
        )
        r.clip(clip)  # nicht außerhalb zeichnen
        pygame.draw.rect(surf, color, r)

# --- EINSTELLUNGEN (Sprache) ---
def _settings_path():
    """Plattformgerechter Pfad zur settings.json."""
    if sys.platform == "win32":
        base = os.environ.get("APPDATA", os.path.expanduser("~"))
    elif sys.platform == "darwin":
        base = os.path.join(os.path.expanduser("~"), "Library", "Application Support")
    else:
        base = os.environ.get("XDG_CONFIG_HOME", os.path.join(os.path.expanduser("~"), ".config"))
    folder = os.path.join(base, "BlockBlast")
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, "settings.json")

def load_lang_setting():
    """Lädt gespeicherte Sprache, Default: Deutsch."""
    try:
        path = _settings_path()
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if data.get("lang") in LANG:
                return data["lang"]
    except Exception:
        pass
    return "Deutsch"

def save_lang_setting(lang):
    """Speichert gewählte Sprache."""
    try:
        path = _settings_path()
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"lang": lang}, f, indent=2)
    except Exception:
        pass

# Aktive Sprache laden
current_lang = load_lang_setting()

def T(key):
    """Übersetzungshelfer – gibt Text in aktueller Sprache zurück."""
    return LANG[current_lang].get(key, LANG["Deutsch"][key])

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def load_highscore():
    try:
        if os.path.exists(HIGHSCORE_FILE):
            with open(HIGHSCORE_FILE, "r") as f:
                return int(f.read())
    except: return 0
    return 0

def save_highscore(s):
    try:
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(s))
    except: pass

# --- INITIALISIERUNG ---
pygame.init()
mixer_available = True
try:
    pygame.mixer.init()
except:
    mixer_available = False

# --- SOUND MANAGEMENT ---
global_volume = 0.20
all_sounds = []

def try_load_sound(path):
    if not mixer_available: return None
    try:
        snd = pygame.mixer.Sound(path)
        snd.set_volume(global_volume)
        all_sounds.append(snd)
        return snd
    except: return None

def change_volume(delta):
    global global_volume
    global_volume = max(0.0, min(1.0, global_volume + delta))
    for s in all_sounds:
        s.set_volume(global_volume)

# --- DISPLAY SETUP ---
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h

if sys.platform == "win32":
    # Windows: maximiertes Fenster ohne Titelleiste
    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME
    )
elif sys.platform == "darwin":
    # macOS: normales Fenster maximiert
    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE
    )
    pygame.display.toggle_fullscreen()
else:
    # Linux: NOFRAME mit Desktop-Auflösung – zuverlässigster Weg
    # FULLSCREEN schlägt auf vielen Linux-WMs fehl
    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME
    )

pygame.display.set_caption("Block Blast: Master Edition")

# --- KONSTANTEN ---
GRID_SIZE  = 8
# Auf Hochformat (3:4): Grid darf max 55% der Bildschirmhöhe belegen
_max_cell_by_h = int(SCREEN_HEIGHT * 0.55 / GRID_SIZE)
_max_cell_by_w = int(SCREEN_WIDTH  * 0.85 / GRID_SIZE)
CELL_SIZE  = min(55, _max_cell_by_h, _max_cell_by_w)
GRID_OFFSET_X = (SCREEN_WIDTH  - GRID_SIZE * CELL_SIZE) // 2
GRID_OFFSET_Y = max(55, (SCREEN_HEIGHT - GRID_SIZE * CELL_SIZE) // 2 - 80)

WHITE, GRAY, BLACK = (240, 240, 240), (45, 45, 50), (5, 5, 10)
GOLD, RED, YELLOW = (255, 215, 0), (230, 40, 40), (255, 255, 0)
BOMB_COLOR = (255, 80, 0)
LVL_COLORS = [(0, 255, 200), (0, 150, 255), (200, 100, 255), (255, 100, 100), (255, 200, 0)]
COLORS = [(63, 131, 248), (255, 95, 95), (46, 204, 113), (241, 196, 15), (155, 89, 182), (230, 126, 34)]

# --- KLASSEN ---
class BackgroundStar:
    def __init__(self):
        self.x, self.y = random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)
        self.size = random.uniform(0.5, 2.0)
        self.speed = random.uniform(0.05, 0.2)
        self.brightness = random.randint(50, 150)
    def update(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT: self.y = 0; self.x = random.randint(0, SCREEN_WIDTH)
    def draw(self, surf):
        pygame.draw.circle(surf, (self.brightness, self.brightness, self.brightness), (int(self.x), int(self.y)), int(self.size))

class Lightning:
    def __init__(self, color):
        self.points, self.alpha, self.color = [], 255, color
        x, y = random.randint(0, SCREEN_WIDTH), 0
        self.points = [(x, y)]
        while y < SCREEN_HEIGHT:
            y += random.randint(20, 60)
            x += random.randint(-50, 50)
            self.points.append((x, y))
    def update(self):
        self.alpha -= 15
        return self.alpha > 0
    def draw(self, surf):
        if len(self.points) > 1:
            s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            pygame.draw.lines(s, (*self.color, self.alpha), False, self.points, random.randint(2, 5))
            surf.blit(s, (0,0))

class Particle:
    def __init__(self, x, y, color, speed_mult=1.0):
        self.x, self.y, self.color = x, y, color
        self.vx, self.vy = random.uniform(-6, 6)*speed_mult, random.uniform(-6, 6)*speed_mult
        self.lifetime = 255
    def update(self, dt):
        self.x += self.vx * dt; self.y += self.vy * dt; self.lifetime -= 15 * dt
    def draw(self, surf):
        if self.lifetime > 0:
            s = pygame.Surface((5, 5), pygame.SRCALPHA)
            s.fill((*self.color[:3], int(max(0, self.lifetime))))
            surf.blit(s, (self.x, self.y))

class Block:
    def __init__(self, shape, color, pos):
        self.shape, self.color = shape, color
        self.pos = pygame.Vector2(pos)
        self.start_pos = pygame.Vector2(pos)
        self.dragging = False
        self.update_size()
    
    def update_size(self):
        """Aktualisiert Breite und Höhe basierend auf aktueller Form"""
        self.width = len(self.shape[0]) * CELL_SIZE
        self.height = len(self.shape) * CELL_SIZE
    
    def rotate(self):
        """Rotiert den Block um 90 Grad im Uhrzeigersinn"""
        self.shape = [list(row) for row in zip(*self.shape[::-1])]
        self.update_size()
    
    def draw(self, surf, scale=1.0, alpha=255):
        s_size = CELL_SIZE * scale
        for r, row in enumerate(self.shape):
            for c, val in enumerate(row):
                if val:
                    b_surf = pygame.Surface((max(1, int(s_size-3)), max(1, int(s_size-3))), pygame.SRCALPHA)
                    pygame.draw.rect(b_surf, (*self.color[:3], alpha), (0,0, s_size-3, s_size-3), border_radius=int(6*scale))
                    surf.blit(b_surf, (self.pos.x + c*s_size, self.pos.y + r*s_size))

# --- LOGIK-FUNKTIONEN ---
def rotate_shape(shape):
    return [list(row) for row in zip(*shape[::-1])]

def generate_blocks():
    # Jeder Block bekommt einen festen Slot der breit/hoch genug für den
    # größten möglichen Block ist (5×CELL_SIZE). Kein Überlappen möglich.
    slot_w   = 5 * CELL_SIZE + 20   # Breite pro Slot
    slot_h   = 5 * CELL_SIZE + 20   # Höhe pro Slot
    total_w  = 3 * slot_w
    start_x  = (SCREEN_WIDTH - total_w) // 2
    pos_y    = GRID_OFFSET_Y + GRID_SIZE * CELL_SIZE + 20

    shapes = [
        # --- EINER & QUADRATE ---
        [[1]],                              # 1x1 Einzelblock
        [[1,1],[1,1]],                      # 2x2 Quadrat
        [[1,1,1],[1,1,1],[1,1,1]],          # 3x3 Riesen-Quadrat

        # --- GERADE STÄBE ---
        [[1,1]],                            # 2er Stab
        [[1,1,1]],                          # 3er Stab
        [[1,1,1,1]],                        # 4er Stab
        [[1,1,1,1,1]],                      # 5er Riesen-Stab

        # --- L-SHAPES (WINKEL) ---
        [[1,0],[1,1]],                      # Kleiner 2x2 Winkel
        [[1,0,0],[1,0,0],[1,1,1]],          # Großer 3x3 L-Stein
        [[1,1,1],[1,0,0],[1,0,0]],          # Großer 3x3 L-Stein (andere Richtung)

        # --- STUFEN / Z-STEINE ---
        [[1,1,0],[0,1,1]],                  # Stufe rechts
        [[0,1,1],[1,1,0]],                  # Stufe links

        # --- T-SHAPES & JAMPERS ---
        [[1,1,1],[0,1,0]],                  # Klassischer T-Stein
        [[1,0,1],[1,1,1]]                   # U-Form / Becher
    ]

    blocks = []
    for i in range(3):
        s = random.choice(shapes)
        for _ in range(random.randint(0, 3)):
            s = rotate_shape(s)
        # Block zentriert im Slot platzieren
        block_w = len(s[0]) * CELL_SIZE
        block_h = len(s)    * CELL_SIZE
        slot_x  = start_x + i * slot_w
        bx      = slot_x + (slot_w - block_w) // 2
        by      = pos_y  + (slot_h - block_h) // 2
        b       = Block(s, random.choice(COLORS), (bx, by))
        b.slot_x    = slot_x   # merken für Reset nach Loslassen
        b.slot_w    = slot_w
        b.slot_pos_y = pos_y
        b.slot_h    = slot_h
        blocks.append(b)
    return blocks

def can_fit(shape, r_start, c_start):
    if r_start < 0 or r_start + len(shape) > GRID_SIZE or c_start < 0 or c_start + len(shape[0]) > GRID_SIZE: return False
    for r in range(len(shape)):
        for c in range(len(shape[r])):
            if shape[r][c] and grid[r_start+r][c_start+c] != 0: return False
    return True

def any_block_placeable(blocks):
    """Prüft ob irgendein Block (in irgendeiner Rotation) platzierbar ist"""
    for b in blocks:
        # Prüfe alle 4 möglichen Rotationen
        original_shape = [row[:] for row in b.shape]  # Kopie der Form
        
        for rotation in range(4):
            h, w = len(b.shape), len(b.shape[0])
            for r in range(GRID_SIZE - h + 1):
                for c in range(GRID_SIZE - w + 1):
                    if can_fit(b.shape, r, c):
                        # Stelle Original-Form wieder her
                        b.shape = original_shape
                        b.update_size()
                        return True
            
            # Rotiere für nächsten Versuch
            b.rotate()
        
        # Stelle Original-Form wieder her nach allen Rotationen
        b.shape = original_shape
        b.update_size()
    
    return False

def trigger_game_over_logic():
    global game_over, bombs_available, grid, particles, shake_intensity, slow_mo_timer, highscore, score, bomb_flash
    if bombs_available > 0:
        bombs_available -= 1
        shake_intensity, slow_mo_timer, bomb_flash = 70, 50, 255
        if bomb_sound: bomb_sound.play()
        for r in range(1, 7):
            for c in range(1, 7):
                if grid[r][c] != 0:
                    for _ in range(8): particles.append(Particle(GRID_OFFSET_X + c*CELL_SIZE + 27, GRID_OFFSET_Y + r*CELL_SIZE + 27, grid[r][c], 1.5))
                    grid[r][c] = 0
        if any_block_placeable(blocks_in_hand): 
            return 
        elif bombs_available > 0: 
            trigger_game_over_logic() 
            return

    if not game_over:
        game_over = True
        if score > highscore: highscore = score; save_highscore(score)
        if levelup_sound: levelup_sound.play()

# --- VARIABLEN ---
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
score, highscore = 0, load_highscore()
combo, current_level, bombs_available = 1, 1, 1
game_over, paused = False, False
particles, lightnings = [], []
bg_stars = [BackgroundStar() for _ in range(100)]
shake_intensity, slow_mo_timer, bomb_flash, lvl_up_timer = 0, 0, 0, 0
blocks_in_hand = generate_blocks()
active_block = None

# Schriftarten
try:
    font_huge = pygame.font.SysFont("Verdana", 55, bold=True)
    font_main = pygame.font.SysFont("Verdana", 36, bold=True)
    font_small = pygame.font.SysFont("Verdana", 24, bold=True)
    font_tiny = pygame.font.SysFont("Verdana", 18, bold=True)
except:
    font_huge = pygame.font.Font(None, 55)
    font_main = pygame.font.Font(None, 36)
    font_small = pygame.font.Font(None, 24)
    font_tiny = pygame.font.Font(None, 18)

# Sounds laden
clear_sound = try_load_sound(resource_path("clear.wav"))
levelup_sound = try_load_sound(resource_path("levelup.wav"))
bomb_sound = try_load_sound(resource_path("explosion.wav"))

clock = pygame.time.Clock()

# Sprach-Buttons: dynamisch, 2-zeilig, passt auf jeden Bildschirm
_lang_keys   = list(LANG.keys())
_per_row     = (_lang_keys.__len__() + 1) // 2
lang_btn_h   = 36
lang_btn_gap = 6
lang_btn_w   = min(180, (SCREEN_WIDTH - 20) // _per_row - lang_btn_gap)
_lang_rows   = (_lang_keys.__len__() + _per_row - 1) // _per_row
lang_btn_top = 10
lang_btn_area_h = lang_btn_top + _lang_rows * (lang_btn_h + 4)  # Gesamthöhe der Button-Zeilen

# Alle anderen UI-Elemente beginnen UNTER den Sprach-Buttons
UI_TOP = lang_btn_area_h + 12   # 12px Abstand nach den Buttons

lang_buttons = []
for i, lk in enumerate(_lang_keys):
    row = i // _per_row
    col = i %  _per_row
    bx  = col * (lang_btn_w + lang_btn_gap)
    by  = lang_btn_top + row * (lang_btn_h + 4)
    lang_buttons.append((lk, pygame.Rect(bx, by, lang_btn_w, lang_btn_h)))

# Buttons – alle relativ zu UI_TOP
exit_btn     = pygame.Rect(30, UI_TOP, 60, 60)
bomb_btn     = pygame.Rect(SCREEN_WIDTH - 200, SCREEN_HEIGHT // 2 - 50, 150, 100)
vol_up_btn   = pygame.Rect(SCREEN_WIDTH - 80,  SCREEN_HEIGHT - 180, 50, 50)
vol_down_btn = pygame.Rect(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 180, 50, 50)

# --- HAUPTSCHLEIFE ---
try:
    while True:
        dt = 0.25 if slow_mo_timer > 0 else 1.0
        if slow_mo_timer > 0: slow_mo_timer -= 1
        current_lvl_color = LVL_COLORS[(current_level-1) % len(LVL_COLORS)]
        
        sx = random.randint(-shake_intensity, shake_intensity)
        sy = random.randint(-shake_intensity, shake_intensity)
        if shake_intensity > 0: shake_intensity -= 1

        screen.fill(BLACK)
        for star in bg_stars: star.update(); star.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if score > highscore: save_highscore(score)
                pygame.quit(); sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p: paused = not paused
                if game_over and event.key == pygame.K_r:
                    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
                    score, combo, current_level, bombs_available = 0, 1, 1, 1
                    blocks_in_hand = generate_blocks(); game_over = False
                    particles.clear()
                    lightnings.clear()
                if event.key in (pygame.K_ESCAPE, pygame.K_q): pygame.quit(); sys.exit()
                
                # Rotation mit R-Taste während des Ziehens
                if event.key == pygame.K_r and active_block and active_block.dragging:
                    active_block.rotate()

            if not game_over and not paused:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Sprach-Buttons
                    for lk, lr in lang_buttons:
                        if lr.collidepoint(event.pos):
                            current_lang = lk
                            save_lang_setting(current_lang)
                            break
                    if exit_btn.collidepoint(event.pos): pygame.quit(); sys.exit()
                    if vol_up_btn.collidepoint(event.pos): change_volume(0.1)
                    if vol_down_btn.collidepoint(event.pos): change_volume(-0.1)
                    if bomb_btn.collidepoint(event.pos) and bombs_available > 0:
                        bombs_available -= 1; shake_intensity, bomb_flash = 50, 255
                        if bomb_sound: bomb_sound.play()
                        for r in range(2, 6):
                            for c in range(2, 6):
                                if grid[r][c]: grid[r][c] = 0
                        if not any_block_placeable(blocks_in_hand): trigger_game_over_logic()

                    # Linke Maustaste: Block aufnehmen
                    if event.button == 1:
                        for b in blocks_in_hand:
                            if pygame.Rect(b.pos.x, b.pos.y, b.width, b.height).collidepoint(event.pos):
                                active_block = b; b.dragging = True; break
                    
                    # Rechte Maustaste: Block rotieren
                    if event.button == 3 and active_block and active_block.dragging:
                        active_block.rotate()

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and active_block:
                    gx, gy = round((active_block.pos.x - GRID_OFFSET_X) / CELL_SIZE), round((active_block.pos.y - GRID_OFFSET_Y) / CELL_SIZE)
                    if can_fit(active_block.shape, gy, gx):
                        for r in range(len(active_block.shape)):
                            for c in range(len(active_block.shape[0])):
                                if active_block.shape[r][c]: grid[gy+r][gx+c] = active_block.color
                        blocks_in_hand.remove(active_block)
                        
                        rows = [r for r in range(GRID_SIZE) if all(grid[r][c] != 0 for c in range(GRID_SIZE))]
                        cols = [c for c in range(GRID_SIZE) if all(grid[r][c] != 0 for r in range(GRID_SIZE))]
                        if rows or cols:
                            for r in rows:
                                for c in range(GRID_SIZE): 
                                    particles.append(Particle(GRID_OFFSET_X + c*CELL_SIZE + 27, GRID_OFFSET_Y + r*CELL_SIZE + 27, grid[r][c]))
                                    grid[r][c] = 0
                            for c in cols:
                                for r in range(GRID_SIZE): 
                                    if grid[r][c]:
                                        particles.append(Particle(GRID_OFFSET_X + c*CELL_SIZE + 27, GRID_OFFSET_Y + r*CELL_SIZE + 27, grid[r][c]))
                                        grid[r][c] = 0
                            score += (len(rows) + len(cols)) * 100 * combo
                            combo += 1; shake_intensity = 20
                            if score >= current_level * 1500:
                                current_level += 1; bombs_available += 1; lvl_up_timer = 120
                                if levelup_sound: levelup_sound.play()
                            if clear_sound: clear_sound.play()
                        else: combo = 1
                        
                        if not blocks_in_hand: blocks_in_hand = generate_blocks()
                        if not any_block_placeable(blocks_in_hand): 
                            trigger_game_over_logic()
                    else:
                        # Block zurück in Slot-Mitte
                        block_w = active_block.width
                        block_h = active_block.height
                        bx = active_block.slot_x + (active_block.slot_w - block_w) // 2
                        by = active_block.slot_pos_y + (active_block.slot_h - block_h) // 2
                        active_block.pos = pygame.Vector2(bx, by)
                        active_block.start_pos = pygame.Vector2(bx, by)
                    active_block.dragging = False; active_block = None

        if active_block and active_block.dragging:
            mx, my = pygame.mouse.get_pos()
            active_block.pos = pygame.Vector2(mx - active_block.width/2, my - active_block.height/2)

        # Spielfeld zeichnen
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                rect = (GRID_OFFSET_X + c*CELL_SIZE + sx, GRID_OFFSET_Y + r*CELL_SIZE + sy, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, grid[r][c] if grid[r][c] else GRAY, rect, 0 if grid[r][c] else 1, border_radius=4)

        # Effekte: Level Up Blitze
        if lvl_up_timer > 0:
            lvl_up_timer -= 1
            if random.random() < 0.2: lightnings.append(Lightning(GOLD))
            msg = font_huge.render(T("level_up"), True, GOLD)
            screen.blit(msg, (SCREEN_WIDTH//2 - msg.get_width()//2, SCREEN_HEIGHT//2 - 100))

        for l in lightnings[:]:
            if not l.update(): lightnings.remove(l)
            else: l.draw(screen)

        for p in particles[:]:
            p.update(dt); p.draw(screen)
            if p.lifetime <= 0: particles.remove(p)

        for b in blocks_in_hand: b.draw(screen, scale=0.75 if not b.dragging else 1.0)

        # UI
        screen.blit(font_huge.render(f"{score}", True, WHITE), (SCREEN_WIDTH//2 - 40, UI_TOP + 5))
        screen.blit(font_main.render(f"LVL {current_level}", True, current_lvl_color), (50, UI_TOP + 70))
        screen.blit(font_small.render(f"{T('best')}: {highscore}", True, GOLD), (SCREEN_WIDTH - 250, UI_TOP + 10))
        
        # Hinweis zum Rotieren – direkt unter den Vorschau-Blöcken
        hint_text = font_tiny.render(T("hint"), True, (150, 150, 150))
        hint_y    = GRID_OFFSET_Y + GRID_SIZE * CELL_SIZE + 50
        screen.blit(hint_text, (SCREEN_WIDTH//2 - hint_text.get_width()//2, hint_y))
        
        # Bomb & Vol UI
        pygame.draw.rect(screen, BOMB_COLOR if bombs_available > 0 else (50,50,50), bomb_btn, border_radius=15)
        screen.blit(font_small.render(f"{T('bomb')}: {bombs_available}", True, WHITE), (bomb_btn.x+10, bomb_btn.y+35))
        
        # Volume Regler
        pygame.draw.rect(screen, GRAY, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 120, 120, 10))
        pygame.draw.rect(screen, GOLD, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 120, int(120 * global_volume), 10))
        pygame.draw.rect(screen, (70,70,70), vol_up_btn, border_radius=10)
        pygame.draw.rect(screen, (70,70,70), vol_down_btn, border_radius=10)
        screen.blit(font_small.render("+", True, WHITE), (vol_up_btn.x+15, vol_up_btn.y+10))
        screen.blit(font_small.render("-", True, WHITE), (vol_down_btn.x+20, vol_down_btn.y+10))

        pygame.draw.rect(screen, RED, exit_btn, border_radius=50)
        screen.blit(font_small.render("X", True, WHITE), (exit_btn.x+22, exit_btn.y+15))
        
        # Bomb Blitz Effekt
        if bomb_flash > 0:
            f_s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            f_s.fill(WHITE)
            f_s.set_alpha(bomb_flash)
            screen.blit(f_s, (0,0))
            bomb_flash -= 20

        if paused: 
            s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            s.fill((0,0,0,150))
            screen.blit(s, (0,0))
            screen.blit(font_huge.render(T("pause"), True, YELLOW), (SCREEN_WIDTH//2-140, SCREEN_HEIGHT//2))

        if game_over:
            s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            s.fill((0,0,0,180))
            screen.blit(s, (0,0))
            screen.blit(font_huge.render(T("game_over"), True, RED), (SCREEN_WIDTH//2-160, SCREEN_HEIGHT//2-50))
            screen.blit(font_small.render(T("restart_quit"), True, WHITE), (SCREEN_WIDTH//2-150, SCREEN_HEIGHT//2+20))

        # Sprach-Buttons zeichnen
        for lk, lr in lang_buttons:
            is_active = (lk == current_lang)
            btn_color  = (80, 80, 120) if not is_active else (120, 100, 200)
            border_col = GOLD if is_active else (100, 100, 100)
            pygame.draw.rect(screen, btn_color, lr, border_radius=8)
            pygame.draw.rect(screen, border_col, lr, 2, border_radius=8)

            pad       = 7                          # Innenabstand links/rechts
            flag_w    = 32
            flag_h    = int(lr.height * 0.55)
            flag_x    = lr.x + pad
            flag_y    = lr.y + (lr.height - flag_h) // 2
            draw_flag(screen, lk, flag_x, flag_y, flag_w, flag_h)
            pygame.draw.rect(screen, (180, 180, 180),
                             (flag_x, flag_y, flag_w, flag_h), 1)

            lbl = font_tiny.render(lk, True, WHITE)
            text_x = flag_x + flag_w + 7
            text_y = lr.y + (lr.height - lbl.get_height()) // 2
            # Nur zeichnen wenn Text in den Button passt
            screen.set_clip(lr)
            screen.blit(lbl, (text_x, text_y))
            screen.set_clip(None)

        pygame.display.flip(); clock.tick(60)

except Exception:
    with open(LOGFILE, "a") as f: f.write(traceback.format_exc())
finally:
    pygame.quit(); sys.exit()