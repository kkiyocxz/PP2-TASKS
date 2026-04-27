# main.py — Entry point: all screens & game loop

import sys
import pygame
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, TITLE, CELL_SIZE,
    BG_COLOR, WHITE, BLACK, GRAY, DARK_GRAY, LIGHT_GRAY,
    GREEN, DARK_GREEN, RED, YELLOW, CYAN, ORANGE, BLUE, PURPLE,
)
from game import GameSession, UP, DOWN, LEFT, RIGHT
from db import init_db, save_session, get_personal_best, get_leaderboard
from settings import load_settings, save_settings

# ─── Colors ───────────────────────────────────────────────────────────────────
ACCENT    = (0,  200,  80)
HEADER    = (20,  20,  40)
PANEL_BG  = (30,  30,  50)


# ─── UI helpers ───────────────────────────────────────────────────────────────

def draw_rect_alpha(surface, color, rect, alpha=180):
    s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    s.fill((*color, alpha))
    surface.blit(s, rect.topleft)


class Button:
    def __init__(self, rect: pygame.Rect, text: str,
                 color=ACCENT, text_color=WHITE, font=None):
        self.rect = rect
        self.text = text
        self.color = color
        self.hover_color = tuple(min(255, c + 40) for c in color)
        self.text_color = text_color
        self.font = font

    def draw(self, surface, font):
        f = self.font or font
        mouse = pygame.mouse.get_pos()
        c = self.hover_color if self.rect.collidepoint(mouse) else self.color
        pygame.draw.rect(surface, c, self.rect, border_radius=8)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=8)
        label = f.render(self.text, True, self.text_color)
        surface.blit(label, label.get_rect(center=self.rect.center))

    def is_clicked(self, event) -> bool:
        return (event.type == pygame.MOUSEBUTTONDOWN and
                event.button == 1 and
                self.rect.collidepoint(event.pos))


# ─── App ──────────────────────────────────────────────────────────────────────

