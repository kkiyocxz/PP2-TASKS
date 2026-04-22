import pygame
import sys
from player import MusicPlayer

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

font_big = pygame.font.SysFont("Arial", 32)
font_small = pygame.font.SysFont("Arial", 22)

player = MusicPlayer("music/")
clock = pygame.time.Clock()

def draw_ui():
    screen.fill((30, 30, 30))  # тёмный фон

    # Название трека
    title = font_big.render("🎵 Music Player", True, (255, 255, 255))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))

    # Текущий трек
    track_name = font_small.render(f"Трек: {player.get_track_name()}", True, (200, 200, 200))
    screen.blit(track_name, (WIDTH // 2 - track_name.get_width() // 2, 130))

    # Статус
    status = "▶ Играет" if player.is_playing else "⏹ Остановлено"
    status_text = font_small.render(status, True, (100, 255, 100) if player.is_playing else (255, 100, 100))
    screen.blit(status_text, (WIDTH // 2 - status_text.get_width() // 2, 180))

    # Управление
    controls = [
        "P — Play   |   S — Stop",
        "N — Next   |   B — Back",
        "Q — Quit"
    ]
    for i, line in enumerate(controls):
        text = font_small.render(line, True, (180, 180, 180))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 270 + i * 35))

    pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.next_track()
            elif event.key == pygame.K_b:
                player.prev_track()
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

    draw_ui()
    clock.tick(30)