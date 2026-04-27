# config.py

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
TITLE = "Snake"

CELL_SIZE = 20
COLS = WINDOW_WIDTH // CELL_SIZE
ROWS = WINDOW_HEIGHT // CELL_SIZE

FOOD_PER_LEVEL = 5
INITIAL_SPEED = 8
SPEED_INCREMENT = 2

FOOD_TIMEOUT_MS = 5000
POWERUP_FIELD_LIFETIME = 7000
POWERUP_EFFECT_MS = 5000

OBSTACLE_START_LEVEL = 2
MIN_OBSTACLES = 3
MAX_OBSTACLES = 20

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (120, 120, 120)
DARK_GRAY = (40, 40, 40)
LIGHT_GRAY = (180, 180, 180)
BG_COLOR = (15, 15, 25)

GREEN = (0, 200, 0)
DARK_GREEN = (0, 120, 0)
RED = (220, 50, 50)
YELLOW = (230, 230, 0)
CYAN = (0, 220, 220)
DARK_RED = (120, 0, 0)
ORANGE = (230, 120, 0)
BLUE = (50, 100, 220)
PURPLE = (180, 80, 220)

FOOD_TYPES = [
    {"name": "normal", "color": RED, "points": 10, "disappears": False},
    {"name": "bonus", "color": YELLOW, "points": 20, "disappears": True},
    {"name": "super", "color": CYAN, "points": 30, "disappears": True},
    {"name": "poison", "color": PURPLE, "points": 0, "disappears": False},
]

POWERUP_TYPES = ["speed_boost", "slow_motion", "shield"]

POWERUP_COLORS = {
    "speed_boost": ORANGE,
    "slow_motion": BLUE,
    "shield": PURPLE,
}

POWERUP_LABELS = {
    "speed_boost": "F",
    "slow_motion": "S",
    "shield": "P",
}

DB_CONFIG = {
    "host": "localhost",
    "database": "snake_db",
    "user": "postgres",
    "password": "Killu7755",
    "port": 5432,
}