# game.py — Core snake game logic

import pygame
import random
from config import (
    CELL_SIZE, COLS, ROWS, FOOD_PER_LEVEL, INITIAL_SPEED, SPEED_INCREMENT,
    FOOD_TIMEOUT_MS, POWERUP_FIELD_LIFETIME, POWERUP_EFFECT_MS,
    FOOD_TYPES, POWERUP_TYPES, POWERUP_COLORS, POWERUP_LABELS,
    OBSTACLE_START_LEVEL, MIN_OBSTACLES, MAX_OBSTACLES,
    BLACK, WHITE, GRAY, DARK_GRAY, LIGHT_GRAY, BG_COLOR,
    GREEN, DARK_GREEN, RED, YELLOW, CYAN, DARK_RED, ORANGE, BLUE, PURPLE,
)


# ─── Direction helpers ────────────────────────────────────────────────────────
UP    = ( 0, -1)
DOWN  = ( 0,  1)
LEFT  = (-1,  0)
RIGHT = ( 1,  0)
OPPOSITES = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}


def cell_rect(col: int, row: int) -> pygame.Rect:
    return pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)


# ─── Food ────────────────────────────────────────────────────────────────────
class Food:
    def __init__(self, pos: tuple, ftype: dict, spawn_time: int):
        self.pos = pos
        self.ftype = ftype          # dict from FOOD_TYPES
        self.spawn_time = spawn_time

    def is_expired(self, now: int) -> bool:
        if not self.ftype["disappears"]:
            return False
        return (now - self.spawn_time) > FOOD_TIMEOUT_MS

    def draw(self, surface: pygame.Surface, now: int):
        r = cell_rect(*self.pos)
        pygame.draw.rect(surface, self.ftype["color"], r)
        if self.ftype["disappears"]:
            remaining = FOOD_TIMEOUT_MS - (now - self.spawn_time)
            frac = max(0, remaining / FOOD_TIMEOUT_MS)
            inner = r.inflate(-4, -4)
            pygame.draw.rect(surface, WHITE, inner, 1)
            bar_w = int(inner.width * frac)
            pygame.draw.rect(surface, WHITE, (inner.x, inner.bottom - 3, bar_w, 3))


# ─── Power-up ────────────────────────────────────────────────────────────────
class PowerUp:
    def __init__(self, pos: tuple, ptype: str, spawn_time: int):
        self.pos = pos
        self.ptype = ptype
        self.spawn_time = spawn_time

    def is_expired(self, now: int) -> bool:
        return (now - self.spawn_time) > POWERUP_FIELD_LIFETIME

    def draw(self, surface: pygame.Surface, font: pygame.font.Font):
        r = cell_rect(*self.pos)
        pygame.draw.rect(surface, POWERUP_COLORS[self.ptype], r)
        label = font.render(POWERUP_LABELS[self.ptype], True, WHITE)
        lx = r.x + (CELL_SIZE - label.get_width()) // 2
        ly = r.y + (CELL_SIZE - label.get_height()) // 2
        surface.blit(label, (lx, ly))


# ─── Snake ───────────────────────────────────────────────────────────────────
class Snake:
    def __init__(self, color):
        cx, cy = COLS // 2, ROWS // 2
        self.body = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.direction = RIGHT
        self.next_dir = RIGHT
        self.color = color
        self.grew = False

    def set_direction(self, new_dir):
        if new_dir != OPPOSITES.get(self.direction):
            self.next_dir = new_dir

    def move(self):
        self.direction = self.next_dir
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body.insert(0, new_head)
        if not self.grew:
            self.body.pop()
        self.grew = False

    def grow(self, n: int = 1):
        for _ in range(n):
            self.grew = True

    def shrink(self, n: int = 2) -> bool:
        """Remove n segments from tail. Returns False if snake too short."""
        for _ in range(n):
            if len(self.body) > 1:
                self.body.pop()
            else:
                return False
        return len(self.body) > 1

    @property
    def head(self):
        return self.body[0]

    def self_collision(self) -> bool:
        return self.head in self.body[1:]

    def wall_collision(self) -> bool:
        x, y = self.head
        return x < 0 or x >= COLS or y < 0 or y >= ROWS

    def draw(self, surface: pygame.Surface):
        for i, seg in enumerate(self.body):
            r = cell_rect(*seg)
            color = self.color if i > 0 else tuple(min(255, c + 60) for c in self.color)
            pygame.draw.rect(surface, color, r)
            pygame.draw.rect(surface, DARK_GREEN, r, 1)