class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        self.font_big   = pygame.font.SysFont("consolas", 48, bold=True)
        self.font_med   = pygame.font.SysFont("consolas", 28)
        self.font_small = pygame.font.SysFont("consolas", 18)
        self.font_tiny  = pygame.font.SysFont("consolas", 12)

        self.settings = load_settings()
        self.db_ok = init_db()
        if not self.db_ok:
            print("[App] Running without database (leaderboard disabled).")

        self.username = ""
        self.state = "menu"      # menu | game | gameover | leaderboard | settings
        self.session: GameSession | None = None
        self.last_score = 0
        self.last_level = 1

    # ── Main loop ─────────────────────────────────────────────────────────────
    def run(self):
        while True:
            if   self.state == "menu":        self.menu_screen()
            elif self.state == "game":        self.game_loop()
            elif self.state == "gameover":    self.gameover_screen()
            elif self.state == "leaderboard": self.leaderboard_screen()
            elif self.state == "settings":    self.settings_screen()

    # ── Background ────────────────────────────────────────────────────────────
    def _draw_bg(self):
        self.screen.fill(BG_COLOR)
        # subtle grid
        for x in range(0, WINDOW_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, (22, 22, 35), (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, (22, 22, 35), (0, y), (WINDOW_WIDTH, y))

    # ─────────────────────────────────────────────────────────────────────────
    # MAIN MENU
    # ─────────────────────────────────────────────────────────────────────────
    def menu_screen(self):
        input_active = True
        username_buf = self.username

        bw, bh = 220, 50
        bx = WINDOW_WIDTH // 2 - bw // 2
        buttons = {
            "play":        Button(pygame.Rect(bx, 320, bw, bh), "▶  Play",     ACCENT),
            "leaderboard": Button(pygame.Rect(bx, 385, bw, bh), "🏆 Leaderboard", (80, 60, 160)),
            "settings":    Button(pygame.Rect(bx, 450, bw, bh), "⚙  Settings", (60, 100, 160)),
            "quit":        Button(pygame.Rect(bx, 515, bw, bh), "✕  Quit",     (160, 50, 50)),
        }
        input_rect = pygame.Rect(WINDOW_WIDTH // 2 - 150, 240, 300, 46)

        while self.state == "menu":
            self._draw_bg()

            # Title
            title = self.font_big.render("🐍  SNAKE", True, ACCENT)
            self.screen.blit(title, title.get_rect(center=(WINDOW_WIDTH // 2, 100)))
            sub = self.font_small.render("TSIS-4  ·  PostgreSQL Edition", True, LIGHT_GRAY)
            self.screen.blit(sub, sub.get_rect(center=(WINDOW_WIDTH // 2, 158)))

            # Username input
            lbl = self.font_small.render("Enter username:", True, LIGHT_GRAY)
            self.screen.blit(lbl, (input_rect.x, input_rect.y - 24))
            border_col = ACCENT if input_active else GRAY
            pygame.draw.rect(self.screen, DARK_GRAY, input_rect, border_radius=6)
            pygame.draw.rect(self.screen, border_col, input_rect, 2, border_radius=6)
            ub = self.font_med.render(username_buf + ("_" if pygame.time.get_ticks() % 1000 < 500 else ""),
                                      True, WHITE)
            self.screen.blit(ub, (input_rect.x + 10, input_rect.y + 8))

            for btn in buttons.values():
                btn.draw(self.screen, self.font_med)

            if not self.db_ok:
                warn = self.font_tiny.render("⚠ DB not connected — leaderboard disabled", True, YELLOW)
                self.screen.blit(warn, (10, WINDOW_HEIGHT - 20))

            pygame.display.flip()
            self.clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        username_buf = username_buf[:-1]
                    elif event.key == pygame.K_RETURN:
                        if username_buf.strip():
                            self.username = username_buf.strip()
                            self.state = "game"
                    elif len(username_buf) < 20:
                        if event.unicode.isprintable():
                            username_buf += event.unicode

                if buttons["play"].is_clicked(event):
                    if not username_buf.strip():
                        continue
                    self.username = username_buf.strip()
                    self.state = "game"
                elif buttons["leaderboard"].is_clicked(event):
                    self.state = "leaderboard"
                elif buttons["settings"].is_clicked(event):
                    self.state = "settings"
                elif buttons["quit"].is_clicked(event):
                    self._quit()

    # ─────────────────────────────────────────────────────────────────────────
    # GAME LOOP
    # ─────────────────────────────────────────────────────────────────────────
    def game_loop(self):
        pb = get_personal_best(self.username) if self.db_ok else 0
        snake_color = tuple(self.settings.get("snake_color", [0, 200, 0]))
        grid = self.settings.get("grid_overlay", False)

        self.session = GameSession(
            username=self.username,
            personal_best=pb,
            snake_color=snake_color,
            grid_overlay=grid,
        )
        session = self.session

        move_timer = 0
        paused = False

        while self.state == "game":
            dt = self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = "menu"
                        return
                    if event.key == pygame.K_p:
                        paused = not paused
                    if not paused:
                        if event.key in (pygame.K_UP,    pygame.K_w): session.snake.set_direction(UP)
                        if event.key in (pygame.K_DOWN,  pygame.K_s): session.snake.set_direction(DOWN)
                        if event.key in (pygame.K_LEFT,  pygame.K_a): session.snake.set_direction(LEFT)
                        if event.key in (pygame.K_RIGHT, pygame.K_d): session.snake.set_direction(RIGHT)

            if not paused:
                move_timer += dt
                interval = max(50, 1000 // session.speed)
                if move_timer >= interval:
                    move_timer = 0
                    result = session.update()
                    if result == "dead":
                        self.last_score = session.score
                        self.last_level = session.level
                        if self.db_ok:
                            save_session(self.username, session.score, session.level)
                        self.state = "gameover"
                        return

            self._draw_bg()
            session.draw(self.screen, self.font_small, self.font_tiny)

            if paused:
                overlay = self.font_big.render("PAUSED", True, YELLOW)
                self.screen.blit(overlay, overlay.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)))

            pygame.display.flip()

    # ─────────────────────────────────────────────────────────────────────────
    # GAME OVER
    # ─────────────────────────────────────────────────────────────────────────
    def gameover_screen(self):
        pb = get_personal_best(self.username) if self.db_ok else self.last_score
        bw, bh = 220, 50
        cx = WINDOW_WIDTH // 2
        retry_btn = Button(pygame.Rect(cx - bw - 20, 430, bw, bh), "↺  Retry",     ACCENT)
        menu_btn  = Button(pygame.Rect(cx + 20,      430, bw, bh), "⌂  Main Menu", (80, 60, 160))

        while self.state == "gameover":
            self._draw_bg()

            # Panel
            panel = pygame.Rect(cx - 220, 100, 440, 360)
            draw_rect_alpha(self.screen, PANEL_BG[:3], panel, 200)
            pygame.draw.rect(self.screen, RED, panel, 3, border_radius=10)

            go = self.font_big.render("GAME OVER", True, RED)
            self.screen.blit(go, go.get_rect(center=(cx, 145)))

            def stat(label, value, color, y):
                ls = self.font_med.render(label, True, LIGHT_GRAY)
                vs = self.font_med.render(str(value), True, color)
                self.screen.blit(ls, ls.get_rect(right=cx - 10, centery=y))
                self.screen.blit(vs, vs.get_rect(left=cx + 10, centery=y))

            stat("Score",         self.last_score, WHITE,  220)
            stat("Level",         self.last_level, YELLOW, 270)
            stat("Personal Best", pb,              CYAN,   320)

            retry_btn.draw(self.screen, self.font_med)
            menu_btn.draw(self.screen, self.font_med)

            pygame.display.flip()
            self.clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._quit()
                if retry_btn.is_clicked(event):
                    self.state = "game"
                elif menu_btn.is_clicked(event):
                    self.state = "menu"

    # ─────────────────────────────────────────────────────────────────────────
    # LEADERBOARD
    # ─────────────────────────────────────────────────────────────────────────
    def leaderboard_screen(self):
        rows = get_leaderboard(10) if self.db_ok else []
        back_btn = Button(pygame.Rect(WINDOW_WIDTH // 2 - 110, 545, 220, 44), "← Back", (80, 60, 160))
        col_heads = ["#", "Username", "Score", "Level", "Date"]
        col_xs    = [40, 90, 310, 420, 510]

        while self.state == "leaderboard":
            self._draw_bg()

            title = self.font_big.render("🏆  Leaderboard", True, YELLOW)
            self.screen.blit(title, title.get_rect(center=(WINDOW_WIDTH // 2, 55)))

            # Header row
            for i, h in enumerate(col_heads):
                hs = self.font_small.render(h, True, CYAN)
                self.screen.blit(hs, (col_xs[i], 110))
            pygame.draw.line(self.screen, GRAY, (30, 130), (WINDOW_WIDTH - 30, 130), 1)

            if not self.db_ok:
                m = self.font_med.render("Database not connected", True, RED)
                self.screen.blit(m, m.get_rect(center=(WINDOW_WIDTH // 2, 280)))
            elif not rows:
                m = self.font_med.render("No records yet — play a game!", True, LIGHT_GRAY)
                self.screen.blit(m, m.get_rect(center=(WINDOW_WIDTH // 2, 280)))
            else:
                for i, row in enumerate(rows):
                    y = 140 + i * 38
                    color = YELLOW if i == 0 else (WHITE if i < 3 else LIGHT_GRAY)
                    vals = [str(row["rank"]), row["username"], str(row["score"]),
                            str(row["level"]), row["date"]]
                    for j, val in enumerate(vals):
                        vs = self.font_small.render(val, True, color)
                        self.screen.blit(vs, (col_xs[j], y))

            back_btn.draw(self.screen, self.font_med)
            pygame.display.flip()
            self.clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = "menu"
                if back_btn.is_clicked(event):
                    self.state = "menu"

    # ─────────────────────────────────────────────────────────────────────────
    # SETTINGS
    # ─────────────────────────────────────────────────────────────────────────
    def settings_screen(self):
        s = dict(self.settings)   # working copy

        COLOR_OPTIONS = {
            "Green":  [0,   200, 0],
            "Blue":   [50,  100, 220],
            "Yellow": [230, 200, 0],
            "Orange": [230, 120, 0],
            "Purple": [180, 80,  220],
            "Cyan":   [0,   200, 220],
        }
        color_names = list(COLOR_OPTIONS.keys())

        def current_color_name():
            for name, rgb in COLOR_OPTIONS.items():
                if rgb == s["snake_color"]:
                    return name
            return "Custom"

        save_btn = Button(pygame.Rect(WINDOW_WIDTH // 2 - 110, 500, 220, 50),
                          "💾 Save & Back", ACCENT)

        cy = current_color_name()

        while self.state == "settings":
            self._draw_bg()

            title = self.font_big.render("⚙  Settings", True, WHITE)
            self.screen.blit(title, title.get_rect(center=(WINDOW_WIDTH // 2, 60)))

            cx_ = WINDOW_WIDTH // 2

            def row_label(text, y):
                ls = self.font_med.render(text, True, LIGHT_GRAY)
                self.screen.blit(ls, (80, y))

            # Grid
            row_label("Grid Overlay:", 180)
            gc = ACCENT if s["grid_overlay"] else GRAY
            grid_btn = Button(pygame.Rect(cx_ - 60, 175, 140, 40),
                              "ON" if s["grid_overlay"] else "OFF", gc)
            grid_btn.draw(self.screen, self.font_med)

            # Sound
            row_label("Sound:", 250)
            sc = ACCENT if s["sound"] else GRAY
            sound_btn = Button(pygame.Rect(cx_ - 60, 245, 140, 40),
                               "ON" if s["sound"] else "OFF", sc)
            sound_btn.draw(self.screen, self.font_med)

            # Snake color
            row_label("Snake Color:", 320)
            prev_btn = Button(pygame.Rect(cx_ - 120, 315, 40, 40), "◀", (60, 60, 100))
            next_btn = Button(pygame.Rect(cx_ + 80,  315, 40, 40), "▶", (60, 60, 100))
            prev_btn.draw(self.screen, self.font_med)
            next_btn.draw(self.screen, self.font_med)

            color_val = tuple(s["snake_color"])
            pygame.draw.rect(self.screen, color_val,
                             pygame.Rect(cx_ - 70, 315, 140, 40), border_radius=6)
            pygame.draw.rect(self.screen, WHITE,
                             pygame.Rect(cx_ - 70, 315, 140, 40), 2, border_radius=6)
            cn = self.font_small.render(cy, True, WHITE)
            self.screen.blit(cn, cn.get_rect(center=(cx_, 335)))

            save_btn.draw(self.screen, self.font_med)
            pygame.display.flip()
            self.clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = "menu"

                if grid_btn.is_clicked(event):
                    s["grid_overlay"] = not s["grid_overlay"]
                if sound_btn.is_clicked(event):
                    s["sound"] = not s["sound"]

                if prev_btn.is_clicked(event):
                    idx = (color_names.index(cy) - 1) % len(color_names) \
                          if cy in color_names else 0
                    cy = color_names[idx]
                    s["snake_color"] = COLOR_OPTIONS[cy]
                if next_btn.is_clicked(event):
                    idx = (color_names.index(cy) + 1) % len(color_names) \
                          if cy in color_names else 0
                    cy = color_names[idx]
                    s["snake_color"] = COLOR_OPTIONS[cy]

                if save_btn.is_clicked(event):
                    self.settings = s
                    save_settings(s)
                    self.state = "menu"

    # ── Quit ─────────────────────────────────────────────────────────────────
    def _quit(self):
        pygame.quit()
        sys.exit()


# ─── Entry ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    App().run()
