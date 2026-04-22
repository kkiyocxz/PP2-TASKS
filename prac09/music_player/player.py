import pygame
import os

class MusicPlayer:
    def __init__(self, music_folder):
        pygame.mixer.init()
        self.tracks = []        # список треков
        self.current_index = 0  # текущий трек
        self.is_playing = False

        # Загружаем все .mp3 и .wav файлы из папки
        if os.path.exists(music_folder):
            for file in os.listdir(music_folder):
                if file.endswith(('.mp3', '.wav')):
                    self.tracks.append(os.path.join(music_folder, file))

    def play(self):
        if not self.tracks:
            print("Нет треков в папке music/")
            return
        pygame.mixer.music.load(self.tracks[self.current_index])
        pygame.mixer.music.play()
        self.is_playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_track(self):
        if not self.tracks:
            return
        self.current_index = (self.current_index + 1) % len(self.tracks)
        self.play()

    def prev_track(self):
        if not self.tracks:
            return
        self.current_index = (self.current_index - 1) % len(self.tracks)
        self.play()

    def get_track_name(self):
        if not self.tracks:
            return "Нет треков"
        return os.path.basename(self.tracks[self.current_index])