# ─── GameSession ─────────────────────────────────────────────────────────────
class GameSession:
    """Holds all runtime state for one play-through."""

    def __init__(self, username: str, personal_best: int,
                 snake_color, grid_overlay: bool):
        self.username = username
        self.personal_best = personal_best
        self.grid_overlay = grid_overlay

        self.snake = Snake(snake_color)
        self.score = 0
        self.level = 1
        self.food_eaten_this_level = 0
        self.speed = INITIAL_SPEED
        self.obstacles: set[tuple] = set()

        self.foods: list[Food] = []
        self.powerup: PowerUp | None = None

        # Active effects
        self.shield_active = False
        self.speed_effect_end = 0    # ticks; 0 = no effect
        self.speed_effect_type = None  # "speed_boost" | "slow_motion"
        self.base_speed = INITIAL_SPEED

        self._spawn_food()
        self._small_font = None   # set by Game after pygame.init

    # ── Occupied cells ────────────────────────────────────────────────────────
    def _occupied(self) -> set[tuple]:
        occ = set(self.snake.body) | self.obstacles
        occ.update(f.pos for f in self.foods)
        if self.powerup:
            occ.add(self.powerup.pos)
        return occ

    def _random_free_cell(self) -> tuple | None:
        occ = self._occupied()
        free = [(c, r) for c in range(COLS) for r in range(ROWS) if (c, r) not in occ]
        return random.choice(free) if free else None

    # ── Food ─────────────────────────────────────────────────────────────────
    def _spawn_food(self):
        now = pygame.time.get_ticks()
        pos = self._random_free_cell()
        if pos is None:
            return
        weights = [4, 2, 1, 1]  # normal, bonus, super, poison
        ftype = random.choices(FOOD_TYPES, weights=weights, k=1)[0]
        self.foods.append(Food(pos, ftype, now))

    # ── Power-up ─────────────────────────────────────────────────────────────
    def _maybe_spawn_powerup(self):
        if self.powerup is not None:
            return
        if random.random() < 0.3:   # 30 % chance each food eaten
            now = pygame.time.get_ticks()
            pos = self._random_free_cell()
            if pos is None:
                return
            ptype = random.choice(POWERUP_TYPES)
            self.powerup = PowerUp(pos, ptype, now)

    # ── Obstacles ────────────────────────────────────────────────────────────
    def _place_obstacles(self):
        if self.level < OBSTACLE_START_LEVEL:
            return
        count = min(MIN_OBSTACLES + (self.level - OBSTACLE_START_LEVEL) * 2,
                    MAX_OBSTACLES)
        head = self.snake.head
        for _ in range(count * 10):   # limited attempts
            if len(self.obstacles) >= count:
                break
            pos = self._random_free_cell()
            if pos is None:
                break
            # Don't place adjacent to snake head
            if abs(pos[0] - head[0]) <= 2 and abs(pos[1] - head[1]) <= 2:
                continue
            self.obstacles.add(pos)

    # ── Level up ─────────────────────────────────────────────────────────────
    def _level_up(self):
        self.level += 1
        self.food_eaten_this_level = 0
        self.base_speed += SPEED_INCREMENT
        self.speed = self.base_speed
        self._place_obstacles()

    # ── Update ────────────────────────────────────────────────────────────────
    def update(self) -> str:
        """Move snake, check collisions, handle eating. Returns 'ok' or 'dead'."""
        now = pygame.time.get_ticks()

        # Expire timed speed effect
        if self.speed_effect_end and now >= self.speed_effect_end:
            self.speed = self.base_speed
            self.speed_effect_end = 0
            self.speed_effect_type = None

        self.snake.move()

        # Wall collision
        if self.snake.wall_collision():
            if self.shield_active:
                self.shield_active = False
                # Wrap around (teleport to other side)
                x, y = self.snake.head
                x = x % COLS
                y = y % ROWS
                self.snake.body[0] = (x, y)
            else:
                return "dead"

        # Obstacle collision
        if self.snake.head in self.obstacles:
            if self.shield_active:
                self.shield_active = False
            else:
                return "dead"

        # Self collision
        if self.snake.self_collision():
            return "dead"

        # Expire disappearing food
        expired = [f for f in self.foods if f.is_expired(now)]
        for f in expired:
            self.foods.remove(f)

        # Expire powerup on field
        if self.powerup and self.powerup.is_expired(now):
            self.powerup = None

        # Eat food?
        for food in list(self.foods):
            if self.snake.head == food.pos:
                self.foods.remove(food)
                if food.ftype["name"] == "poison":
                    ok = self.snake.shrink(2)
                    if not ok:
                        return "dead"
                else:
                    self.snake.grow()
                    self.score += food.ftype["points"]
                    self.food_eaten_this_level += 1
                    if self.food_eaten_this_level >= FOOD_PER_LEVEL:
                        self._level_up()
                self._spawn_food()
                self._maybe_spawn_powerup()
                break

        # Collect powerup?
        if self.powerup and self.snake.head == self.powerup.pos:
            self._apply_powerup(self.powerup.ptype, now)
            self.powerup = None

        # Always maintain at least one food item
        if not self.foods:
            self._spawn_food()

        return "ok"

    def _apply_powerup(self, ptype: str, now: int):
        if ptype == "speed_boost":
            self.speed = self.base_speed + 5
            self.speed_effect_end = now + POWERUP_EFFECT_MS
            self.speed_effect_type = "speed_boost"
        elif ptype == "slow_motion":
            self.speed = max(2, self.base_speed - 4)
            self.speed_effect_end = now + POWERUP_EFFECT_MS
            self.speed_effect_type = "slow_motion"
        elif ptype == "shield":
            self.shield_active = True

    # ── Draw ─────────────────────────────────────────────────────────────────
    def draw(self, surface: pygame.Surface, small_font: pygame.font.Font,
             tiny_font: pygame.font.Font):
        # Grid
        if self.grid_overlay:
            for c in range(COLS):
                for r in range(ROWS):
                    pygame.draw.rect(surface, (25, 25, 40), cell_rect(c, r), 1)

        # Obstacles
        for pos in self.obstacles:
            r = cell_rect(*pos)
            pygame.draw.rect(surface, GRAY, r)
            pygame.draw.rect(surface, LIGHT_GRAY, r, 2)

        # Food
        now = pygame.time.get_ticks()
        for food in self.foods:
            food.draw(surface, now)

        # Power-up
        if self.powerup:
            self.powerup.draw(surface, tiny_font)

        # Snake
        self.snake.draw(surface)

        # HUD
        self._draw_hud(surface, small_font, tiny_font)

    def _draw_hud(self, surface: pygame.Surface,
                  small_font: pygame.font.Font, tiny_font: pygame.font.Font):
        now = pygame.time.get_ticks()
        pad = 8
        line_h = small_font.get_height() + 4

        def txt(text, color, x, y):
            s = small_font.render(text, True, color)
            surface.blit(s, (x, y))

        txt(f"Score: {self.score}",  WHITE,   pad, pad)
        txt(f"Level: {self.level}",  YELLOW,  pad, pad + line_h)
        txt(f"Best:  {self.personal_best}", CYAN, pad, pad + line_h * 2)
        txt(f"User:  {self.username}", LIGHT_GRAY, pad, pad + line_h * 3)

        # Active effects
        ey = pad
        if self.shield_active:
            txt("🛡 SHIELD", PURPLE, surface.get_width() - 120, ey)
            ey += line_h
        if self.speed_effect_end:
            remaining = max(0, self.speed_effect_end - now) // 1000
            color = ORANGE if self.speed_effect_type == "speed_boost" else BLUE
            label = "FAST" if self.speed_effect_type == "speed_boost" else "SLOW"
            txt(f"⚡ {label} {remaining}s", color,
                surface.get_width() - 120, ey)
