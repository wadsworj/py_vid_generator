import os
import pygame
from pygame.locals import *
import cv2
import config
from pygame import mixer


class Video:
    def __init__(self):
        self.name = None
        self.video = None
        self.resolution = None
        self.screen = None
        self.scenes = []
        self.current_scene = None
        self.audio_file = None
        self.playing_audio = False
        self.back_color = None
        self.debug = False
        self.start_seconds = 0

    def add_scene(self, scene):
        self.scenes.append(scene)

    def render(self):
        self.play_audio()

        done_capturing = False

        file_num = 0
        scene_file_start = 1
        self.current_scene = self.scenes.pop(0)
        clock = pygame.time.Clock()

        while not done_capturing:
            pygame.display.update()

            file_num = file_num + 1
            # Save every frame
            filename = "output/%04d.png" % file_num
            pygame.image.save(self.screen, filename)

            self.screen.fill(self.back_color)

            clock.tick(config.FRAME_RATE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done_capturing = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        done_capturing = True

            if self.current_scene:
                if self.debug:
                    self.render_debug_info()

                self.current_scene.render(self.screen, self.start_seconds)

                if self.current_scene.finished:
                    self.save_video_file(scene_file_start, file_num)
                    scene_file_start = file_num + 1

                    if self.scenes:
                        self.current_scene = self.scenes.pop(0)
                    else:
                        return

    def render_debug_info(self):
        video_time = pygame.time.get_ticks()
        seconds = (video_time / 1000) % 60

        my_font = pygame.font.SysFont('Comic Sans MS', 30)
        text_surface = my_font.render(str(seconds) + " seconds", True, config.RED)
        screen_rect = self.screen.get_rect()
        self.screen.blit(text_surface, (0,0))

    def save_video_file(self, scene_file_start, scene_file_end):
        images = [img for img in os.listdir("output") if img.endswith(".png")]
        frame = cv2.imread(os.path.join("output", images[0]))
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video = cv2.VideoWriter("output_video/" + str(scene_file_start) + "_" + str(scene_file_end) + ".avi", fourcc, config.FRAME_RATE, (self.resolution[0], self.resolution[1]))

        for image in images[scene_file_start:scene_file_end]:
            video.write(cv2.imread(os.path.join("output", image)))

        cv2.destroyAllWindows()
        video.release()

    def play_audio(self):
        # play music if it is configured
        if self.audio_file and not self.playing_audio:
            count = 0
            mixer.init()
            for audio in self.audio_file:
                mixer.music.load("audio/" + audio)
                # Setting the volume
                if count > 0:
                    mixer.music.set_volume(0.5)

                # Start playing the song
                mixer.music.play()
                mixer.music.set_pos(self.start_seconds)
                count = count + 1